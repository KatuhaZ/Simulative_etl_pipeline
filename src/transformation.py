import ast
from datetime import datetime


class Transformation:

    def __init__(self, logger):
        self._logger = logger

    # Формирование массива для загрузки в базу:
    def transform(self, data):
        result = []

        for line in data:
            lis_result_sourcedid, lis_outcome_service_url = self._parse_passback(line)

            if self._is_valid_row(line, lis_result_sourcedid, lis_outcome_service_url):
                result.append({
                    'user_id': line.get('lti_user_id'),
                    'oauth_consumer_key': line.get('oauth_consumer_key'),
                    'lis_result_sourcedid': lis_result_sourcedid,
                    'lis_outcome_service_url': lis_outcome_service_url,
                    'is_correct': line.get('is_correct'),
                    'attempt_type': line.get('attempt_type'),
                    'created_at': line.get('created_at')
                })
            else:
                self._logger.info(f'Ошибка добавления. Строка: {line}')

        self._logger.info(
            f'Добавлено строк: {len(result)}\n'
            f'Строк с ошибкой: {len(data) - len(result)}'
        )
        return result

    def _parse_passback(self, line):
        raw = line.get('passback_params')

        if not raw:
            return None, None
        try:
            pms = ast.literal_eval(raw)
            lis_result_sourcedid = pms.get('lis_result_sourcedid')
            lis_outcome_service_url = pms.get('lis_outcome_service_url')
            return lis_result_sourcedid, lis_outcome_service_url
        except (SyntaxError, ValueError) as err:  # Можно except Exception
            self._logger.exception(f'Ошибка парсинга passback_params: {err}. Строка: {line}')
            return None, None

    def _is_valid_row(self, line, lis_result_sourcedid, lis_outcome_service_url):
        return all([
            self._is_valid_user(line.get('lti_user_id')),
            self._is_valid_oauth_consumer_key(line.get('oauth_consumer_key')),
            self._is_valid_lis_result_sourcedid(lis_result_sourcedid),
            self._is_valid_lis_outcome_service_url(lis_outcome_service_url),
            self._is_valid_is_correct(line.get('is_correct')),
            self._is_valid_attempt_type(line.get('attempt_type')),
            self._is_valid_created_at(line.get('created_at'))
        ])

    # Проверка данных на соответствие:
    # id клиента
    def _is_valid_user(self, user_id):
        if user_id and isinstance(user_id, str):
            return True
        else:
            self._logger.info(f'Некорректный user_id: {user_id}.')
            return False

    # уникальный токен клиента
    def _is_valid_oauth_consumer_key(self, oauth_consumer_key):
        if oauth_consumer_key is None or isinstance(oauth_consumer_key, str):
            return True
        else:
            self._logger.info('Некорректный oauth_consumer_key')
            return False

    # ссылка на блок, в котором находится задача в ЛМС
    def _is_valid_lis_result_sourcedid(self, lis_result_sourcedid):
        if not lis_result_sourcedid or isinstance(lis_result_sourcedid, str):
            return True
        else:
            self._logger.info(f'Некорректный lis_result_sourcedid: {lis_result_sourcedid}')
            return False

    # URL адрес в ЛМС, куда мы шлем оценку
    def _is_valid_lis_outcome_service_url(self, outcome_service_url):
        if not outcome_service_url or isinstance(outcome_service_url, str):
            return True
        else:
            self._logger.info(f'Некорректный lis_outcome_service_url: {outcome_service_url}')
            return False

    # была ли попытка верной (null, если это run)
    def _is_valid_is_correct(self, is_correct):
        if is_correct in [None, 0, 1]:
            return True
        else:
            self._logger.info(f'Некорректный is_correct: {is_correct}')
            return False

    # ран или сабмит
    def _is_valid_attempt_type(self, attempt_type):
        if attempt_type in ['run', 'submit']:
            return True
        else:
            self._logger.exception(f'Некорректный attempt_type: {attempt_type}')
            return False

    # дата попытки
    def _is_valid_created_at(self, created_at):
        try:
            datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')
            return True
        except ValueError:
            self._logger.exception(f'Некорректный created_at: {created_at}')
            return False
