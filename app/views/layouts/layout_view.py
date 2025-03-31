import streamlit as st
import pandas as pd
import time
from services.validation_service import load_validation_layouts, save_validation_layouts
from typing import Dict, List

def _delete_layout(layout_name: str, layouts: Dict) -> None:
    """Exclui um layout e atualiza a interface."""
    layouts["layouts"] = [layout for layout in layouts["layouts"] if layout["nome"] != layout_name]
    save_validation_layouts(layouts)
    st.toast(f"Layout '{layout_name}' excluído com sucesso! 🗑️")
    time.sleep(2)
    st.rerun()

def _render_layout_details(layout: Dict, layouts: Dict) -> None:
    """Exibe os detalhes de um layout dentro de um expander."""
    layout_name = layout["nome"]
    layout_type = layout["tipo"]

    with st.expander(f"🔹 **{layout_name}** - Tipo: `{layout_type}`"):
        st.markdown("### 📑 Atributos e Regras")

        df = pd.DataFrame({
            "Atributo": list(layout["validacoes"].keys()),
            "Regras": list(layout["validacoes"].values())
        })

        st.data_editor(
            df,
            key=layout_name,
            column_config={
                "Regras": st.column_config.ListColumn("🛠 Regras", help="Lista de regras aplicadas ao atributo")
            },
            hide_index=True,
            disabled=["Atributo"],
            use_container_width=True
        )

        if layout_name not in ('default_lancamento', 'default_saldo'):
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"🗑️ Excluir", key=f"excluir_{layout_name}"):
                    _delete_layout(layout_name, layouts)

def display_layouts_view() -> None:
    """Exibe a tela de visualização de layouts existentes."""
    st.title("📋 Visualização de Layouts de Validação")

    layouts = load_validation_layouts()
    st.write("Explore os layouts de validação existentes abaixo. Clique para expandir e visualizar os detalhes de cada layout.")

    if not layouts or not layouts.get("layouts"):
        st.warning("⚠ Nenhum layout foi criado até o momento.")
    else:
        for layout in layouts.get("layouts", []):
            _render_layout_details(layout, layouts)

if __name__ == "__main__":
    display_layouts_view()