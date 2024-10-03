import pyreadstat
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import data
from data import renda_filtrada_rural, renda_filtrada_urbana

# Cálculo da média de renda para cada categoria (rural e urbana)
media_renda_rural = data.media(renda_filtrada_rural)
media_renda_urbana = data.media(renda_filtrada_urbana)

# Cálculo da mediana de renda para cada categoria (rural e urbana)
mediana_renda_rural = data.mediana(renda_filtrada_rural)
mediana_renda_urbana = data.mediana(renda_filtrada_urbana)

# Cálculo da curva de Lorenz para cada categoria (rural e urbana)
renda_acumulada_rural, populacao_acumulada_rural = data.lorenz(renda_filtrada_rural)
renda_acumulada_urbana, populacao_acumulada_urbana = data.lorenz(renda_filtrada_urbana)

# Inserção do ponto inicial (0,0) para as curvas de Lorenz
renda_acumulada_rural = np.insert(renda_acumulada_rural, 0, 0)
populacao_acumulada_rural = np.insert(populacao_acumulada_rural, 0, 0)
renda_acumulada_urbana = np.insert(renda_acumulada_urbana, 0, 0)
populacao_acumulada_urbana = np.insert(populacao_acumulada_urbana, 0, 0)

# Cálculo do índice de Gini para cada categoria (rural e urbana)
i_gini_rural = data.indice_gini(renda_acumulada_rural, populacao_acumulada_rural)
i_gini_urbana = data.indice_gini(renda_acumulada_urbana, populacao_acumulada_urbana)

# Função para gerar tabela de comparação entre rural e urbano
def gerar_tabela_comparação_rural_urbano(media_renda_rural, media_renda_urbana, mediana_renda_rural, mediana_renda_urbana, i_gini_rural, i_gini_urbana):
    nova_tabela = pd.DataFrame()
    nova_tabela["Categoria"] = ["Rural", "Urbana"]
    nova_tabela["Média de renda"] = [media_renda_rural, media_renda_urbana]
    nova_tabela["Mediana de renda"] = [mediana_renda_rural, mediana_renda_urbana]
    nova_tabela["Índice de Gini"] = [i_gini_rural, i_gini_urbana]
    return nova_tabela

# Gerar tabela de comparação
tabela_rural_urbano = gerar_tabela_comparação_rural_urbano(media_renda_rural, media_renda_urbana, mediana_renda_rural, mediana_renda_urbana, i_gini_rural, i_gini_urbana)

# Visualização dos dados
st.markdown("# Análise de dados da PNAD - Ceará 2023")
st.markdown("Distribuição de renda pessoal e suas diferenças entre áreas rurais e urbanas")
st.divider()

# Histograma de renda
fig_hist_rural_urbano = px.histogram(
    pd.concat([renda_filtrada_rural.assign(area="Rural"), renda_filtrada_urbana.assign(area="Urbana")]),
    x="Faixa_renda",
    histnorm="percent",
    category_orders={"Faixa_renda": ["< 1", "1-2", "2-5", "5-10", ">= 10"]},
    title="Histograma da Renda do Estado do Ceará",
    color="area",
    barmode="group",
    color_discrete_map={"Rural": "#4B02D4", "Urbana": "#6E60FF"}
)

# Curva de Lorenz
fig_lorenz_rural_urbano = go.Figure()
fig_lorenz_rural_urbano.add_trace(
    go.Scatter(
        x=populacao_acumulada_rural,
        y=renda_acumulada_rural,
        mode="lines",
        name="Curva Rural",
        line=dict(color="#6E60FF"),
    )
)
fig_lorenz_rural_urbano.add_trace(
    go.Scatter(
        x=populacao_acumulada_urbana,
        y=renda_acumulada_urbana,
        mode="lines",
        name="Curva Urbana",
        line=dict(color="#4B02D4"),
    )
)
fig_lorenz_rural_urbano.add_trace(
    go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        name="Linha de Igualdade",
        line=dict(dash="dash", color="gray"),
    )
)
fig_lorenz_rural_urbano.update_layout(
    title="Curva de Lorenz da Rendas",
    xaxis_title="Proporção Acumulada da População",
    yaxis_title="Proporção Acumulada da Renda",
    showlegend=True,
)

# Exibir gráficos e tabelas
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.plotly_chart(fig_hist_rural_urbano, use_container_width=True)
    st.markdown("### Tabela de comparação de renda entre áreas rurais e urbanas")
    st.table(tabela_rural_urbano)

with col2:
    st.plotly_chart(fig_lorenz_rural_urbano, use_container_width=True)