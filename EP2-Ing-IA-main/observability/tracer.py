import time

from observability.logger import (
    log_info,
    log_error
)


class Trace:
    """
    Context manager para medir el tiempo de ejecución
    de una etapa del agente.
    """

    def __init__(self, name):

        self.name = name

        self.start = None

        self.end = None

        self.duration = 0

    def __enter__(self):

        self.start = time.perf_counter()

        log_info(
            f"Iniciando etapa: {self.name}"
        )

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        self.end = time.perf_counter()

        self.duration = (
            self.end - self.start
        )

        if exc_type is None:

            log_info(
                f"{self.name} finalizada "
                f"en {self.duration:.3f} segundos"
            )

        else:

            log_error(
                f"Error en {self.name}: "
                f"{exc_value}"
            )

        print(
            f"[TRACE] "
            f"{self.name}: "
            f"{self.duration:.3f}s"
        )

        return False