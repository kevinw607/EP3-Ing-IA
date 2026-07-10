from langchain_core.tools import tool
from memory.semantic_memory import SemanticMemory

_memoria_compartida = SemanticMemory()
_memoria_compartida.cargar_documentos()

@tool
def consultar_base_conocimiento(query: str) -> str:
    """Busca información organizacional y procedimientos operativos utilizando memoria semántica FAISS."""
    return _memoria_compartida.buscar(query, k=3)