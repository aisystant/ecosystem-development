Выполни сценарий Strategy Session для агента Стратег.

Источник сценария: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/scenarios/scheduled/01-strategy-session.md

## Контекст

- **HUB (личные планы):** ~/Github/my-strategy/current/
- **SPOKE (планы репо):** ~/Github/*/WORKPLAN.md
- **Неудовлетворённости:** ~/Github/my-strategy/dissatisfactions/current.md
- Шаблоны: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/templates/

## Алгоритм

1. **Анализ прошлой недели:**
   - Загрузи текущий weekly-plan.md из my-strategy/current/
   - Получи коммиты за прошлую неделю из ВСЕХ репо в ~/Github/
   - Рассчитай completion rate

2. **Обход WORKPLAN.md (Hub-and-Spoke):**
   - Прочитай ~/Github/*/WORKPLAN.md из каждого репо
   - Собери все РП со статусом pending/in-progress
   - Выяви расхождения с HUB-планом

3. **Сдвиг месячного окна:**
   - Загрузи monthly-priorities.md из my-strategy/current/
   - Учти неудовлетворённости из dissatisfactions/current.md
   - Предложи обновления

4. **План на неделю:**
   - Выбери РП из месячных приоритетов + WORKPLAN.md
   - Сформируй таблицу с бюджетом

5. **Запрос на подтверждение:**
   - Покажи итоги прошлой недели
   - Покажи предложение плана
   - Спроси о корректировках

6. **После подтверждения:**
   - Сохрани weekly-plan.md в my-strategy/current/
   - Обнови monthly-priorities.md в my-strategy/current/
   - Обнови WORKPLAN.md в целевых репо (обратная синхронизация)
   - Закоммить изменения в my-strategy
   - Закоммить изменения в затронутых репо
   - Зафиксируй сессию в my-strategy/sessions/YYYY-MM-DD.md

Результат: обновлённый план недели, месячные приоритеты, синхронизированные WORKPLAN.md.
