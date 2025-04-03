import streamlit as st
from services.validation_service import load_validation_layouts
from views.layouts import layout_view, create_new_layout_view, edit_layout_view
import config.styles.styles as styles

def _clear_session_state_if_option_changed(selected_option: str) -> None:
    """Limpa o st.session_state se a opção selecionada mudar."""
    if "last_option" not in st.session_state:
        st.session_state.last_option = selected_option
    elif st.session_state.last_option != selected_option:
        for key in list(st.session_state.keys()): # Usar list para evitar erros de dicionário durante a iteração
            if key != "last_option":
                del st.session_state[key]
        st.session_state.last_option = selected_option

def _display_selected_layout_option(selected_option: str) -> None:
    """Exibe a interface correspondente à opção de layout selecionada."""
    if selected_option == "Visualizar Layouts":
        layout_view.display_layouts_view()
    elif selected_option == "Criar Novo Layout":
        create_new_layout_view.create_new_layout_view() # chamada corrigida
    elif selected_option == "Editar Layout":
        edit_layout_view.edit_layout_view()

def main() -> None:
    """Função principal para gerenciar layouts de validação."""
    styles.load_css()
    st.title("Gerenciamento de Layouts de Validação")

    layout_option = st.radio(
        "Escolha uma opção:",
        ["Visualizar Layouts", "Criar Novo Layout", "Editar Layout"],
        horizontal=True,
    )

    _clear_session_state_if_option_changed(layout_option)
    _display_selected_layout_option(layout_option)

if __name__ == "__main__":
    main()