import structlog


if not structlog.is_configured():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"]
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        # "json_file": {
        #     "class": "logging.handlers.WatchedFileHandler",
        #     "filename": "logs/json.log",
        #     "formatter": "json_formatter",
        # },
        # "flat_line_file": {
        #     "class": "logging.handlers.WatchedFileHandler",
        #     "filename": "logs/flat_line.log",
        #     "formatter": "key_value",
        # },
    },
    "loggers": {
        "django_structlog": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "security": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
