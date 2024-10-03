import streamlit as st

# Definindo as páginas
pages = {
    "Geral": "nav/main.py",
    "Sexo": "nav/sexo.py",
    "Cor/raça": "nav/cor_raca.py",
    "por escolaridade": "nav/escolaridade.py",
    "Idade": "nav/idade.py",
    "Situação de domicílio": "nav/situacao_domicilio.py",
}

# Adicionando um título e texto na barra lateral    
with st.sidebar:
    st.image("assets/loco.png")
    selected = st.selectbox(
        "Distribuição de renda por:",
        list(pages.keys())
    )

st.markdown(
    """
    <style>
    img[data-testid="stLogo"] {
        height: 2.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Executando a página selecionada
page_path = pages[selected]
with open(page_path, "r", encoding="utf-8") as file:
    exec(file.read())
