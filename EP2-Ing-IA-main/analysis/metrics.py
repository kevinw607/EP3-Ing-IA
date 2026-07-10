import time

class Metrics:

    @staticmethod
    def accuracy(correct, total):
        if total == 0:
            return 0
        return round((correct / total) * 100, 2)

    @staticmethod
    def latency(start_time, end_time):
        return round(end_time - start_time, 3)

    @staticmethod
    def error_rate(errors, total):
        if total == 0:
            return 0
        return round((errors / total) * 100, 2)

    @staticmethod
    def consistency(successes, total):
        if total == 0:
            return 0
        return round((successes / total) * 100, 2)