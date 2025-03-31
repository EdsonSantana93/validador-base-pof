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

def _initialize_session_state(selected_layout: dict, selected_layout_name: str) -> None:
    """Inicializa o st.session_state com os dados do layout selecionado."""
    if "base_data" not in st.session_state or st.session_state.get("last_selected_layout") != selected_layout_name:
        st.session_state.base_data = {
            "Atributo": list(selected_layout["validacoes"].keys()),
            "Regras": list(selected_layout["validacoes"].values()),
        }
        st.session_state.last_selected_layout = selected_layout_name

def _display_edit_layout_form(layouts: list, selected_layout_name: str) -> str:
    """Exibe o formulário para editar o nome do layout."""
    st.subheader("Nome do Layout")
    new_layout_name = st.text_input(
        "Defina um novo nome (se necessário)",
        placeholder="Ex: Layout de Lançamento XYZ",
        value=selected_layout_name,
        key="new_layout_name",
    )
    if new_layout_name in [layout["nome"] for layout in layouts["layouts"]] and new_layout_name != selected_layout_name:
        st.error("⚠️ Já existe um layout com esse nome.")
    return new_layout_name

def edit_layout_view() -> None:
    """Exibe a interface para editar um layout de validação."""
    st.title("✏️ Alterar Layout de Validação")
    st.markdown("---")

    layouts = load_validation_layouts()
    editable_layouts = [layout["nome"] for layout in layouts["layouts"] if layout.get("modificavel", True)]

    if not editable_layouts:
        st.error("⚠️ Nenhum layout disponível para edição.")
        return

    selected_layout_name = st.selectbox("Selecione um layout para editar", editable_layouts, key="selected_layout")
    selected_layout = get_layout_by_name(layouts, selected_layout_name)
    default_layout = get_layout_by_name(layouts, "default_lancamento")

    if not selected_layout:
        st.error("❌ O layout selecionado não foi encontrado.")
        return

    _initialize_session_state(selected_layout, selected_layout_name)

    new_layout_name = _display_edit_layout_form(layouts, selected_layout_name)

    st.markdown("---")
    st.subheader("➕ Adicionar ou Atualizar Atributo")
    display_attribute_form(st.session_state.base_data, selected_layout)

    display_attribute_table(st.session_state.base_data)

    if any(attr not in default_layout["validacoes"] for attr in st.session_state.base_data["Atributo"]):
        save, delete_selected = display_delete_attributes(st.session_state.base_data, default_layout)

        if delete_selected:
            delete_selected_attributes(st.session_state.base_data)

        if save:
            if save_layout(layouts, new_layout_name, st.session_state.base_data, selected_layout):
                for key in ["new_layout_name", "new_attribute", "selected_rules", "excluir_atributos"]:
                    st.session_state.pop(key, None)
                time.sleep(2)
                st.rerun()
    else:
        save = st.button("Salvar Alterações", type="primary", use_container_width=True)
        if save:
            if save_layout(layouts, new_layout_name, st.session_state.base_data, selected_layout):
                for key in ["new_layout_name", "new_attribute", "selected_rules", "excluir_atributos"]:
                    st.session_state.pop(key, None)
                time.sleep(2)
                st.rerun()

if __name__ == "__main__":
    edit_layout_view()