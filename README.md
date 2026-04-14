[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Google Sheets](https://img.shields.io/badge/Google-Sheets-green.svg)](https://www.google.com/sheets/about/)

# 📊 Simulative ETL Pipeline

## 📌 Описание проекта

Данный проект представляет собой реализацию **ETL-пайплайна (Extract, Transform, Load)** для обработки данных об активности студентов в онлайн-образовательной системе.

---

## 🧩 Архитектура пайплайна

```
API → Extract → Transform → Load (PostgreSQL)
                    ↓
            Google Sheets Report
                    ↓
              Email Notification
```

### Основные этапы:

1. **Extract**

   * Получение данных через API (`requests`)
   * Параметры: `client`, `client_key`, `start`, `end`

2. **Transform**

   * Парсинг поля `passback_params`
   * Приведение данных к нужной структуре
   * Валидация данных
   * Обработка некорректных записей

3. **Load**

   * Загрузка данных в PostgreSQL (`psycopg2`)
   * Работа с таблицами и схемой БД

---

## 🗄️ Структура данных

В базе данных хранится следующая информация:

| Поле                    | Описание                    |
| ----------------------- | --------------------------- |
| user_id                 | ID пользователя             |
| oauth_consumer_key      | Токен клиента               |
| lis_result_sourcedid    | Идентификатор задания       |
| lis_outcome_service_url | URL для отправки результата |
| is_correct              | Результат попытки           |
| attempt_type            | Тип попытки (run / submit)  |
| created_at              | Дата и время                |

---

## ⚙️ Технологии

 - **Python 3.11**
- **requests** — работа с API
- **pandas** — обработка данных
- **psycopg2** — работа с PostgreSQL
- **Google Sheets API** + **Google Drive API**
- **Google OAuth 2.0** — авторизация
- **pydantic-settings** — управление конфигурацией
- **logging** — логирование

---

## 🚀 Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/KatuhaZ/Simulative_etl_pipeline.git
cd Simulative_etl_pipeline
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка окружения
Создать файл .env в корне проекта:

```
PGHOST=your_host
PGDATABASE=your_db
PGUSER=your_user
PGPASSWORD=your_password
PGSSLMODE=require

mail_password=your_app_password
MAIL_FROM=sender@mail.ru
MAIL_TO=recipient@mail.ru
```
Добавить ключ Google OAuth в папку secret/client_secret.json.

### 4. Настройка базы данных

* Установить PostgreSQL
* Создать базу данных
* Настроить параметры подключения

### 5. Запуск скрипта

```bash
# Отчёт за вчерашний день
python run.py

# Отчёт за конкретную дату
python run.py 2023-09-09

# Отчёт за период
python run.py 2023-09-01 2023-09-07
```

---
## 📊 **Результаты**
После выполнения:

* Данные загружены в таблицу problems в PostgreSQL
* Создан Google Sheets отчёт с метриками:
  * Количество попыток
  * Успешные попытки (%)
  * Уникальные пользователи
  * Попытки на пользователя
* Отправлено email-уведомление со ссылкой на отчёт

## 📝 Логирование
Логи сохраняются в папку logs/ с ротацией (хранятся последние 3 дня).

## 🔧 **Возможные улучшения**

* Добавить тесты (pytest)
* Настроить запуск по расписанию (cron / Airflow)
* Добавить Docker
* Визуализация метрик в Power BI / Tableau

## 👩‍💻 Автор
Екатерина Заварина

GitHub: @KatuhaZ
