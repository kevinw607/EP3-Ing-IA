import os
import time

import psutil


class ResourceMonitor:
    """
    Monitorea el consumo de recursos del proceso del agente.
    """

    def __init__(self):

        self.process = psutil.Process(os.getpid())

        self.start_time = time.time()

    def get_cpu_percent(self):
        """
        Retorna el porcentaje de CPU utilizado.
        """

        return psutil.cpu_percent(interval=0.1)

    def get_memory_mb(self):
        """
        Retorna la memoria utilizada por el proceso en MB.
        """

        memory = self.process.memory_info().rss

        return round(
            memory / (1024 * 1024),
            2
        )

    def get_memory_percent(self):
        """
        Retorna el porcentaje de memoria RAM utilizada
        por todo el sistema.
        """

        return round(
            psutil.virtual_memory().percent,
            2
        )

    def get_cpu_count(self):
        """
        Retorna la cantidad de núcleos disponibles.
        """

        return psutil.cpu_count()

    def get_uptime(self):
        """
        Retorna el tiempo que lleva ejecutándose
        el agente (segundos).
        """

        return round(
            time.time() - self.start_time,
            2
        )

    def snapshot(self):
        """
        Devuelve una captura instantánea de recursos.
        """

        return {

            "cpu_percent":
                self.get_cpu_percent(),

            "memory_mb":
                self.get_memory_mb(),

            "memory_percent":
                self.get_memory_percent(),

            "cpu_count":
                self.get_cpu_count(),

            "uptime":
                self.get_uptime()
        }