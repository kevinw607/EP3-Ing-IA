from analysis.analyzer import Analyzer


class Recommendations:

    def __init__(self):
        self.analyzer = Analyzer()

    def generate(self):

        summary = self.analyzer.summary()

        recommendations = []

        # Latencia
        if summary["average_latency"] > 2:
            recommendations.append({
                "category": "Latencia",
                "priority": "Alta",
                "message": (
                    "La latencia promedio supera los 2 segundos. "
                    "Se recomienda optimizar las herramientas, "
                    "reducir llamadas innecesarias al modelo "
                    "o implementar caché."
                )
            })

        # Errores
        if summary["error_rate"] > 10:
            recommendations.append({
                "category": "Errores",
                "priority": "Alta",
                "message": (
                    "La tasa de errores es elevada. "
                    "Revise las excepciones registradas "
                    "y fortalezca el manejo de errores."
                )
            })

        # CPU
        if summary["average_cpu"] > 80:
            recommendations.append({
                "category": "CPU",
                "priority": "Media",
                "message": (
                    "El consumo de CPU es alto. "
                    "Optimice algoritmos o distribuya la carga."
                )
            })

        # RAM
        if summary["average_memory"] > 80:
            recommendations.append({
                "category": "Memoria",
                "priority": "Media",
                "message": (
                    "El consumo de memoria RAM es elevado. "
                    "Libere recursos o reduzca el tamaño "
                    "de los objetos mantenidos en memoria."
                )
            })

        # Consultas lentas
        if summary["slow_requests"] > 0:
            recommendations.append({
                "category": "Rendimiento",
                "priority": "Media",
                "message": (
                    f"Se detectaron {summary['slow_requests']} "
                    "consultas lentas. "
                    "Analice esos casos para identificar "
                    "cuellos de botella."
                )
            })

        # Herramienta con errores
        if summary["tool_with_most_errors"] is not None:
            recommendations.append({
                "category": "Herramientas",
                "priority": "Media",
                "message": (
                    f"La herramienta "
                    f"'{summary['tool_with_most_errors']}' "
                    "presenta la mayor cantidad de errores. "
                    "Revise su implementación."
                )
            })

        # Sin problemas detectados
        if len(recommendations) == 0:
            recommendations.append({
                "category": "General",
                "priority": "Baja",
                "message": (
                    "No se detectaron problemas relevantes. "
                    "El agente presenta un comportamiento estable."
                )
            })

        return recommendations

    def print_report(self):

        recommendations = self.generate()

        print("\n========== RECOMENDACIONES ==========\n")

        for recommendation in recommendations:

            print(
                f"[{recommendation['priority']}] "
                f"{recommendation['category']}"
            )

            print(
                recommendation["message"]
            )

            print("-" * 60)