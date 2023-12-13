from celery import Celery


celery = Celery("tasks", broker="redis://localhost", include=["app.tasks.task"])
