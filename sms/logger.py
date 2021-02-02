from flask import Flask
from logging.config import dictConfig

def init_logger(app:Flask) -> None:
    with app.app_context():
        log = app.config["LOG"]

    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "incremental": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
            }
        },
        "handlers": {
            "file": {
                "level": log["LEVEL"],
                "filename": log["FILE"],
                "formatter": "default",
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": log["MAXBYTES"],
                "backupCount": log["BACKUPCOUNT"]
            },
            "console": {
                "level": log["LEVEL"],
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "werkzeug": {
                "handlers": ["file"],
                "level": log["LEVEL"],
                "propagate": True
            },
            "sms": {
                "handlers": ["file", "console"],
                "level": log["LEVEL"],
                "propagate": True
            }
        }
    })
