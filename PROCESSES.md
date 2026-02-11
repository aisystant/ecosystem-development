---
type: process
status: active
created: 2026-02-10
updated: 2026-02-10
---

# Процессы экосистемы

> Межсистемные процессы (сценарии) экосистемы развития интеллекта.
> Внутренние процессы каждой системы → `<repo>/PROCESSES.md`.
> Различение: процесс = поток действий с ВДВ; сценарий = межсистемный процесс (синоним).

---

## 1. Пользовательские сценарии

### 1.1. Рабочая сессия Claude Code

> Тип: пользовательский сценарий
> Владелец: Claude Code (сессия)
> Участники: Пользователь, Claude Code, MEMORY.md, CLAUDE.md, memory/*.md, DS-strategy, Pack-репо

**Вход:** Задание от пользователя

**Действие:**

1. **Open: WP Gate** — Claude проверяет РП в MEMORY.md → совпадает/СТОП
2. **Open: Ритуал** — Claude объявляет Работу/РП/Метод → пользователь согласует
3. **Work** — выполнение задачи + capture-to-pack на рубежах
4. **Close** — собрать captures → применить → обновить MEMORY.md → обновить DS-strategy/Plan → backup memory/ → DS-strategy/exocortex/ → коммит

**Выход:** Закоммиченный результат, обновлённый план, captures в Pack/CLAUDE.md/memory

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| MEMORY.md (таблица РП) | Вход → Claude | Markdown |
| CLAUDE.md (протоколы) | Вход → Claude | Markdown |
| memory/*.md (справочники) | Вход → Claude (по необходимости) | Markdown |
| Captures | Выход → Pack / CLAUDE.md / memory | Текст |
| Статусы РП | Выход → MEMORY.md, DS-strategy/Plan | Таблица |

---

### 1.2. Стратегирование недели

> Тип: пользовательский сценарий
> Владелец: Пользователь + Стратег
> Участники: Пользователь, Стратег, DS-strategy, все ~/Github/*/WORKPLAN.md, ~/Github/*/MAPSTRATEGIC.md

**Вход:** WeekReport W{N-1} (создан week-review, Пн 00:00), WORKPLAN.md, MAPSTRATEGIC.md, docs/*, inbox/*

**Действие:**

1. **Week-Review (авто, Пн 00:00)** — Стратег собирает коммиты за неделю → WeekReport
2. **Session-Prep (авто, Пн 4:00)** — Стратег читает WeekReport + docs/ + inbox/ + MAPSTRATEGIC.md → обновляет Strategy.md → формирует draft WeekPlan с повесткой
3. **Strategy-Session (интерактив, вручную)** — пользователь утверждает/корректирует → синхронизация WORKPLAN.md, MEMORY.md, Strategy.md, очистка inbox

> Бывший Strategy-Cascade поглощён session-prep (агрегация MAPSTRATEGIC) и strategy-session (синхронизация).

**Выход:** WeekReport (для клуба), WeekPlan W{N} (confirmed), обновлённые Strategy.md, WORKPLAN.md, MEMORY.md

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| WeekReport W{N-1} | Вход → Strategy | Markdown |
| ~/Github/*/WORKPLAN.md | Вход → Strategy | Markdown |
| ~/Github/*/MAPSTRATEGIC.md | Вход → Strategy | Markdown |
| WeekPlan W{N} | Выход → DS-strategy/current/ | Markdown |
| MEMORY.md (новые РП) | Выход → memory/ | Markdown |

---

## 2. Платформенные сценарии

### 2.1. Day-Close

> Тип: платформенный сценарий
> Владелец: Стратег (ручной — по запросу пользователя)
> Участники: Стратег, все ~/Github/ репо, DS-strategy, MEMORY.md, экзокортекс

**Вход:** Коммиты за день (git log по всем ~/Github/ репо)

**Действие:**

1. Сбор коммитов → группировка по репо и РП
2. Обновление WeekPlan W{N} (статусы, carry-over)
3. Синхронизация MEMORY.md (статусы РП)
4. Backup: memory/ + CLAUDE.md → DS-strategy/exocortex/
5. Коммит

> Отдельный файл отчёта НЕ создаётся. Итоги дня войдут в DayPlan следующего утра.

**Выход:** Обновлённый WeekPlan, актуальный MEMORY.md, backup экзокортекса

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| git log (все репо) | Вход → Стратег | Git output |
| WeekPlan W{N} (обновлённый) | Выход → DS-strategy/current/ | Markdown |
| MEMORY.md (обновлённый) | Выход → memory/ | Markdown |
| Exocortex backup | Выход → DS-strategy/exocortex/ | Файлы |

---

### 2.2. Синхронизация экзокортекса (Backup)

> Тип: платформенный сценарий
> Владелец: Claude Code (Close) + Стратег (day-close)
> Участники: memory/*.md, ~/Github/CLAUDE.md, DS-strategy/exocortex/

**Вход:** Изменённые файлы memory/*.md + CLAUDE.md

**Действие:** Копирование → DS-strategy/exocortex/

**Выход:** Версионированная копия в git (DS-strategy)

---

## 3. Формат описания процесса (шаблон)

```markdown
### Процесс: [Название]

> Тип: пользовательский сценарий | платформенный сценарий | внутренний процесс
> Владелец: [система]
> Участники: [системы]

**Вход:** [данные]
**Действие:** [шаги]
**Выход:** [данные]

**Данные:** (таблица ВДВ)
```

---

*Последнее обновление: 2026-02-10*
