import re


class PurchasePlanner:

    """
    Planificador de tareas organizacionales.
    """

    @staticmethod
    def extraer_monto(texto):

        patron = r"(\d+)"

        resultado = re.search(
            patron,
            texto
        )

        if resultado:
            return float(
                resultado.group(1)
            )

        return None

    @staticmethod
    def construir_plan(texto_usuario):

        plan = []

        texto_lower = texto_usuario.lower()

        if (
            "compra" in texto_lower
            or "gasto" in texto_lower
        ):
            plan.append(
                "CONSULTAR_BASE_CONOCIMIENTO"
            )

        monto = PurchasePlanner.extraer_monto(
            texto_usuario
        )

        if monto is not None:

            plan.append(
                "EVALUAR_SOLICITUD"
            )

            if monto > 500:

                plan.append(
                    "GENERAR_REPORTE"
                )

        return plan