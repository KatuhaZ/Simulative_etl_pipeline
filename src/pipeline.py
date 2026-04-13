from src.logger import Logger
from src.extraction import Extraction
from src.transformation import Transformation
from src.db_client import DataBaseConnection
from src.google_auth import GoogleClient
from src.google_sheets import GoogleSheets
from src.report_builder import ReportBuilder
from src.mail_service import SendMail


class ETLPipeline:

    def __init__(self):
        self._project_name = 'Final_project'
        self._logger = Logger(self._project_name).get_logger()
        self._logger.info(f'Старт работы {self._project_name}')

    def run(self, dt_start, dt_end):
        """Запускает полный ETL-пайплайн."""

        # 1. Extraction
        self._logger.info('Шаг 1: Загрузка данных из api')
        try:
            extractor = Extraction(self._logger)
            data = extractor.extract_data(dt_start, dt_end)
        except Exception:
            self._logger.exception('Ошибка на шаге 1')
            raise

        # 2. Transformation
        self._logger.info('Шаг 2: Обработка и валидация данных')
        try:
            transformator = Transformation(self._logger)
            transformed_data = transformator.transform(data)
        except Exception:
            self._logger.exception('Ошибка на шаге 2')
            raise

        # 3. Load to DB
        self._logger.info('Шаг 3: Загрузка в базу данных')
        try:
            db_connector = DataBaseConnection(self._logger)
            db_connector.data_loading(transformed_data)
            db_connector.close_connection()
        except Exception:
            self._logger.exception('Ошибка на шаге 3')
            raise

        # 4. Google authorization
        self._logger.info('Шаг 4: Авторизация в Google')
        try:
            authorization = GoogleClient(self._logger)
            creds = authorization.get_credentials()
        except Exception:
            self._logger.exception('Ошибка на шаге 4')
            raise

        # 5. Report builder
        self._logger.info('Шаг 5: Подготовка данных для отчета')
        try:
            report_builder = ReportBuilder(self._logger)
            report = report_builder.get_report(transformed_data, dt_start, dt_end)
            column_size = report_builder.get_column_size(report)
        except Exception:
            self._logger.exception('Ошибка на шаге 5')
            raise

        # 6. Create and fill googlesheet
        self._logger.info('Шаг 6: Создание, форматирование и заполнение файла')
        try:
            sheets_creator = GoogleSheets(self._logger, creds)
            file = sheets_creator.create_report_file(dt_start)
            sheets_creator.spreadsheet_moving(file)
            sheets_creator.get_permission(file)
            sheets_creator.fill_data(file, dt_start, report)
            sheets_creator.file_formater(file, column_size)
        except Exception:
            self._logger.exception('Ошибка на шаге 6')
            raise

        # 7. Send email
        self._logger.info('Шаг 7: Отправка письма о выполнении отчета')
        try:
            mailsender = SendMail(self._logger)
            mailsender.send_message(file, dt_start, dt_end, data, transformed_data)
        except Exception:
            self._logger.exception('Ошибка на шаге 7')
            raise

        self._logger.info('Pipeline успешно выполнен')
