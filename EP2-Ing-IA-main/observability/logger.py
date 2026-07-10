import json
import logging
import os
from datetime import datetime

LOG_JSON = "logs/execution_log.json"
LOG_TXT = "logs/agent.log"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_TXT,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)


class Logger:

    @staticmethod
    def log(event):

        if os.path.exists(LOG_JSON):

            with open(
                LOG_JSON,
                "r",
                encoding="utf-8"
            ) as file:

                try:
                    logs = json.load(file)
                except json.JSONDecodeError:
                    logs = []

        else:

            logs = []

        event["timestamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        logs.append(event)

        with open(
            LOG_JSON,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                logs,
                file,
                indent=4,
                ensure_ascii=False
            )


def log_info(message):

    logging.info(message)

    Logger.log({

        "level": "INFO",

        "message": message

    })


def log_warning(message):

    logging.warning(message)

    Logger.log({

        "level": "WARNING",

        "message": message

    })


def log_error(message):

    logging.error(message)

    Logger.log({

        "level": "ERROR",

        "message": message

    })