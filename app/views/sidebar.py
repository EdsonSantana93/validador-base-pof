import streamlit as st

def page2():
    st.title("Second page")

def carregar_sidebar():
    # Caminho para o logo salvo localmente
    logo_path = "app/assets/images/logo-itau.png"

    # Exibir o logo no topo da sidebar
    st.logo(logo_path, size="large")

    # Adicionar título abaixo do logo
    st.sidebar.title("Título do Seu Projeto")

    # Navegação
    pg = st.navigation({"Menu": ["pages/layout_manager.py", "pages/teste.py"]})
    pg.run()

if __name__ == "__main__":
    carregar_sidebar()