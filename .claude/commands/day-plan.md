Выполни сценарий Day Plan для агента Стратег.

Источник сценария: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/scenarios/scheduled/02-day-plan.md

## Контекст

- **HUB (личные планы):** ~/Github/my-strategy/current/
- **SPOKE (планы репо):** ~/Github/*/WORKPLAN.md
- Шаблоны: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/templates/

## Алгоритм

1. **Апдейт о вчера:**
   - Загрузи план вчера из my-strategy/current/daily/ (если есть)
   - Получи коммиты за вчера из ВСЕХ репо в ~/Github/
   - Сопоставь РП и коммиты
   - Покажи статистику

2. **Контекст недели:**
   - Найди последний файл недели в my-strategy/current/weeks/
   - Загрузи его
   - Рассчитай прогресс по неделе

3. **План на сегодня:**
   - Выбери 2-4 РП из недельного плана
   - Учти carry-over со вчера
   - Учти дедлайны из WORKPLAN.md
   - Ограничь по дневному бюджету (4-6h)

4. **Рекомендация:**
   - Предложи с чего начать и почему

5. **Сохранение:**
   - Создай my-strategy/current/daily/YYYY-MM-DD.md
   - Закоммить в my-strategy

Результат: план на день с апдейтом о вчера и рекомендацией.
