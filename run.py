import sys
from datetime import datetime, timedelta
from src.pipeline import ETLPipeline

from src.utils.date import validate_date

if __name__ == '__main__':

    # Берём даты из командной строки или используем по умолчанию
    if len(sys.argv) == 1:
        yesterday = datetime.now() - timedelta(days=1)
        dt1 = yesterday
    else:
        dt1 = datetime.strptime(validate_date(sys.argv[1]), '%Y-%m-%d %H:%M:%S.%f')

    dt2 = sys.argv[2] if len(sys.argv) > 2 else (dt1 + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    dt1 = dt1.strftime('%Y-%m-%d %H:%M:%S')

    print(dt1, dt2)

    # Запускаем пайплайн
    pipeline = ETLPipeline()
    pipeline.run(dt1, dt2)
