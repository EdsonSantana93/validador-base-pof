import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Caminho para o arquivo de layouts de validação
_LAYOUTS_FILE_PATH = 'app/config/validation_layouts.json'

def load_validation_layouts() -> Dict:
    """Carrega os layouts de validação do arquivo JSON.

    Returns:
        Um dicionário contendo os layouts de validação.
    """
    if not os.path.exists(_LAYOUTS_FILE_PATH):
        return {"layouts": []}  # Se o arquivo não existir, retorna um dicionário com uma lista vazia de layouts

    with open(_LAYOUTS_FILE_PATH, 'r') as file:
        return json.load(file)

def save_validation_layouts(layouts: Dict) -> None:
    """Salva os layouts de validação no arquivo JSON.

    Args:
        layouts: Um dicionário contendo os layouts de validação.
    """
    with open(_LAYOUTS_FILE_PATH, 'w') as file:
        json.dump(layouts, file, indent=4, ensure_ascii=False)

def _find_default_launch_layout(layouts: List[Dict]) -> Optional[Dict]:
    """Encontra o layout padrão de lançamento na lista de layouts.

    Args:
        layouts: Uma lista de dicionários contendo os layouts.

    Returns:
        O layout padrão de lançamento, se encontrado, caso contrario None.
    """
    return next(
        (layout for layout in layouts if layout.get('tipo') == 'default_lancamento'),
        None,
    )

def is_valid_new_layout(new_layout_name: str, layouts: Dict) -> bool:
    """Valida se um novo layout de lançamento é válido.

    Args:
        new_layout_name: O nome do novo layout.
        layouts: Um dicionário contendo os layouts existentes.

    Returns:
        True se o novo layout for válido, False caso contrário.
    """
    existing_layouts = layouts.get("layouts", [])
    default_layout = _find_default_launch_layout(existing_layouts)

    if not default_layout:
        return False  # Retorna False se não encontrar um layout do tipo 'default_lancamento'

    # Outras lógicas para validação podem continuar aqui...

    return True

def generate_new_layout(layout_name: str, layout_type: str, validations: Dict) -> Dict:
    """Gera um novo layout de validação.

    Args:
        layout_name: O nome do layout.
        layout_type: O tipo do layout.
        validations: Um dicionário contendo as validações do layout.

    Returns:
        Um dicionário contendo o novo layout gerado.
    """
    return {
        "name": layout_name,
        "type": layout_type,
        "validations": validations,
        "created_at": datetime.now().isoformat()
    }