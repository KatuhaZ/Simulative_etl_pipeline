import sys
from datetime import datetime, timedelta
from src.pipeline import ETLPipeline

from src.utils.date import validate_date

if __name__ == '__main__':

    # Берём даты из командной строки или используем по умолчанию
    if len(sys.argv) == 1:
        yesterday = datetime.now().date() - timedelta(days=1)
        dt1 = yesterday
    elif len(sys.argv) > 2:
        try:
            dt1 = datetime.strptime(sys.argv[1], '%Y-%m-%d')
            dt2 = datetime.strptime(sys.argv[2], '%Y-%m-%d')
        except Exception:
            print(f'Ошибка: некорректный формат даты: {sys.argv[1], sys.argv[2]}')
            sys.exit(1)  # ← завершить программу с ошибкой
    else:
        try:
            dt1 = datetime.strptime(sys.argv[1], '%Y-%m-%d')
            dt2 = dt1 + timedelta(days=1)
        except Exception:
            print(f'Ошибка: некорректный формат даты: {sys.argv[1]}')
            sys.exit(1)  # ← завершить программу с ошибкой

    # Добавляем время 00:00:00 для API
    dt1_str = dt1.strftime('%Y-%m-%d') + ' 00:00:00'
    dt2_str = dt2.strftime('%Y-%m-%d') + ' 00:00:00'


    # Запускаем пайплайн
    print(f'Запускаем pipeline за период: {dt1} - {dt2}')
    pipeline = ETLPipeline()
    pipeline.run(dt1_str, dt2_str)
