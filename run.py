import sys
from datetime import datetime, timedelta
from src.pipeline import ETLPipeline

if __name__ == '__main__':

    # Берём даты из командной строки или используем по умолчанию
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    dt1 = sys.argv[1] if len(sys.argv) > 1 else yesterday
    dt2 = sys.argv[2] if len(sys.argv) > 2 else dt1

    # Запускаем пайплайн
    pipeline = ETLPipeline()
    pipeline.run(dt1, dt2)
