import pandas as pd
from datetime import datetime


class ReportBuilder:
    """Pасчёт метрик и формирование данных для отчёта"""
    def __init__(self, logger):
        self._logger = logger

    def get_report(self, data, dt1, dt2):
        dt_start = dt1[:10]
        dt_end = dt2[:10]
        period = datetime.strptime(dt_end, '%Y-%m-%d') - datetime.strptime(dt_start, '%Y-%m-%d')
        period_ru = 'день' if period.days == 1 else ('дня' if period.days in (2,3,4) else 'дней')
        df = pd.DataFrame(data)
        unique_user = df['user_id'].nunique()
        all_attempts = df['user_id'].count()
        correct_attempts = df['is_correct'].sum()
        correct_attempts_pr = correct_attempts / all_attempts * 100 if all_attempts else 0
        attempts_per_user = all_attempts / unique_user if unique_user else 0
        correct_attempts_per_user = correct_attempts / unique_user if unique_user else 0
        report = [
            [f'Отчет за {period.days} {period_ru}: с {dt_start} по {dt_end}'],
            ['Метрика', 'Значение'],
            ['Количество совершенных попыток:', int(all_attempts)],
            ['Количество успешных попыток:', int(correct_attempts)],
            ['Количество успешных попыток, %:', round(float(correct_attempts_pr), 2)],
            ['Количество уникальных пользователей:', unique_user],
            ['Количество попыток на одного пользователя:', round(float(attempts_per_user), 2)],
            ['Количество успешных попыток на одного пользователя:', round(float(correct_attempts_per_user), 2)]
        ]
        self._logger.info('Отчет сформирован')
        return report

    def get_column_size(self, data):
        return max([len(i[0]) for i in data]) * 7 + 20
