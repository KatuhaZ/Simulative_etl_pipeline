from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials as SA_Credentials

from src.settings import settings


class GoogleSheets:
    """работа с таблицами (создать, переместить, форматировать, заполнить)"""

    def __init__(self, logger, creds):
        self._logger = logger
        self.folderId = settings.folderId
        # Oauth
        self.creds = creds
        self.SCOPES = settings.SCOPES
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        #Service_Account
        self.credential_file = settings.secret_key
        self.SCOPES_SA = settings.SCOPES_SA
        self.creds_sa = SA_Credentials.from_service_account_file(self.credential_file, scopes=self.SCOPES_SA)
        self.service_sa = build('sheets', 'v4', credentials=self.creds_sa)
        self.drive_service_sa = build('drive', 'v3', credentials=self.creds_sa)

    # Создание файла
    def create_report_file(self, dt_start):
        file = self.service.spreadsheets().create(body={
            'properties': {'title': f'Daily_report_{dt_start[:10]}', 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                       'sheetId': 0,
                                       'title': f'Report_{dt_start}'}}]
        }).execute()
        self._logger.info(f"Создан файл: https://docs.google.com/spreadsheets/d/{file['spreadsheetId']}")
        return file

    # Перемещение файла
    def spreadsheet_moving(self, file):
        file_info = self.drive_service.files().get(fileId=file['spreadsheetId'], fields='parents').execute()
        parents = file_info.get('parents')
        previous_parents = ','.join(parents) if parents else None

        # Перемещаем файл в нужную папку
        try:
            result = self.drive_service.files().update(
                fileId=file['spreadsheetId'],
                addParents=settings.folderId,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            self._logger.info(f'Файл успешно перемещен {result}')
        except Exception:
            self._logger.exception('Не удалось переместить файл в указанную папку.')
            raise

    # Предоставление доступа сервисному аккаунту
    def get_permission(self, file):
        try:
            shareRes = self.drive_service.permissions().create(
                fileId=file['spreadsheetId'],
                body={
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.sa_email
                },
                fields='id'
            ).execute()
            self._logger.info(f'Доступ успешно предоставлен: {shareRes}')
        except Exception:
            self._logger.exception('Ошибка при предоставлении доступа.')
            raise

    # Заполнение данных
    def fill_data(self, file, dt, report):
        try:
            fill_res = self.service_sa.spreadsheets().values().batchUpdate(spreadsheetId=file['spreadsheetId'], body={
                'valueInputOption': 'USER_ENTERED',
                'data': [
                    {'range': f'Report_{dt}',
                     'majorDimension': 'ROWS',
                     'values': report}
                ]
            }).execute()
            self._logger.info(f'Отчет {file} успешно заполнен: {fill_res}')
        except Exception:
            self._logger.exception(f'Ошибка при заполнении отчета {file}')
            raise

    def file_formater(self, file, column_size):
        try:
            # Нужна тут эта переменная?
            prepare_report = self.service_sa.spreadsheets().batchUpdate(
                spreadsheetId=file['spreadsheetId'],
                body={
                    'requests': [
                        {'updateDimensionProperties': {
                            'range': {
                                'sheetId': 0,
                                'dimension': 'COLUMNS',
                                'startIndex': 0,
                                'endIndex': 1
                            },
                            'properties': {
                                'pixelSize': column_size
                            },
                            'fields': 'pixelSize'}},
                        {'repeatCell':{
                            'range': {
                                'sheetId': 0,
                                'startRowIndex': 0,
                                'endRowIndex': 2
                            },
                            'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
                            'fields': 'userEnteredFormat'}},
                        {'repeatCell': {
                            'range': {
                                'sheetId': 0,
                                'startRowIndex': 0,
                                'endRowIndex': 2
                            },
                            'cell': {'userEnteredFormat': {
                                'backgroundColor': {
                                    'red': 0.8,
                                    'blue': 0.8,
                                    'green': 0.8,
                                    'alpha': 0.3
                                },
                                'textFormat': {'bold': True}}},
                            'fields': 'userEnteredFormat'}}
                    ]
                }
            ).execute()
            self._logger.info('Файл успешно отформатирован.')
        except Exception:
            self._logger.exception('Не удалось настроить форматирование.')
            raise
