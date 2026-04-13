import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from src.settings import settings

class GoogleClient:
    """Авторизация (OAuth)"""

    def __init__(self, logger):

        self._logger = logger
        self.SCOPES = settings.SCOPES

    # Загружаем токен если он существует
    def get_credentials(self):
        creds = None
        if os.path.exists('secret/token.pickle'):
            try:
                with open('secret/token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            except Exception:
                self._logger.exception('Файл token.pickle поврежден или неверный')

        if creds:
            if creds.valid:
                self._logger.info('Действующий токен успешно загружен')
                return creds
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self._logger.info('Токен успешно обновлен')
                    return creds
                except Exception:
                    self._logger.exception(f'Не удалось обновить токен.')

        try:
            flow = InstalledAppFlow.from_client_secrets_file('secret/client_secret.json', self.SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)
            with open('secret/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                self._logger.info('OAuth Токен успешно загружен')
                return creds
        except FileNotFoundError:
            self._logger.exception('client_secret.json не найден. Скачайте его в Google Cloud Console.')
            raise
        except Exception:
            self._logger.exception('Не удалось получить OAuth токен.')
            raise





