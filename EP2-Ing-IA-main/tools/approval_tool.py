from langchain_core.tools import tool


@tool
def evaluar_solicitud_compra(monto: float) -> str:
    """
    Evalúa automáticamente una solicitud
    de compra según reglas corporativas.
    """

    if monto > 500:

        return (
            "REQUIERE_APROBACION_FINANZAS"
        )

    return (
        "APROBACION_AUTOMATICA"
    )