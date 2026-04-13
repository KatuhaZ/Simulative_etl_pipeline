import os
import ssl
import smtplib
from email.message import EmailMessage
from datetime import datetime

from src.settings import settings


class SendMail:

  def __init__(self, logger):
    # Создадим защищенное соединение
    self.context = ssl.create_default_context()
    self._logger = logger

  def send_message(self, file, dt_start, dt_end, extract_data, transformed_data):
    log_file = datetime.now().strftime('%Y-%m-%d.txt')
    log_path = os.path.join('logs', log_file)
    try:
      # Создадим новый объект письма
      msg = EmailMessage()
      # Заполним письмо
      subject = 'Завершение процедуры загрузки данных'
      message = f"""
      Коллеги, Добрый день!

      Автоматическая процедура загрузки данных завершена.

      Параметры выполнения:
      • Период: {dt_start} — {dt_end}
      • Всего обработано строк: {len(extract_data)}
      • Успешно загружено: {len(transformed_data)}
      • Ошибок обработки: {len(extract_data) - len(transformed_data)}

      Отчёт доступен по ссылке: https://docs.google.com/spreadsheets/d/{file['spreadsheetId']}
      Лог выполнения: {log_path}

      С уважением,
      Команда Data Analytics
      """
      msg.set_content(message)
      msg['Subject'] = subject
      msg['From'] = settings.MAIL_FROM
      msg['To'] = settings.MAIL_TO
      self._logger.info('Письмо успешно сформировано')

    except Exception as err:
      self._logger.exception(f'Ошибка создания письма: {err}')
      raise

    try:
      # Создадим защищенное SSL-соединение с SMTP-сервером, который обрабатывает отправку электронной почты.
      # Вы указываете smtp_server и port, чтобы указать сервер и порт для подключения. context=context - это контекст SSL.
      server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT, context=self.context)

      # Авторизуемся на SMTP-сервере, используя адрес электронной почты (sender_email) и пароль (password)
      server.login(settings.MAIL_FROM, settings.MAIL_PASSWORD)

      # Отправка письма (msg) через подключенное SSL-соединение к SMTP-серверу.
      server.send_message(msg=msg)
      server.quit()
      self._logger.info(f'Письмо успешно отправлено')

    except Exception as err:
      self._logger.exception(f'Ошибка отправки письма: {err}')
      raise
