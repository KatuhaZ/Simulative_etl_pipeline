import psycopg2

from src.settings import settings


class DataBaseConnection:

    def __init__(self, logger):
        self._logger = logger
        try:
            self.connection = psycopg2.connect(
                host=settings.PGHOST,
                database=settings.PGDATABASE,
                user=settings.PGUSER,
                password=settings.PGPASSWORD,
                port=settings.PGPORT
            )
            self._initialized = True
            self._logger.info('Успешное подключение к БД')
        except Exception as err:
            self._logger.exception(f'Ошибка подключения к БД: {err} ({type(err).__name__})')
            raise

    def data_loading(self, data):
        self._logger.info('Начало загрузки данных в БД')

        try:
            with self.connection.cursor() as curr:
                request = """INSERT INTO problems(
                    user_id,
                    oauth_consumer_key,
                    lis_result_sourcedid,
                    lis_outcome_service_url,
                    is_correct,
                    attempt_type,
                    created_at
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id, created_at, attempt_type) DO NOTHING"""
                loading_data = [(
                    i.get('user_id'),
                    i.get('oauth_consumer_key'),
                    i.get('lis_result_sourcedid'),
                    i.get('lis_outcome_service_url'),
                    i.get('is_correct'),
                    i.get('attempt_type'),
                    i.get('created_at')
                ) for i in data]
                curr.executemany(request, loading_data)
                rows_inserted = curr.rowcount   # Подсчет кол-ва загруженных строк
                self.connection.commit()
                self._logger.info(f'Загрузка данных в БД прошла успешно.\nЗагружено строк: {rows_inserted}')

        except Exception as err:
            self._logger.exception(f'Ошибка загрузки данных в БД: {err} ({type(err).__name__})')
            try:
                if self.connection and not self.connection.closed:
                    self.connection.rollback()
            except:
                pass
            raise

    def close_connection(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            self._logger.info('Отключение от БД')
