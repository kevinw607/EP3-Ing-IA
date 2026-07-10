from datetime import datetime
import os

from langchain_core.tools import tool

from observability.metrics import MetricsManager


@tool
def registrar_reporte_local(
    contenido: str,
    nombre_archivo: str
) -> str:
    """
    Genera reportes locales para auditoría.
    """

    carpeta = "data/reports"

    os.makedirs(carpeta, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta = os.path.join(
        carpeta,
        f"{timestamp}_{nombre_archivo}"
    )

    try:

        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as archivo:

            archivo.write(contenido)

        # Actualizar métricas de observabilidad
        MetricsManager().increment("reports_generated")

        return (
            f"Reporte generado correctamente: {ruta}"
        )

    except Exception as e:

        return (
            f"Error generando reporte: {str(e)}"
        )