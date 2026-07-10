class HealthStatus:

    def __init__(self, summary):

        self.summary = summary

    def evaluate(self):

        score = 100

        reasons = []

        # -----------------------
        # Latencia
        # -----------------------

        if self.summary["average_latency"] > 5:

            score -= 30

            reasons.append(
                "Latencia muy elevada."
            )

        elif self.summary["average_latency"] > 2:

            score -= 15

            reasons.append(
                "Latencia superior al recomendado."
            )

        # -----------------------
        # CPU
        # -----------------------

        if self.summary["average_cpu"] > 90:

            score -= 25

            reasons.append(
                "Uso crítico de CPU."
            )

        elif self.summary["average_cpu"] > 70:

            score -= 10

            reasons.append(
                "Uso elevado de CPU."
            )

        # -----------------------
        # Memoria
        # -----------------------

        if self.summary["average_memory"] > 90:

            score -= 25

            reasons.append(
                "Uso crítico de memoria."
            )

        elif self.summary["average_memory"] > 75:

            score -= 10

            reasons.append(
                "Uso elevado de memoria."
            )

        # -----------------------
        # Errores
        # -----------------------

        if self.summary["error_rate"] > 20:

            score -= 30

            reasons.append(
                "Alta tasa de errores."
            )

        elif self.summary["error_rate"] > 5:

            score -= 10

            reasons.append(
                "Se detectaron errores."
            )

        score = max(score, 0)

        if score >= 85:

            status = "🟢 Saludable"

        elif score >= 60:

            status = "🟡 Atención"

        else:

            status = "🔴 Crítico"

        return {

            "status": status,

            "score": score,

            "reasons": reasons

        }