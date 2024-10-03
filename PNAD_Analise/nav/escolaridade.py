import pyreadstat
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu  # Adicionando a importação necessária
import data
from data import renda_filtrada_alto, renda_filtrada_medio, renda_filtrada_baixo

media_rendab, mediana_rendab, i_ginib, renda_acumuladab, populacao_acumuladab = (
    data.gerar_todos_os_dados(renda_filtrada_baixo)
)
media_rendam, mediana_rendam, i_ginim, renda_acumuladam, populacao_acumuladam = (
    data.gerar_todos_os_dados(renda_filtrada_medio)
)
media_rendaa, mediana_rendaa, i_ginia, renda_acumuladaa, populacao_acumuladaa = (
    data.gerar_todos_os_dados(renda_filtrada_alto)
)

tabela_baixa = data.gerar_tabela(renda_filtrada_baixo)
tabela_media = data.gerar_tabela(renda_filtrada_medio)
tabela_alta = data.gerar_tabela(renda_filtrada_alto)


renda_filtrada_alto["escolaridade"] = "3"
renda_filtrada_medio["escolaridade"] = "2"
renda_filtrada_baixo["escolaridade"] = "1"

juntos = pd.concat([renda_filtrada_alto, renda_filtrada_medio, renda_filtrada_baixo])

fig_hist = px.histogram(
    juntos,
    x="Faixa_renda",
    histnorm="percent",
    category_orders={
        "Faixa_renda": ["< 1", "1-2", "2-5", "5-10", ">= 10"],
        "escolaridade": ["1", "2", "3"],
    },
    title="Histograma da Renda do Estado do Ceará",
    color="escolaridade",
    barmode="group",
    color_discrete_map={"1": "#7e72fc", "2": "#4B02D4", "3": "#30038a"},
)

mapping = {"< 1": "1", "1-2": "2", "2-5": "3", "5-10": "4", ">= 10": "5"}

# Aplicando o mapeamento
juntos["Faixa_renda"] = juntos["Faixa_renda"].replace(mapping)

nova_tabela = juntos[["escolaridade", "Faixa_renda"]]


correlacao = nova_tabela.corr(method="spearman")
correlacao_escolaridade_faixa_renda = correlacao.loc["escolaridade", "Faixa_renda"]


def gerar_tabela_comparação(
    media_rendab,
    media_rendam,
    media_rendaa,
    mediana_rendab,
    mediana_rendam,
    mediana_rendaa,
    i_ginib,
    i_ginim,
    i_ginia,
):
    nova_tabela = pd.DataFrame()
    nova_tabela["escolaridade"] = ["fundamental", "medio", "superior"]
    nova_tabela["Média de renda"] = [media_rendab, media_rendam, media_rendaa]
    nova_tabela["Mediana de renda"] = [mediana_rendab, mediana_rendam, mediana_rendaa]
    nova_tabela["Índice de Gini"] = [i_ginib, i_ginim, i_ginia]

    print(nova_tabela.head())
    return nova_tabela


tabelag = gerar_tabela_comparação(
    media_rendab,
    media_rendam,
    media_rendaa,
    mediana_rendab,
    mediana_rendam,
    mediana_rendaa,
    i_ginib,
    i_ginim,
    i_ginia
)
st.markdown("# Análise de dados da PNAD - Ceará 2023")
st.markdown("distribuição de renda pessoal e suas diferenças por nível de escolaridade")
st.divider()

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.plotly_chart(
        fig_hist,
        use_container_width=True,
    )
    st.markdown(
        "### Diferença de renda expressiva entre os :violet[**níveis de escolaridade**]"
    )
    st.markdown(
        f"""Enquanto a mediana de renda do nível fundamental é :violet[R${mediana_rendab:.2f}], a mediana de renda do nível médio é :violet[R${mediana_rendam:.2f}] e a mediana de renda do nível superior é :violet[R${mediana_rendaa:.2f}]."""
    )
    st.markdown("### Tabela de comparação de renda os níveis de escolaridade")
    st.table(tabelag)


with col2:
    option = st.selectbox(
        "escolha a forma de vizualização:",
        ["tabela nivel superior", "tabela nivel medio", "tabela nivel fundamental"],
    )
    if option == "tabela nivel superior":
        st.table(tabela_alta)
    elif option == "tabela nivel medio":
        st.table(tabela_media)
    else:
        st.table(tabela_baixa)

    st.divider()

    st.markdown("### correlação de Spearman")
    st.markdown(
        f"""A correlação de Spearman entre escolaridade e renda é de :violet[{correlacao_escolaridade_faixa_renda:.3f}], considerado um valor moderado e positivo.
        Quem tem mais escolaridade tende a ter uma renda maior.
        """
    )
    st.markdown("### Concentração de renda")
    st.markdown(
        f""" A concentração da maior parte da população que fez até o :violet[**nível fundamental**] é inferior a um salario minimo. Além disso apresenta valores abaixo de 1% para as faixas de renda mais altas.
        """
    )
    st.markdown(
        f""" A concentração de renda para quem fez o :violet[**nível médio**] é mais equilibrada em relação as outras, tendo o menor indice de gini.

        """
    )
    st.markdown(
        f""" A concentração de renda para quem fez o :violet[**nível superior**] é a mais desigual, com a media mais que o dobro da renda do nível médio.
        """
    )   
