from datetime import datetime


# Проверка ввода даты
def validate_date(dt):
    """Приводит дату к формату API: YYYY-MM-DD HH:MM:SS.ffffff"""

    if not dt:
        return None

    # Пробуем разные форматы
    formates = [
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d'
    ]

    for fmt in formates:
        try:
            dt_obj = datetime.strptime(dt, fmt)
            return dt_obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            continue

    return None
