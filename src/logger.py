import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime


class Logger:

    def __init__(self, name):
        self._logger = None
        self._name = name
        self._directory = 'logs'
        self._logger_configure()

    def _logger_configure(self):
        os.makedirs(self._directory, exist_ok=True)
        file_name = datetime.now().strftime('%Y-%m-%d.txt')
        path = os.path.join(self._directory, file_name)

        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(logging.INFO)

        # Очистка хэндлеров, чтобы избежать дубликатов
        if self._logger.hasHandlers():
            self._logger.handlers.clear()

        # Создаём обработчик для консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Будет показывать WARNING и выше

        # Создаём обработчик для файла
        file_handler = TimedRotatingFileHandler(
            path,
            when='midnight',  # каждый день
            interval=1,       # каждые 1 сутки
            backupCount=7,    # хранить 7 файлов (исправить на 3)
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)

        # Формат логов
        formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Добавляем обработчики в логгер
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def get_logger(self):
        return self._logger





