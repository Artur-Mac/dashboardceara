import streamlit as st
import sys

# Insira o caminho absoluto do módulo streamlit_option_menu
sys.path.insert(1, "C:\Users\Artur\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\streamlit_option_menu\__init__.py")

from streamlit_option_menu import option_menu

# Configurando a página
st.set_page_config(layout="wide", page_icon="assets/icone.png")

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
    st.logo("assets/loco.png")
    selected = option_menu(
        "Distribuição de renda por:",
        list(pages.keys()),
        icons=[],
        menu_icon="",
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
