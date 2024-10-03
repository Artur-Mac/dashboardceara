import pyreadstat
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu  # Adicionando a importação necessária
import data
from data import renda_filtrada_fem, renda_filtrada_masc

"""
tabela
grafico de comparação 
indice de gini de cada categoria
coeficiente de contigencia de pearson
"""


# Cálculo da média de renda para cada sexo
media_renda_masc = data.media(renda_filtrada_masc)
media_renda_fem = data.media(renda_filtrada_fem)

# Cálculo da mediana de renda para cada sexo
mediana_renda_masc = data.mediana(renda_filtrada_masc)
mediana_renda_fem = data.mediana(renda_filtrada_fem)

# Cálculo da curva de Lorenz para cada sexo
renda_acumulada_masc, populacao_acumulada_masc = data.lorenz(renda_filtrada_masc)
renda_acumulada_fem, populacao_acumulada_fem = data.lorenz(renda_filtrada_fem)

# Inserção do ponto inicial (0,0) para as curvas de Lorenz
renda_acumulada_masc = np.insert(renda_acumulada_masc, 0, 0)
populacao_acumulada_masc = np.insert(populacao_acumulada_masc, 0, 0)
renda_acumulada_fem = np.insert(renda_acumulada_fem, 0, 0)
populacao_acumulada_fem = np.insert(populacao_acumulada_fem, 0, 0)

# Cálculo do índice de Gini para cada sexo
i_gini_masc = data.indice_gini(renda_acumulada_masc, populacao_acumulada_masc)
i_gini_fem = data.indice_gini(renda_acumulada_fem, populacao_acumulada_fem)

# Cálculo da razão 80/20 para cada sexo
(
    mai20_masc,
    men80_masc,
    media80_masc,
    media20_masc,
    mediana80_masc,
    data.mediana20_masc,
) = data.raz8020(renda_filtrada_masc)
mai20_fem, men80_fem, media80_fem, media20_fem, mediana80_fem, mediana20_fem = (
    data.raz8020(renda_filtrada_fem)
)


st.markdown("# Análise de dados da PNAD - Ceará 2023")
st.markdown("distribuição de renda pessoal e suas diferenças por sexo")
st.divider()

renda_filtrada_fem["sexo"] = "feminino"
renda_filtrada_masc["sexo"] = "masculino"
dfs = pd.concat([renda_filtrada_masc, renda_filtrada_fem])

# grafico de colunas bidimensional
def gerar_tabela_comparação_sexo(media_renda_masc, media_renda_fem, mediana_renda_masc, mediana_renda_fem, i_gini_masc, i_gini_fem, mai20_masc, mai20_fem):
    nova_tabela = pd.DataFrame()
    nova_tabela["sexo"] = ["masculino", "feminino"]
    nova_tabela["Média de renda"] = [media_renda_masc, media_renda_fem]
    nova_tabela["Mediana de renda"] = [mediana_renda_masc, mediana_renda_fem]
    nova_tabela["Índice de Gini"] = [i_gini_masc, i_gini_fem]
    nova_tabela["20% mais ricos"] = [mai20_masc.round(2), mai20_fem.round(2)]

    
    print(nova_tabela.head())
    return nova_tabela


fig_hist = px.histogram(
    dfs,
    x="Faixa_renda",
    histnorm="percent",
    category_orders={"Faixa_renda": ["< 1", "1-2", "2-5", "5-10", ">= 10"]},
    title="Histograma da Renda do Estado do Ceará",
    color="sexo",
    barmode="group",
    color_discrete_map={"masculino": "#4B02D4", "feminino": "#6E60FF"}
)
tabela = gerar_tabela_comparação_sexo(media_renda_masc, media_renda_fem, mediana_renda_masc, mediana_renda_fem, i_gini_masc, i_gini_fem, mai20_masc, mai20_fem)



col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.plotly_chart(
        fig_hist,
        use_container_width=True,
    
)
    st.markdown(
        """## Média e Mediana de Renda"""
        
        
    )
    st.markdown(
        f"""
        Em média, os homens ganham :violet[ {(100*(media_renda_masc - media_renda_fem)/media_renda_fem):.2f}%] a mais que as mulheres.
        """
    )
    st.markdown(
        f"""
        Entretanto, a mediana de renda é igual para os dois, denotando uma distribuição de renda mais desigual para os homens.
        """
    )

with col2:
    fig_lorenz = go.Figure()
    fig_lorenz.add_trace(
        go.Scatter(
            x=populacao_acumulada_masc,
            
            y=renda_acumulada_masc,
            mode="lines",
            name="Curva masculina",
            line=dict(color="#6E60FF"),
        )
    )
    fig_lorenz.add_trace(
        go.Scatter(
            x=populacao_acumulada_fem,
            y=renda_acumulada_fem,
            mode="lines",
            name="Curva feminina",
            line=dict( color="#4B02D4"),
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
    st.plotly_chart(fig_lorenz, use_container_width=True)
    st.markdown("### Tabela de comparação de renda entre os sexos")
    st.table(tabela)

    desvio_masc = data.gerar_desvio_padrao(renda_filtrada_masc)
    desvio_fem = data.gerar_desvio_padrao(renda_filtrada_fem)
    st.markdown("## Desvio padrão")
    st.markdown(f"""### :violet[**R$ {desvio_masc:.2f}**] X :blue[**R$ {desvio_fem:.2f}**]""")
    st.markdown(
        f"""
        O desvio padrão da renda dos :blue[homens] é de :violet[**R$ {desvio_masc:.2f}**], enquanto o desvio padrão da renda das :blue[mulheres] é de :violet[**R$ {desvio_fem:.2f}**].
        """
    )