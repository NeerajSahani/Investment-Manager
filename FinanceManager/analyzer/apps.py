from django.apps import AppConfig


class AnalyzerConfig(AppConfig):
    name = 'analyzer'

    def ready(self):
        from analyzer.task_scheduler import start
        start()
