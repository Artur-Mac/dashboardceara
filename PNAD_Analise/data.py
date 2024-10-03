import pyreadstat
import pandas as pd
import numpy as np


def filtrar_renda(renda):
    renda["Faixa_renda"] = pd.cut(
        renda["VD4019"],
        bins=[0, sm, 2 * sm, 5 * sm, 10 * sm, float("inf")],
        labels=["< 1", "1-2", "2-5", "5-10", ">= 10"],
        right=False,  # Garante que o limite superior não seja incluído na próxima faixa
    )
    return renda["Faixa_renda"]


def divisao_sexo(renda):
    renda["sexo"] = pd.cut(
        renda["VD2007"],
        bins=[1, 2],
        labels=["homem", "mulher"],
    )
    return renda["VD2007"]


def media(renda):
    return renda["VD4019"].mean()


def mediana(renda):
    return renda["VD4019"].median()


def lorenz(renda):
    renda = renda["VD4019"].sort_values()
    renda_acumulada = np.cumsum(renda) / renda.sum()
    n = len(renda)
    populacao_acumulada = np.arange(1, n + 1) / n
    return renda_acumulada, populacao_acumulada


def indice_gini(renda_acumulada, populacao_acumulada):

    area_sob_lorenz = np.trapz(renda_acumulada, populacao_acumulada)

    # Calcular a área entre a linha de igualdade e a Curva de Lorenz
    area_entre_linhas = 0.5 - area_sob_lorenz

    # Calcular o índice de Gini
    indice_gini = 2 * area_entre_linhas

    print(f"Índice de Gini: {indice_gini}")
    return indice_gini


def raz8020(renda):
    print(renda)
    renda = renda["VD4019"].sort_values()
    print(renda)
    renda_acumulada = np.cumsum(renda) / renda.sum()
    n = len(renda)
    populacao_acumulada = np.arange(1, n + 1) / n
    parte = int(n * 0.8)
    menores_80 = renda.iloc[:parte]
    # print(menores_80)
    maior20 = renda.iloc[parte:]
    media80 = menores_80.mean()
    media20 = maior20.mean()
    mediana80 = menores_80.median()
    mediana20 = maior20.median()

    print(f"Razão 80/20: {menores_80.sum() / maior20.sum()}")
    rel20tot = maior20.sum() / renda.sum()
    rel80tot = menores_80.sum() / renda.sum()
    print(f"Relação 20% da população: {rel20tot}")
    print(f"Relação 80% da população: {rel80tot}")

    return rel20tot * 100, rel80tot * 100, media80, media20, mediana80, mediana20


def gerar_desvio_padrao(renda):
    return renda["VD4019"].std()


def gerar_tabela(renda):
    ordem_faixas = ["< 1", "1-2", "2-5", "5-10", ">= 10"]
    total_entradas = len(renda)
    nova_tabela = renda["Faixa_renda"].value_counts()

    nova_tabela = nova_tabela.to_frame()
    nova_tabela = nova_tabela.reindex(ordem_faixas)
    nova_tabela["Percentual acumulado"] = (renda["Faixa_renda"].value_counts()).cumsum()
    nova_tabela["Valores_Absolutos"] = (
        renda["Faixa_renda"].value_counts() / total_entradas
    ) * 100
    nova_tabela["Val. Relativos Acumulados (%)"] = nova_tabela["Valores_Absolutos"].cumsum()

    nova_tabela = nova_tabela.rename(
        columns={nova_tabela.columns[1]: "Val. Absolutos Acumulados"}
    )
    nova_tabela = nova_tabela.rename(columns={nova_tabela.columns[2]: "Freq. Relativa (%)"})
    nova_tabela["Freq. Relativa (%)"] = nova_tabela["Freq. Relativa (%)"].apply(
        lambda x: round(x, 2)
    )
    nova_tabela["Val. Relativos Acumulados (%)"] = nova_tabela[
        "Val. Relativos Acumulados (%)"
    ].apply(lambda x: round(x, 2))
    nova_tabela = nova_tabela.rename(
        columns={nova_tabela.columns[0]: "Valores Absolutos"}
    )
    nova_tabela = nova_tabela.reindex(ordem_faixas)
    print(nova_tabela.head())
    return nova_tabela


def gerar_todos_os_dados(renda):
    media_renda = media(renda)

    mediana_renda = mediana(renda)

    renda_acumulada, populacao_acumulada = lorenz(renda)

    i_gini = indice_gini(renda_acumulada, populacao_acumulada)

    renda_acumulada = np.insert(renda_acumulada, 0, 0)
    populacao_acumulada = np.insert(populacao_acumulada, 0, 0)
    return media_renda, mediana_renda, i_gini, renda_acumulada, populacao_acumulada





sm = 1320.00


df, meta = pyreadstat.read_sav("ceara_pnad.sav")

print(df.columns)
renda_filtrada = df[(df["VD4019"] >= 0) & (df["V2009"] > 20)]
renda_filtrada_masc = df[(df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V2007"] == 1)]
renda_filtrada_fem = df[(df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V2007"] == 2)]

renda_filtrada_baixo = df[(df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V3009A"] < 9)]
renda_filtrada_medio = df[
    (df["VD4019"] >= 0)
    & (df["V2009"] > 20)
    & ((df["V3009A"] >= 9) & (df["V3009A"] < 12))
]
renda_filtrada_alto = df[
    (df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V3009A"] >= 12)
]
renda_filtrada_branco = df[(df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V2010"] == 1)]
renda_filtrada_pardo = df[(df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V2010"] == 4)]
renda_filtrada_pai = df[(df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V2010"] != 1) & (df["V2010"] != 4)]

renda_filtrada_rural = df[(df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V1022"] == 2)]
renda_filtrada_urbana = df[(df["VD4019"] >= 0) & (df["V2009"] > 20) & (df["V1022"] == 1)]

renda_filtrada_rural["Faixa_renda"] = filtrar_renda(renda_filtrada_rural)
renda_filtrada_urbana["Faixa_renda"] = filtrar_renda(renda_filtrada_urbana)

renda_filtrada_branco["Faixa_renda"] = filtrar_renda(renda_filtrada_branco)
renda_filtrada_pardo["Faixa_renda"] = filtrar_renda(renda_filtrada_pardo)
renda_filtrada_pai["Faixa_renda"] = filtrar_renda(renda_filtrada_pai)

renda_filtrada_alto["Faixa_renda"] = filtrar_renda(renda_filtrada_alto)
renda_filtrada_medio["Faixa_renda"] = filtrar_renda(renda_filtrada_medio)
renda_filtrada_baixo["Faixa_renda"] = filtrar_renda(renda_filtrada_baixo)

renda_filtrada_masc["Faixa_renda"] = filtrar_renda(renda_filtrada_masc)
renda_filtrada_fem["Faixa_renda"] = filtrar_renda(renda_filtrada_fem)

renda_filtrada["Faixa_renda"] = filtrar_renda(renda_filtrada)


media_renda, mediana_renda, i_gini, renda_acumulada, populacao_acumulada = gerar_todos_os_dados(renda_filtrada)


mai20, men80, media80, media20, mediana80, mediana20 = raz8020(renda_filtrada)

tamanho = len(renda_filtrada)

gerar_tabela(renda_filtrada)

# divisao_sexo(renda_filtrada)

# print("Desvio padrão: ", gerar_desvio_padrao(renda_filtrada))

print(renda_filtrada_alto.head())