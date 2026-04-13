from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    api_url: str = 'https://b2b.itresume.ru/api/statistics'

    PGHOST: str
    PGDATABASE: str
    PGUSER: str
    PGPASSWORD: str
    PGPORT: str

    SCOPES: list = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file'
    ]

    SCOPES_SA: list = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    MAIL_PASSWORD: str

    secret_key: str = 'secret/secret_key_service_accaunt.json'  # имя файла с закрытым ключом для сервисного аккаунта
    sa_email: str = 'googlesheet2@acquired-shape-477512-n1.iam.gserviceaccount.com'  # сервисный аккаунт

    MAIL_FROM: str = 'edproject_zavarina@mail.ru'
    MAIL_TO: str = 'katuha_tarasova@mail.ru'  # Получатели автоматической рассылки
    SMTP_SERVER: str = 'smtp.mail.ru'
    SMTP_PORT: int = 465
    folderId: str = '1BGlSQ58OvB6deoEjPJAt4Ht5QviE1vFF'  # Id папки для хранения dailyreport

    client: str = 'Skillfactory'
    CLIENT_KEY: str

    def get_api_params(self, start: str, end: str) -> dict:
        return {
            'client': self.client,
            'client_key': self.CLIENT_KEY,
            'start': start,
            'end': end
        }

    @property
    def pg_url(self) -> str:
        return f'postgresql://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}'

    class Config:
        env_file = '.env'


settings = Settings()