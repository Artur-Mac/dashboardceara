"histogama; frequencia acumulada"
import pyreadstat
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu  # Adicionando a importação necessária
import data
from data import renda_filtrada_branco, renda_filtrada_pardo, renda_filtrada_pai

media_renda, mediana_renda, i_gini, renda_acumulada, populacao_acumulada = (
    data.gerar_todos_os_dados(data.renda_filtrada)
)

media_rendab, mediana_rendab, i_ginib, renda_acumuladab, populacao_acumuladab = (
    data.gerar_todos_os_dados(renda_filtrada_branco)
)
media_rendam, mediana_rendam, i_ginim, renda_acumuladam, populacao_acumuladam = (
    data.gerar_todos_os_dados(renda_filtrada_pardo)
)
media_rendaa, mediana_rendaa, i_ginia, renda_acumuladaa, populacao_acumuladaa = (
    data.gerar_todos_os_dados(renda_filtrada_pai)
)

mai20_br, men80_br, media80_br, media20_br, mediana80_br, mediana20_br = data.raz8020(
    renda_filtrada_branco
)
mai20_pa, men80_pa, media80_pa, media20_pa, mediana80_pa, mediana20_pa = data.raz8020(
    renda_filtrada_pai
)
mai20_par, men80_par, media80_par, media20_par, mediana80_par, mediana20_par = (
    data.raz8020(renda_filtrada_pardo)
)

tabela_branco = data.gerar_tabela(renda_filtrada_branco)
tabela_pardo = data.gerar_tabela(renda_filtrada_pardo)
tabela_pai = data.gerar_tabela(renda_filtrada_pai)
"""
st.table(tabela_branco)
st.table(tabela_pardo)
st.table(tabela_pai)"""

renda_filtrada_branco["cor"] = "branco"
renda_filtrada_pardo["cor"] = "pardo"
renda_filtrada_pai["cor"] = "pai"

juntos = pd.concat([renda_filtrada_branco, renda_filtrada_pardo, renda_filtrada_pai])

fig_hist = px.histogram(
    juntos,
    x="Faixa_renda",
    histnorm="percent",
    category_orders={
        "Faixa_renda": ["< 1", "1-2", "2-5", "5-10", ">= 10"],
        "cor": ["branco", "pardo", "pai"],
    },
    title="Histograma da Renda do Estado do Ceará",
    color="cor",
    barmode="group",
    color_discrete_map={"branco": "#980dd9", "pardo": "#0dd987", "pai": "#080ccf"},
)

fig_lorenz = go.Figure()
fig_lorenz.add_trace(
    go.Scatter(
        x=populacao_acumuladab,
        y=renda_acumuladab,
        mode="lines",
        name="Curva branco",
        line=dict(color="#980dd9"),
    )
)
fig_lorenz.add_trace(
    go.Scatter(
        x=populacao_acumuladam,
        y=renda_acumuladam,
        mode="lines",
        name="Curva pardo",
        line=dict(color="#0dd987"),
    )
)
fig_lorenz.add_trace(
    go.Scatter(
        x=populacao_acumuladaa,
        y=renda_acumuladaa,
        mode="lines",
        name="Curva pai",
        line=dict(color="#080ccf"),
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
    title="Curva de Lorenz da Rendas",
    xaxis_title="Proporção Acumulada da População",
    yaxis_title="Proporção Acumulada da Renda",
    showlegend=True,
)


st.markdown("# Análise de dados da PNAD - Ceará 2023")
st.markdown("distribuição de renda pessoal e suas diferenças por cor/raça")
st.divider()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.plotly_chart(fig_hist, use_container_width=True)

    col3, col4 = st.columns([1, 1])

    with col3:

        col3.metric(
            "Média de renda brancos",
            f"R$ {media_rendab:.2f}",
            delta=f"R${(media_rendab - media_renda):.2f} em relação a media geral",
            delta_color="inverse" if (media_rendab - media_renda) < 0 else "normal",
        )
        col3.divider()

        col3.metric(
            "Média de renda pretos, amarelos e indigenas",
            f"R$ {media_rendaa:.2f}",
            delta=f"R${(media_rendaa - media_renda):.2f} em relação a media geral",
            delta_color="inverse" if (media_rendaa - media_renda) < 0 else "normal",
        )

    with col4:
        col4.metric(
            "Média de renda pardos",
            f"R$ {media_rendam:.2f}",
            delta=f"R${(media_rendam - media_renda):.2f} em relação a media geral",
            delta_color="inverse" if (media_rendam - media_renda) < 0 else "normal",
        )
       
        

with col2:
    st.plotly_chart(fig_lorenz, use_container_width=True)

    st.markdown(
        """## Grande difereça de renda""")
    st.markdown(
        """Cerca de 95% da renda dos grupos minoritarios (pretos, amarelos e indigenas) esta entre <1 e 1-2 salarios minimos."""
    )
    