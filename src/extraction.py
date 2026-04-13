import requests

from src.settings import settings
from src.utils.date import validate_date


class Extraction:

    def __init__(self, logger):
        self._logger = logger
        self.api_url = settings.api_url

    # Выгрузка данных
    def extract_data(self, dt1, dt2):

        start = validate_date(dt1)
        end = validate_date(dt2)

        if not start or not end:
            self._logger.error(f'Некорректный формат дат {start, end}')
            raise

        params = settings.get_api_params(start, end)

        self._logger.info('Начало загрузки данных')
        try:
            response = requests.get(self.api_url, params=params)  # , timeout=30
            response.raise_for_status()
            data = response.json()
            self._logger.info(f'Загрузка данных прошла успешно. Получено записей: {len(data)}')
            return data

        except requests.exceptions.RequestException:
            self._logger.exception('Ошибка запроса к API')
            raise

        except ValueError:
            self._logger.exception('Ошибка парсинга JSON')
            raise
