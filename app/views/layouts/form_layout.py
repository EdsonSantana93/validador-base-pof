import streamlit as st
from services.validation_service import save_validation_layouts
from services.validation_service import load_validation_layouts
from typing import Dict, List, Optional, Tuple

def get_layout_by_name(layouts: Dict, layout_name: str) -> Optional[Dict]:
    """Retorna o layout com o nome especificado, se encontrado."""
    return next((layout for layout in layouts["layouts"] if layout["nome"] == layout_name), None)

def display_attribute_form(base_data: Dict, selected_layout: Optional[Dict], is_new_layout: bool = False) -> None:
    """Exibe o formulário para adicionar ou atualizar atributos."""
    with st.form("form_atributo", clear_on_submit=True):
        new_attribute = st.text_input("Nome do Atributo", placeholder="Ex: novo_atributo", key="new_attribute")
        available_rules = ["not_null", "numeric", "match_ph", "date_format", "lte_today", "gte_0"]
        selected_rules = st.multiselect("Regras do Atributo", options=available_rules, key="selected_rules")
        submitted = st.form_submit_button("Incluir/Atualizar Atributo", type="primary")

        if submitted:
            if not new_attribute:
                st.error("❌ O nome do atributo não pode estar vazio.")
            else:
                layouts = load_validation_layouts() # Carrega os layouts
                default_layout = get_layout_by_name(layouts, "default_lancamento") # Adicionado para obter o layout padrão

                if default_layout and new_attribute in default_layout["validacoes"]:
                    st.error(f"⚠️ O atributo '{new_attribute}' não pode ser alterado, pois faz parte do layout padrão.")
                elif new_attribute in base_data["Atributo"]:
                    if selected_layout and new_attribute in selected_layout["validacoes"]:
                        idx = base_data["Atributo"].index(new_attribute)
                        base_data["Regras"][idx] = selected_rules
                        st.success(f"✏️ Atributo '{new_attribute}' atualizado com sucesso!")
                    elif not is_new_layout:
                        st.error(f"⚠️ O atributo '{new_attribute}' não existe no layout original.")
                    else:
                        st.error(f"⚠️ O atributo '{new_attribute}' não pode ser alterado, pois faz parte do layout padrão.")
                elif is_new_layout and selected_layout and new_attribute in selected_layout["validacoes"]:
                    st.error(f"⚠️ O atributo '{new_attribute}' já existe no layout padrão.")
                elif not selected_rules:
                    st.error("⚠️ Selecione pelo menos uma regra.")
                else:
                    base_data["Atributo"].append(new_attribute)
                    base_data["Regras"].append(selected_rules)
                    st.success(f"✅ Atributo '{new_attribute}' adicionado com sucesso!")
            st.rerun()
                
def display_attribute_table(base_data: Dict) -> None:
    """Exibe a tabela de atributos e regras."""
    st.write("### 📊 Atributos e Regras:")
    st.dataframe(base_data, use_container_width=True)

def display_delete_attributes(base_data: Dict, default_layout: Optional[Dict]) -> Tuple[bool, bool]:
    """Exibe a seção para excluir atributos."""
    if default_layout:
        new_attributes = [attr for attr in base_data["Atributo"] if attr not in default_layout["validacoes"]]
    else:
        new_attributes = base_data["Atributo"]

    if new_attributes:
        st.markdown("---")
        st.subheader("🗑️ Excluir Atributos Novos")
        attributes_to_delete = st.multiselect("Selecione os atributos para excluir", options=new_attributes, key="excluir_atributos")

        col1, col2 = st.columns([3, 1])
        with col1:
            save = st.button("💾 Salvar Layout", type="primary", use_container_width=True)
        with col2:
            delete_selected = st.button("🗑️ Excluir", use_container_width=True)
    else:
        save = st.button("💾 Salvar Layout", type="primary", use_container_width=True)
        delete_selected = False

    return save, delete_selected

def delete_selected_attributes(base_data: Dict) -> None:
    """Exclui os atributos selecionados."""
    for attr in st.session_state.get("excluir_atributos", []):
        idx = base_data["Atributo"].index(attr)
        del base_data["Atributo"][idx]
        del base_data["Regras"][idx]
    st.success("✅ Atributos excluídos com sucesso!")
    st.rerun()

def save_layout(layouts: Dict, new_layout_name: str, base_data: Dict, selected_layout: Optional[Dict] = None) -> bool:
    """Salva o layout no arquivo JSON."""
    if not new_layout_name:
        st.error("❌ O nome do layout não pode ficar vazio.")
        return False

    # Validação aplicada para criação e alteração de layouts
    default_layout = get_layout_by_name(layouts, "default_lancamento")
    if default_layout and all(attr in default_layout["validacoes"] for attr in base_data["Atributo"]):
        st.error("⚠️ O layout deve conter pelo menos um atributo diferente do layout padrão.")
        return False

    new_layout = {
        "nome": new_layout_name,
        "tipo": selected_layout["tipo"] if selected_layout else "lancamento",
        "modificavel": selected_layout["modificavel"] if selected_layout else True,
        "validacoes": dict(zip(base_data["Atributo"], base_data["Regras"]))
    }

    if selected_layout:
        for i, layout in enumerate(layouts["layouts"]):
            if layout["nome"] == selected_layout["nome"]:
                layouts["layouts"][i] = new_layout
                break
    else:
        layouts["layouts"].append(new_layout)

    save_validation_layouts(layouts)
    st.success(f" Layout '{new_layout_name}' {'atualizado' if selected_layout else 'criado'} com sucesso!")
    st.balloons()
    return True
