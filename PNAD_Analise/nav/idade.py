"histogama; frequencia acumulada"

import pyreadstat
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu  # Adicionando a importação necessária
import data
from data import mai20, men80, media80, media20, mediana80, mediana20
from data import media_renda, mediana_renda, i_gini, renda_acumulada, populacao_acumulada

df = data.renda_filtrada[data.renda_filtrada["V2009"] <= 80]

# Adicionando uma coluna de categorias de idade
bins = [20, 30, 40, 50, 60, 80]
labels = ['20-29', '30-39', '40-49', '50-59', '60+']
df['Faixa_Etaria'] = pd.cut(df['V2009'], bins=bins, labels=labels, right=False, ordered=True)

fig_hist = px.histogram(
    df,
    x="Faixa_renda",
    histnorm="percent",
    category_orders={
        "Faixa_renda": ["< 1", "1-2", "2-5", "5-10", ">= 10"],
        "Faixa_Etaria": ['20-29', '30-39', '40-49', '50-59', '60+'],
    },
    title="Histograma da Renda do Estado do Ceará",
    color="Faixa_Etaria",
    barmode="group",
    color_discrete_map={"1": "#7e72fc", "2": "#4B02D4", "3": "#30038a"},
)

# Garantindo a ordem correta das categorias
df['Faixa_Etaria'] = pd.Categorical(df['Faixa_Etaria'], categories=labels, ordered=True)

# Ordenando o DataFrame pela faixa etária
df = df.sort_values(by='Faixa_Etaria')

# Criando o box plot
figg = px.box(df, x='Faixa_Etaria', y='VD4019', title='Box Plot das Idades por Faixa Etária')



# Criando o gráfico de dispersão
fig = px.scatter(df, x="V2009", y="VD4019", trendline="ols")



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

with col1:
    st.plotly_chart(fig_hist)

    
with col2:
    st.plotly_chart(fig)

    st.plotly_chart(figg)