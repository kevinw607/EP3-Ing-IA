from dotenv import load_dotenv
load_dotenv()

import os

from agent.orchestrator import OrganizationalAgent


def main():

    if not os.getenv("GOOGLE_API_KEY"):

        print(
            "❌ Error: No se encontró GOOGLE_API_KEY "
            "en el archivo .env"
        )

        return

    print("🚀 Inicializando Agente Autónomo SAEAC...")

    try:

        agente = OrganizationalAgent()

        print("\n--- EJECUTANDO ESCENARIO 1 (600 USD) ---")

        caso_1 = (
            "Revisa el procedimiento de compras, "
            "analiza un gasto de 600 USD "
            "y genera un reporte."
        )

        print(f"Usuario: {caso_1}")

        respuesta_1 = agente.ejecutar(caso_1)

        print(f"Agente: {respuesta_1}")

        print("\n--- EJECUTANDO ESCENARIO 2 (300 USD) ---")

        caso_2 = (
            "Llegó otra solicitud por un gasto de "
            "300 USD. ¿Se requiere reporte?"
        )

        print(f"Usuario: {caso_2}")

        respuesta_2 = agente.ejecutar(caso_2)

        print(f"Agente: {respuesta_2}")

    except Exception as e:

        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()