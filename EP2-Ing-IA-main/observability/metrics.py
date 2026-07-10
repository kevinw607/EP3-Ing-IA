import csv
import json
import os
from datetime import datetime

METRICS_FILE = "logs/metrics.json"
CSV_FILE = "logs/execution_history.csv"

DEFAULT_METRICS = {
    "total_requests": 0,
    "successful_requests": 0,
    "errors": 0,
    "knowledge_queries": 0,
    "approval_requests": 0,
    "reports_generated": 0,
    "average_latency": 0,
    "min_latency": 0,
    "max_latency": 0,
    "total_latency": 0,
    "tool_calls": {},
    "tool_errors": {}
}


class MetricsManager:

    def __init__(self):

        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(METRICS_FILE):
            self.save(DEFAULT_METRICS)

        if not os.path.exists(CSV_FILE):

            with open(
                CSV_FILE,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "question",
                    "latency",
                    "cpu",
                    "memory",
                    "status"
                ])

    def load(self):

        with open(
            METRICS_FILE,
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save(self, metrics):

        with open(
            METRICS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metrics,
                file,
                indent=4
            )

    def increment(self, key):

        metrics = self.load()

        if key in metrics:
            metrics[key] += 1

        self.save(metrics)

    def add_tool_usage(self, tool):

        metrics = self.load()

        if tool not in metrics["tool_calls"]:
            metrics["tool_calls"][tool] = 0

        metrics["tool_calls"][tool] += 1

        self.save(metrics)

    def add_tool_error(self, tool):

        metrics = self.load()

        if tool not in metrics["tool_errors"]:
            metrics["tool_errors"][tool] = 0

        metrics["tool_errors"][tool] += 1

        self.save(metrics)

    def update_latency(self, latency):

        metrics = self.load()

        metrics["total_latency"] += latency

        total = metrics["total_requests"]

        if total > 0:
            metrics["average_latency"] = (
                metrics["total_latency"] / total
            )

        if metrics["min_latency"] == 0:
            metrics["min_latency"] = latency
        else:
            metrics["min_latency"] = min(
                metrics["min_latency"],
                latency
            )

        metrics["max_latency"] = max(
            metrics["max_latency"],
            latency
        )

        self.save(metrics)

    def save_execution(
        self,
        question,
        latency,
        cpu,
        memory,
        status
    ):

        with open(
            CSV_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                question,
                round(latency, 3),
                cpu,
                memory,
                status
            ])

    def success_rate(self):

        metrics = self.load()

        if metrics["total_requests"] == 0:
            return 0

        return round(
            (
                metrics["successful_requests"]
                / metrics["total_requests"]
            ) * 100,
            2
        )

    def error_rate(self):

        metrics = self.load()

        if metrics["total_requests"] == 0:
            return 0

        return round(
            (
                metrics["errors"]
                / metrics["total_requests"]
            ) * 100,
            2
        )

    def summary(self):

        metrics = self.load()

        return {

            "total_requests":
                metrics["total_requests"],

            "successful_requests":
                metrics["successful_requests"],

            "errors":
                metrics["errors"],

            "knowledge_queries":
                metrics["knowledge_queries"],

            "approval_requests":
                metrics["approval_requests"],

            "reports_generated":
                metrics["reports_generated"],

            "average_latency":
                round(metrics["average_latency"], 3),

            "min_latency":
                round(metrics["min_latency"], 3),

            "max_latency":
                round(metrics["max_latency"], 3),

            "success_rate":
                self.success_rate(),

            "error_rate":
                self.error_rate(),

            "tool_calls":
                metrics["tool_calls"],

            "tool_errors":
                metrics["tool_errors"]
        }

    def reset(self):

        self.save(DEFAULT_METRICS)

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "question",
                "latency",
                "cpu",
                "memory",
                "status"
            ])