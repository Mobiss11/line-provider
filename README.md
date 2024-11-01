# Line Provider Service

## Описание
Line Provider Service - это сервис для управления событиями и ставками, разработанный с использованием FastAPI и Redis. Сервис предоставляет API для создания событий, управления их статусами и регистрации callback-уведомлений.

## Особенности
- 🚀 Асинхронная обработка запросов
- 📦 Redis для хранения данных с TTL
- 🔄 Система callback-уведомлений
- 📝 Автоматическая OpenAPI документация
- 🧪 Полное тестовое покрытие
- 🐳 Docker и Docker Compose поддержка

## Требования
- Python 3.10+
- Redis 6+
- Docker и Docker Compose (для контейнеризации)

## Структура проекта
```
line_provider/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Основной файл приложения
│   ├── api/                 # API endpoints
│   ├── core/                # Конфигурация и базовые компоненты
│   ├── models/              # Pydantic модели
│   ├── schemas/             # Схемы запросов/ответов
│   ├── services/            # Бизнес-логика
│   └── storage/             # Работа с хранилищем
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Общие фикстуры и конфигурация
│   ├── test_events.py        # Тесты для событий
│   ├── test_callbacks.py     # Тесты для callbacks
│   └── test_service.py       # Тесты для Cервисов
│
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Установка и запуск

### Локальная разработка
```bash
# Клонирование репозитория
git clone https://github.com/Mobiss11/line-provider
cd line-provider

# Создание и активация виртуального окружения
python3.10 -m venv venv
source venv/bin/activate

# Установка и обновление необходимых инструментов
pip install pip --upgrade
pip install setuptools --upgrade
pip install poetry

# Установка зависимостей проекта
poetry install
```

### Запуск через Docker
```bash
# Сборка
docker build -t line-provider:latest .

# Сборка и запуск
docker-compose up --build

# Только запуск (если образ уже собран)
docker-compose up -d

# Остановка
docker-compose down
```

## Конфигурация
Настройки приложения можно изменить через переменные окружения или файл `.env`:

```env
APP_NAME=Line Provider Service
DEBUG=True
REDIS_URL=redis://127.0.0.1:6378/0
EVENT_EXTRA_TTL=604800
CALLBACK_TTL=86400
```

## Тестирование

### Настройка окружения для тестов
```bash
# Убедитесь, что Redis запущен для тестов
docker run -d -p 6379:6379 --name redis-test redis:6

# Или используйте docker-compose
docker-compose up -d redis
```

### Запуск тестов
```bash
# Запуск всех тестов
poetry run pytest

# Запуск с подробным выводом
poetry run pytest -v

# Запуск тестов с покрытием
poetry run pytest --cov=app tests/

# Запуск конкретной группы тестов
poetry run pytest tests/test_events.py

# Запуск тестов с метками
poetry run pytest -m "slow"  # медленные тесты
poetry run pytest -m "integration"  # интеграционные тесты

# Параллельный запуск тестов
poetry run pytest -n auto  # использует все доступные CPU ядра
```

### Тестовое покрытие
```bash
# Генерация HTML-отчета о покрытии
poetry run pytest --cov=app --cov-report=html

# Отчет будет доступен в coverage_html/index.html
```

### Отладка тестов
```bash
# Подробный вывод с print-statements
poetry run pytest -v --capture=no

# Остановка после первого падения
poetry run pytest -x

# Вывод самых медленных тестов
poetry run pytest --durations=10
```

## Configuration Ruff
```toml
[tool.ruff]
fix = true
unsafe-fixes = true
line-length = 120
select = ["ALL"]
ignore = ["D1", "D203", "D213", "FA102", "ANN101", "UP007", "TCH001", "BLE001", "DTZ005", "TRY300", "DTZ007"]

[tool.ruff.isort]
no-lines-before = ["standard-library", "local-folder"]
known-third-party = []
known-local-folder = ["whole_app"]

[tool.ruff.extend-per-file-ignores]
"./*.py" = ["ANN401", "S101", "S311", "F401"]
```

## API Endpoints

### События (Events)

#### Получение списка событий
```http
GET /events
```
Ответ:
```json
{
    "status": "success",
    "message": "События успешно получены",
    "data": {
        "events": {
            "event1": [{
                "event_id": "event1",
                "coefficient": 1.85,
                "deadline": "2024-03-25T12:00:00",
                "status": "new"
            }]
        }
    }
}
```

#### Создание события
```http
POST /events
```
Запрос:
```json
{
    "event_id": "event1",
    "coefficient": 1.85,
    "deadline": "2024-10-29T15:00:00",
    "status": "new"
}
```

#### Обновление статуса события
```http
PUT /events/{event_id}/status
```
Запрос:
```json
{
    "status": "first_team_won"
}
```

### Callbacks

#### Регистрация callback
```http
POST /callbacks/register
```
Запрос:
```json
{
    "url": "http://example.com/webhook"
}
```

## CI/CD
- Проверка типов (mypy)
- Линтинг (ruff)
- Тесты (pytest)

## Производительность

### Redis оптимизации
- Использование pipeline для множественных операций
- Эффективное управление TTL
- Оптимизированная структура данных

### TTL полезен в нашем приложении для:

- Автоматической очистки памяти - старые события удаляются автоматически
- Соблюдения бизнес-правил - события недоступны для ставок после дедлайна
- Оптимизации памяти - не храним устаревшие данные
- Управления callbacks - неактивные webhooks автоматически удаляются
- Для событий: время до дедлайна + время хранения истории
- Для callbacks: время между пингами + запас

## Безопасность

### Основные меры
- Валидация входных данных
- CORS настройки

### Рекомендации по развертыванию
- Использование HTTPS
- Настройка файрвола
- Регулярное обновление зависимостей

## FAQ

### Как добавить новый endpoint?
1. Создайте новый файл в `app/api/endpoints/`
2. Определите новый router
3. Добавьте router в `app/api/routes.py`
4. Добавьте тесты

### Как изменить время жизни событий?
Измените `EVENT_EXTRA_TTL` в настройках окружения или `.env` файле.

### Дальнейшее масштабирование
1. Используйте несколько инстансов Redis
2. Настройте балансировщик нагрузки
3. Используйте Redis Cluster для больших нагрузок
