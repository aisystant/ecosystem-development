---
family: F6
kernel: D
system: D3
role: Architecture
status: active
target_audience:
  - Разработчики
  - DevOps
---

# Технологический стек

## Основные технологии

| Компонент | Технология | Версия |
|-----------|------------|--------|
| **Язык** | Python | 3.11+ |
| **Telegram API** | aiogram | 3.x |
| **AI** | Anthropic Claude API | — |
| **База данных** | PostgreSQL | 14+ |
| **Хостинг** | Railway / Render | — |

## Структура проекта

```
aist_bot/
├── src/
│   ├── handlers/          # Обработчики команд
│   ├── states/            # State Machine
│   ├── services/          # Бизнес-логика
│   ├── db/                # Работа с БД
│   └── utils/             # Утилиты
├── docs/
│   ├── ontology.md        # Терминология
│   ├── scenarios/         # Сценарии
│   └── processes/         # Процессы
├── tests/
│   └── test-manual/       # Ручные тесты
├── knowledge_structure.yaml
└── CLAUDE.md              # Инструкции для AI
```

## Ключевые зависимости

```
aiogram>=3.0
anthropic
asyncpg
pydantic
python-dotenv
```

## Инфраструктура

- **CI/CD**: GitHub Actions
- **Деплой**: Railway (production), Render (staging)
- **Мониторинг**: Sentry
- **Логирование**: structlog
