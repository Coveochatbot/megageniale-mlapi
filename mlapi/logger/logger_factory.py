import json
import sys
import logging


class LoggerFactory:
    __configuration_file_path = "logger/log.config"
    __loggers = dict()

    @staticmethod
    def configure(logger_name):
        configuration_data = json.load(open(LoggerFactory.__configuration_file_path))
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.getLevelName(configuration_data["level"]))

        handler_types = configuration_data["handlerTypes"]
        for handler_type in handler_types:
            if handler_type == "none":
                handler = logging.NullHandler()
                logger.addHandler(handler)
            if handler_type == "console":
                handler = logging.StreamHandler(stream=sys.stdout)
                handler.setFormatter(logging.Formatter(configuration_data["format"]))
                logger.addHandler(handler)
            if handler_type == "file":
                if configuration_data["appendToFile"] is True:
                    mode = 'a'
                else:
                    mode = 'w'
                handler = logging.FileHandler(configuration_data["filePath"], mode)
                handler.setFormatter(logging.Formatter(configuration_data["format"]))
                logger.addHandler(handler)
        LoggerFactory.__loggers[logger_name] = logger
        return logger

    @staticmethod
    def get_logger(logger_name):
        if logger_name in LoggerFactory.__loggers:
            return LoggerFactory.__loggers[logger_name]
        return LoggerFactory.configure(logger_name)
