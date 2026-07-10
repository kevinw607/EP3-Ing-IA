import pandas as pd

from observability.metrics import (
    MetricsManager,
    CSV_FILE
)


class Analyzer:

    def __init__(self):
        self.metrics_manager = MetricsManager()

    def load_history(self):
        """
        Carga el historial de ejecuciones desde el archivo CSV.
        """

        try:
            return pd.read_csv(CSV_FILE)

        except FileNotFoundError:
            return pd.DataFrame()

    def get_metrics(self):
        """
        Obtiene el resumen de métricas generales.
        """

        return self.metrics_manager.summary()

    def total_requests(self):

        return self.metrics_manager.load()["total_requests"]

    def successful_requests(self):

        return self.metrics_manager.load()["successful_requests"]

    def total_errors(self):

        return self.metrics_manager.load()["errors"]

    def success_rate(self):

        return self.metrics_manager.success_rate()

    def error_rate(self):

        return self.metrics_manager.error_rate()

    def average_latency(self):

        return self.metrics_manager.load()["average_latency"]

    def min_latency(self):

        return self.metrics_manager.load()["min_latency"]

    def max_latency(self):

        return self.metrics_manager.load()["max_latency"]

    def average_cpu(self):

        history = self.load_history()

        if history.empty:
            return 0

        return round(history["cpu"].mean(), 2)

    def average_memory(self):

        history = self.load_history()

        if history.empty:
            return 0

        return round(history["memory"].mean(), 2)

    def slow_requests(self, threshold=2):

        history = self.load_history()

        if history.empty:
            return pd.DataFrame()

        return history[
            history["latency"] > threshold
        ]

    def slow_request_count(self, threshold=2):

        return len(
            self.slow_requests(threshold)
        )

    def failed_requests(self):

        history = self.load_history()

        if history.empty:
            return pd.DataFrame()

        return history[
            history["status"] == "ERROR"
        ]

    def most_used_tool(self):

        metrics = self.metrics_manager.load()

        tool_calls = metrics["tool_calls"]

        if len(tool_calls) == 0:
            return None

        return max(
            tool_calls,
            key=tool_calls.get
        )

    def tool_with_most_errors(self):

        metrics = self.metrics_manager.load()

        tool_errors = metrics["tool_errors"]

        if len(tool_errors) == 0:
            return None

        return max(
            tool_errors,
            key=tool_errors.get
        )

    def bottlenecks(self):

        bottlenecks = []

        if self.average_latency() > 2:
            bottlenecks.append(
                "Alta latencia promedio."
            )

        if self.error_rate() > 20:
            bottlenecks.append(
                "Alta tasa de errores."
            )

        if self.average_cpu() > 80:
            bottlenecks.append(
                "Uso elevado de CPU."
            )

        if self.average_memory() > 80:
            bottlenecks.append(
                "Uso elevado de memoria RAM."
            )

        if len(bottlenecks) == 0:
            bottlenecks.append(
                "No se detectaron cuellos de botella."
            )

        return bottlenecks

    def summary(self):

        return {

            "total_requests":
                self.total_requests(),

            "successful_requests":
                self.successful_requests(),

            "errors":
                self.total_errors(),

            "success_rate":
                self.success_rate(),

            "error_rate":
                self.error_rate(),

            "average_latency":
                self.average_latency(),

            "min_latency":
                self.min_latency(),

            "max_latency":
                self.max_latency(),

            "average_cpu":
                self.average_cpu(),

            "average_memory":
                self.average_memory(),

            "slow_requests":
                self.slow_request_count(),

            "most_used_tool":
                self.most_used_tool(),

            "tool_with_most_errors":
                self.tool_with_most_errors(),

            "bottlenecks":
                self.bottlenecks()
        }