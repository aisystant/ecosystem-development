Выполни сценарий Strategy Session для агента Стратег.

Источник сценария: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/scenarios/scheduled/01-strategy-session.md

## Контекст

- **HUB (личные планы):** ~/Github/my-strategy/current/
- **SPOKE (планы репо):** ~/Github/*/WORKPLAN.md
- **Неудовлетворённости:** ~/Github/my-strategy/dissatisfactions/current.md
- Шаблоны: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/templates/

## Структура current/

Каждая неделя — отдельная папка `current/YYYY-MM-DD--DD/plan.md`.
Приоритеты месяца включены в plan.md (секция "Приоритеты месяца").
Новые недели — сверху (сортировка по дате, от новых к старым).

## Алгоритм

1. **Анализ прошлой недели:**
   - Найди последнюю папку недели в my-strategy/current/
   - Загрузи plan.md из неё
   - Получи коммиты за прошлую неделю из ВСЕХ репо в ~/Github/
   - Рассчитай completion rate

2. **Обход WORKPLAN.md (Hub-and-Spoke):**
   - Прочитай ~/Github/*/WORKPLAN.md из каждого репо
   - Собери все РП со статусом pending/in-progress
   - Выяви расхождения с HUB-планом

3. **Сдвиг месячного окна:**
   - Приоритеты месяца — в секции plan.md прошлой недели
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
   - Создай новую папку current/YYYY-MM-DD--DD/ с plan.md
   - Обнови WORKPLAN.md в целевых репо (обратная синхронизация)
   - Закоммить изменения в my-strategy
   - Закоммить изменения в затронутых репо
   - Зафиксируй сессию в my-strategy/sessions/YYYY-MM-DD.md

Результат: новая папка недели с plan.md, синхронизированные WORKPLAN.md.
