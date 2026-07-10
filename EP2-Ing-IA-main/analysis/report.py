import json
import os
from datetime import datetime

from analysis.analyzer import Analyzer
from analysis.recommendations import Recommendations

REPORTS_FOLDER = "reports"


class ReportGenerator:

    def __init__(self):

        self.analyzer = Analyzer()
        self.recommendations = Recommendations()

        os.makedirs(
            REPORTS_FOLDER,
            exist_ok=True
        )

    def build(self):

        report = {

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "summary":
                self.analyzer.summary(),

            "recommendations":
                self.recommendations.generate()

        }

        return report

    def save(self):

        report = self.build()

        filename = datetime.now().strftime(
            "report_%Y%m%d_%H%M%S.json"
        )

        filepath = os.path.join(
            REPORTS_FOLDER,
            filename
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        return filepath

    def print(self):

        report = self.build()

        print("\n")
        print("=" * 60)
        print("REPORTE DE OBSERVABILIDAD")
        print("=" * 60)

        print(
            f"\nFecha: {report['generated_at']}"
        )

        print("\nMÉTRICAS\n")

        for key, value in report["summary"].items():

            print(f"{key}: {value}")

        print("\nRECOMENDACIONES\n")

        for recommendation in report["recommendations"]:

            print(
                f"[{recommendation['priority']}] "
                f"{recommendation['category']}"
            )

            print(
                recommendation["message"]
            )

            print("-" * 60)

        print("\nFin del reporte\n")