import pyreadstat
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu  # Adicionando a importação necessária
import data
from data import renda_acumulada, populacao_acumulada, renda_filtrada


st.markdown(
    """
# Análise de dados da PNAD - Ceará
Dashboard para análise de dados da PNAD do Ceará 2023
    """
)
st.divider()
option = st.selectbox(
    "escolha a forma de vizualização:",
    ["Histograma", "Gráfico de setores", "Tabela"],
)
col1, col2 = st.columns([1, 1], gap="large")


fig_hist = px.histogram(
    renda_filtrada,
    x="Faixa_renda",
    histnorm="percent",
    category_orders={"Faixa_renda": ["< 1", "1-2", "2-5", "5-10", ">= 10"]},
    title="Histograma da Renda do Estado do Ceará",
)

fig_sec = px.pie(
    renda_filtrada,
    names="Faixa_renda",
    title="Proporção de Pessoas por Faixa de Renda",
    hole=0.25,
    color_discrete_sequence=["#9712E0", "#090BF0", "#00CC96", "#AB63FA", "#FFA15A"],
)


with col1:
    
    if option == "Histograma":
        fig_hist.update_traces(marker_color="#6E60FF")
        st.plotly_chart(
            fig_hist,
            use_container_width=True,
        )
    elif option == "Gráfico de setores":
        st.plotly_chart(fig_sec, use_container_width=True)
    else:
        tabelageral = data.gerar_tabela(renda_filtrada)
        st.table(tabelageral)

    col3, col4 = st.columns([1, 1])

    with col3:
        desviop = data.gerar_desvio_padrao(renda_filtrada)

        col3.metric(
            "Mediana",
            f"R$ {data.mediana_renda:.2f}",
            delta=f"{(data.mediana_renda - data.media_renda):.2f} em relação a média",
        )
        col3.divider()

        col3.metric(
            "Mediana do 80% mais pobres",
            f"R$ {data.mediana80:.2f}",
            delta=f"{(data.mediana80 - data.media_renda):.2f} em relação a média",
        )
        col3.metric(
            "Desvio Padrão",
            f"R$ {desviop:.2f}",
        )

    with col4:

        col4.metric(
            "Média",
            f"R$ {data.media_renda:.2f}",
            delta=f"{(data.tamanho):.0f} pessoas analisadas",
            delta_color="off",
        )
        col4.divider()
        col4.metric(
            "Mediana do 20% mais ricos",
            f"R$ {data.mediana20:.2f}",
            delta=f"{(data.mediana20 - data.media_renda):.2f} em relação a média",
        )

# Adicionar o ponto (0,0) para a curva de Lorenz


# Plotar a Curva de Lorenz
fig_lorenz = go.Figure()
fig_lorenz.add_trace(
    go.Scatter(
        x=populacao_acumulada,
        y=renda_acumulada,
        mode="lines",
        name="Curva de Lorenz",
        line=dict(color="#6E60FF"),
    )
)
fig_lorenz.add_trace(
    go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        name="Linha de Igualdade",
        line=dict(dash="dash", color="gray"),
    )
)

fig_lorenz.update_layout(
    title="Curva de Lorenz da Renda do Estado do Ceará",
    xaxis_title="Proporção Acumulada da População",
    yaxis_title="Proporção Acumulada da Renda",
    showlegend=True,
)
with col2:
    st.plotly_chart(fig_lorenz, use_container_width=True)
    col2.markdown(f"## Indice de Gini: :violet[{data.i_gini:.4f}]")
    col2.markdown(
        """O **indice de Gini** é calculado pela área entre a linha de igualdade e a curva de Lorenz.
                  O valor de Gini varia de 0 a 1, sendo 0 a igualdade perfeita e 1 a desigualdade máxima.
                  No Brasil, o índice de Gini é de aproximadamente :blue[**0,518**] :gray[(IBGE, 2023).]"""
    )
    # st.divider()
    st.markdown(
        """## 20% mais ricos x 80% mais pobres:
        
        """
    )
    st.markdown(
        f"""
        Os :green[20%] mais rico detem :violet[**{data.mai20:.2f}%**] da riqueza, enquanto os :blue[80%] mais pobres detem :violet[**{data.men80:.2f}%**] da riqueza.
        """
    )
    st.markdown(
        f"""
        A média de renda dos :green[20%] mais ricos é de :violet[**R$ {data.media20:.2f}**], enquanto a dos :blue[80%] mais pobres é de :violet[**R$ {data.media80:.2f}**].
        """
    )
