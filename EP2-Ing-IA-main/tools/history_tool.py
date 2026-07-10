from langchain_core.tools import tool
from memory.semantic_memory import SemanticMemory

_casos_compartidos = SemanticMemory()
_casos_compartidos.cargar_documentos()

@tool
def consultar_historial_casos(query: str) -> str:
    """Recupera casos similares y auditorías previas previamente procesados en la organización."""
    return _casos_compartidos.buscar(query, k=2)