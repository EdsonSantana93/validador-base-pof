import streamlit as st
import time
from services.validation_service import load_validation_layouts
from views.layouts.form_layout import (
    get_layout_by_name,
    display_attribute_form,
    display_attribute_table,
    display_delete_attributes,
    delete_selected_attributes,
    save_layout,
)

def _initialize_session_state(default_layout: dict) -> None:
    """Inicializa o st.session_state com os dados iniciais."""
    if "base_data" not in st.session_state:
        st.session_state.base_data = {
            "Atributo": list(default_layout["validacoes"].keys()),
            "Regras": list(default_layout["validacoes"].values()),
        }
    if "new_layout_name" not in st.session_state:
        st.session_state.new_layout_name = ""

def _display_new_layout_form(layouts: list) -> str:
    """Exibe o formulário para definir o nome do novo layout."""
    st.subheader("📝 Nome do Novo Layout")
    new_layout_name = st.text_input(
        "Defina um nome único",
        placeholder="Ex: Layout de Lançamento XYZ",
        value=st.session_state.new_layout_name,
        key="new_layout_name",
    )
    if new_layout_name in [layout["nome"] for layout in layouts["layouts"]]:
        st.error("⚠️ Já existe um layout com esse nome.")
    return new_layout_name

def create_new_layout_view() -> None:
    """Exibe a interface para criar um novo layout de validação."""
    st.title("📌 Criar Novo Layout de Validação")
    st.markdown("---")

    layouts = load_validation_layouts()
    default_layout = get_layout_by_name(layouts, "default_lancamento")

    if not default_layout:
        st.error("❌ Layout padrão 'default_lancamento' não encontrado!")
        return

    _initialize_session_state(default_layout)

    new_layout_name = _display_new_layout_form(layouts)

    st.markdown("---")
    st.subheader("➕ Adicionar Novo Atributo")
    display_attribute_form(st.session_state.base_data, default_layout)

    display_attribute_table(st.session_state.base_data)

    save, delete_selected = display_delete_attributes(st.session_state.base_data, default_layout)

    if delete_selected:
        delete_selected_attributes(st.session_state.base_data)

    if save:
        if save_layout(layouts, new_layout_name, st.session_state.base_data):
            st.session_state.base_data = {
                "Atributo": list(default_layout["validacoes"].keys()),
                "Regras": list(default_layout["validacoes"].values()),
            }
            for key in ["new_layout_name", "new_attribute", "selected_rules", "excluir_atributos"]:
                st.session_state.pop(key, None)
            time.sleep(2)
            st.rerun()

if __name__ == "__main__":
    create_new_layout_view()