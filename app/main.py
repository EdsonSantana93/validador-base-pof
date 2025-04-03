# main.py

import streamlit as st
import config.styles.styles as styles
from views.sidebar import carregar_sidebar

def main():
    #styles.load_css()
    carregar_sidebar()  # Carrega o logo na sidebar

if __name__ == "__main__":
    main()