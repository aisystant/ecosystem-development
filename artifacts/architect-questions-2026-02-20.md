---
type: meeting-prep
date: 2026-02-20
with: Архитектор
topics: bot-scaling, IWE-architecture
status: draft
---

# Вопросы для обсуждения с Архитектором — 20 фев 2026

## A. Бот: масштабирование до 10K пользователей

### Контекст

Бот @aist_me_bot (Telegram, aiogram, PostgreSQL/Neon, Claude API). Текущая ёмкость ~50 concurrent. Цель: 10K DAU (~500 concurrent). Диагноз ошибок: 60% архитектура, 25% инфраструктура, 15% код.

Уже сделано (Phase 0): DB pool 10→50, Claude semaphore(10) + retry, MCP session reuse, scheduler semaphore 5→20.

### Вопросы

**A1. Polling → Webhook: когда и как?**
Сейчас бот работает через long polling (один процесс). Для horizontal scaling нужны webhooks. Вопрос: делать переход сейчас (300 users) или отложить до 500+? Что нужно для stateless webhooks с aiogram (FSM storage, session affinity)?

**A2. Scheduler как отдельный сервис**
Scheduler сейчас внутри bot process. При multi-instance дублируется. Варианты:
- Redis pub/sub + один scheduler worker
- Postgres advisory locks (бесплатно, но coupling)
- Cron-сервис (Railway cron + HTTP trigger)
Какой подход правильнее для 5-10 инстансов?

**A3. Claude API cost: $5K/мес при 10K DAU**
96% стоимости — Claude API. Mitigation:
- Haiku для простых задач (навигация, команды) — какой порог переключения?
- Кэширование сгенерированного контента (тот же контент для той же темы?) — trade-off персонализация vs. стоимость
- Prompt caching (Anthropic feature) — применимо ли?
Какая архитектура оптимальна?

**A4. Circuit breaker: единый паттерн**
Сейчас circuit breaker есть для MCP (2 failures → 60s cooldown), но нет для Claude API. Нужен ли единый circuit breaker middleware? Или достаточно per-client?

**A5. Observability: Sentry vs. текущий async error logger**
Текущий мониторинг: async DB logging + Telegram alerts. Для 10K нужен managed monitoring? Sentry ($26/мес), Grafana Cloud (free tier), или достаточно улучшить текущее?

**A6. Connection pooling: PgBouncer vs. Neon Pro**
Neon Free: 100 connections. При 5 инстансах × 50 = 250 нужно. Варианты:
- Neon Pro ($20/мес): 100 connections + PgBouncer built-in
- Supabase PgBouncer: connection multiplexing (1000 client → 100 DB)
- Self-hosted PgBouncer на Railway
Что выбрать?

**A7. Рассредоточение пиковой нагрузки (slot-based scheduling)**
Сейчас пользователь выбирает время рассылки (большинство — 10:00). При 1000 users в 10:00 — scheduler перегружен. Идея: ограничивать количество пользователей на один слот (например, max 50 на 10:00), предлагать ближайшее свободное окно (10:05, 10:10...). Вопросы:
- Гранулярность слотов: 5 мин? 15 мин?
- UX: «10:00 занято, предлагаем 10:05» или автоматический сдвиг?
- Нужна ли таблица слотов в БД или достаточно COUNT по scheduled_hour/minute?

---

## B. IWE: архитектура платформы

*(заполнить позже)*

---

## C. Общие архитектурные вопросы

*(заполнить позже)*
