“Канонический” шаблон удобно положить в репозиторий и применять как стандарт описания MCP-интерфейса Цифрового двойника: отдельно для **tools** (вызываемых действий) и **resources** (read-only контекста). 
Шаблон ориентирован на то, чтобы (а) модели было проще корректно выбирать и интерпретировать, (б) человеку было проще сопровождать, (в) интеграции через MCP были предсказуемыми. MCP-логика “tool-first”, JSON Schema и рекомендации по узким/атомарным инструментам соответствуют текущим подходам MCP и Apps SDK. ([OpenAI Developers](https://developers.openai.com/apps-sdk/concepts/mcp-server/?utm_source=chatgpt.com "MCP"))

---

# Шаблон описания MCP Tools

## 0) Заголовок

**Tool name:** `dt.get_time_invested_summary`  
**Подсистема-владелец:** Цифровой двойник (Digital Twin)  
**Статус:** draft | stable | deprecated  
**Версия контракта:** `v1` (см. правила версионирования ниже)  
**Дата обновления:** YYYY-MM-DD  
**Ответственный:** роль/команда  
**Зависимости:** какие ресурсы/таблицы/сервисы читает/пишет

---

## 1) Назначение (Intent)

Коротко: что tool делает и какую пользовательскую/агентную задачу закрывает.

**Одна фраза:**  
Возвращает агрегаты инвестированного времени за период (total/avg/breakdown) из данных Цифрового двойника с указанием качества данных.

---

## 2) Когда использовать / когда НЕ использовать (границы применимости)

**Use when:**

- нужно получить агрегаты по времени за период для диагностики ритма/прогресса;
    
- нужно сравнить неделю к неделе или построить простую сводку.
    

**Do NOT use when:**

- нужен список событий поштучно (используй `dt.list_activity_events`);
    
- нужна оценка “продуктивности” или “качества” (это другая метрика/слой методики);
    
- нет уверенности, что период закрыт данными (тогда сначала `dt.get_data_coverage`).
    

Эта секция критична: она снижает “угадывание” модели и повышает корректность выбора. ([MCP Protocol](https://modelcontextprotocol.info/docs/concepts/tools/?utm_source=chatgpt.com "Tools"))

---

## 3) Контракт вызова

### 3.1 Input schema (JSON Schema)

Описывайте параметры детально (единицы, форматы, ограничения), чтобы tool проще подключался и реже ломался из-за “особых случаев”. ([OpenAI Developers](https://developers.openai.com/apps-sdk/concepts/mcp-server/?utm_source=chatgpt.com "MCP"))

```json
{
  "type": "object",
  "required": ["start_date", "end_date", "timezone"],
  "properties": {
    "start_date": {
      "type": "string",
      "description": "Начало периода (включительно) в формате YYYY-MM-DD."
    },
    "end_date": {
      "type": "string",
      "description": "Конец периода (включительно) в формате YYYY-MM-DD."
    },
    "timezone": {
      "type": "string",
      "description": "IANA timezone, например Asia/Nicosia."
    },
    "granularity": {
      "type": "string",
      "enum": ["none", "day", "week"],
      "default": "day",
      "description": "Детализация выдачи по под-периодам."
    },
    "filters": {
      "type": "object",
      "description": "Фильтры по типам активности/источникам и т.п.",
      "properties": {
        "activity_type": { "type": "string", "description": "Напр. learning, work, reading." },
        "sources": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Напр. timer, manual_log, calendar."
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

### 3.2 Output schema (документируемый формат ответа)

MCP формально требует schema для входа; но для устойчивости интеграций фиксируйте и выходной формат как стандарт. ([OpenAI Developers](https://developers.openai.com/apps-sdk/concepts/mcp-server/?utm_source=chatgpt.com "MCP"))

```json
{
  "period": { "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD", "timezone": "IANA" },
  "total_minutes": 0,
  "avg_minutes_per_day": 0,
  "breakdown": [
    { "date": "YYYY-MM-DD", "minutes": 0 }
  ],
  "data_quality": {
    "coverage_ratio": 0.0,
    "sources": ["timer", "manual_log"],
    "last_sync_at": "ISO-8601",
    "notes": "Короткий комментарий, если есть."
  }
}
```

---

## 4) Семантика данных (самое важное для “Цифрового двойника”)

Здесь вы “заземляете” смысл, чтобы модель не додумывала.

- **Определение метрики:** что считается “инвестированным временем”, какие правила суммирования.
    
- **Единицы измерения:** минуты (целое), округление, отсечение хвостов.
    
- **Границы периода:** включительность start/end, timezone.
    
- **Что НЕ входит:** примеры исключений (сон, дорога, idle и т.п.).
    
- **Конфликты источников:** приоритет/правила merge (если есть).
    

Рекомендуется ссылаться на ресурс-каталог метрик (см. шаблон resources ниже) вместо того, чтобы копировать определения в каждый tool. ([MCP Protocol](https://modelcontextprotocol.info/docs/concepts/resources/?utm_source=chatgpt.com "Resources"))

---

## 5) Метаданные качества данных (обязательный стандарт)

Чтобы агент не делал уверенных выводов при неполных данных:

- `coverage_ratio` — доля покрытия периода (0..1).
    
- `last_sync_at` — когда данные последовательно обновлялись.
    
- `sources[]` — какие источники реально участвовали.
    
- `confidence` (опционально) — если вы умеете оценивать достоверность.
    
- `notes` — краткая причина низкого покрытия.
    

---

## 6) Ошибки и валидация

**Валидация до выполнения:**

- формат дат, start ≤ end;
    
- максимальная длина периода (например, ≤ 366 дней);
    
- whitelist фильтров.
    

**Коды ошибок (пример):**

- `INVALID_ARGUMENT` — неверный формат дат/таймзоны/фильтра;
    
- `NO_DATA` — данных за период нет (это не “0 минут”, это отсутствие наблюдений);
    
- `PARTIAL_DATA` — данные есть, но `coverage_ratio < threshold`;
    
- `UNAUTHORIZED` / `FORBIDDEN` — нет прав;
    
- `RATE_LIMITED` — превышены лимиты;
    
- `INTERNAL` — внутренняя ошибка.
    

---

## 7) Примеры (минимум 2)

### Пример A: “Сводка за прошлую неделю”

**User intent:** “Сколько времени я инвестировал на прошлой неделе и среднее в день?”  
**Tool call args:** start/end/timezone.  
**Expected response:** total/avg + breakdown + quality.

### Пример B: “Только learning по данным таймера”

Фильтры: activity_type + sources.

(Важно: примеры должны показывать границы применимости.) ([MCP Protocol](https://modelcontextprotocol.info/docs/concepts/tools/?utm_source=chatgpt.com "Tools"))

---

## 8) Безопасность, приватность, доступ

- **Scopes/permissions:** какие роли/клиенты имеют доступ.
    
- **Минимизация данных:** возвращайте только то, что нужно сценарию.
    
- **Аудит:** логируйте кто/когда/что запрашивал.
    
- **Auth:** как проверяются токены/сессии (если вы публикуете как ChatGPT App — смотрите auth-архитектуру). ([OpenAI Developers](https://developers.openai.com/apps-sdk/build/auth/?utm_source=chatgpt.com "Authentication - Apps SDK"))
    

---

## 9) Наблюдаемость (observability)

- latency p50/p95, error rate, доля `NO_DATA`, доля `PARTIAL_DATA`, средний coverage;
    
- трассировка request_id → вызовы хранилища;
    
- метрика “tool_selected_vs_tool_needed” (в тестовом стенде).
    

---

## 10) Версионирование и совместимость

- Нейминг: `dt.<verb>_<object>_<qualifier>` (коротко, без лишней “поэзии”).
    
- **MAJOR** меняйте при breaking changes (удаление/переименование полей).
    
- MINOR — добавление полей (backward compatible).
    
- PATCH — исправления без изменения контракта.
    
- Deprecated: срок поддержки + замена.
    

---

# Шаблон описания MCP Resources

Resources — это read-only контекст (схемы, каталоги, определения), который сильно повышает корректность интерпретации и выбора. ([Model Context Protocol](https://modelcontextprotocol.io/specification/draft/server/resources?utm_source=chatgpt.com "Resources"))

## 0) Заголовок

**Resource URI:** `dt://catalogs/metrics`  
**MIME type:** `application/json` (или `text/markdown`)  
**Статус:** draft | stable | deprecated  
**Версия:** `v1`  
**Дата обновления:** YYYY-MM-DD  
**Владелец:** команда ЦД

---

## 1) Назначение (Intent)

Коротко: что это и зачем модели/клиенту читать.

Пример: “Каталог метрик Цифрового двойника: определения, единицы, правила агрегации, типичные сценарии использования и ограничения.”

---

## 2) Структура (schema / формат)

Если JSON — дайте schema или хотя бы пример структуры.

```json
{
  "metrics": [
    {
      "id": "time_invested_minutes",
      "title": "Инвестированное время",
      "unit": "minutes",
      "definition": "…",
      "aggregation_rules": ["sum_by_day", "sum_by_period"],
      "exclusions": ["…"],
      "recommended_tools": ["dt.get_time_invested_summary"],
      "notes": "…"
    }
  ]
}
```

---

## 3) Свежесть и изменчивость

- Частота обновления: редко / часто.
    
- Нужны ли подписки (subscriptions) или кэширование. ([MCP Protocol](https://modelcontextprotocol.info/docs/concepts/resources/?utm_source=chatgpt.com "Resources"))
    
- TTL/etag (если используете).
    

---

## 4) Ограничения доступа

- кто может читать (scope), есть ли персональные данные (желательно избегать в resources).
    

---

## 5) Примеры использования

- “Если агент не уверен, что такое ‘инвестированное время’, он должен сначала прочитать `dt://catalogs/metrics`, затем вызвать tool”.
    

---

# Минимальный “базовый пакет” resources для вашего ЦД

1. `dt://catalogs/metrics` — каталог метрик (определения/единицы/агрегации).
    
2. `dt://schemas/activity_event` — схема события активности (поля, допустимые значения).
    
3. `dt://catalogs/activity_types` — типы активностей и их смысл.
    
4. `dt://policies/data_quality` — что значит coverage/confidence и пороги.
    
5. `dt://changelog` — изменения контрактов (для отладки и поддержки клиентов).
    

---

# Минимальный “базовый пакет” tools для старта (хорошо ложится на вашу дорожную карту)

1. `dt.get_time_invested_summary` — агрегаты времени + quality.
    
2. `dt.get_data_coverage` — отдельный tool для диагностики “есть ли данные”.
    
3. `dt.list_work_products` — список рабочих продуктов за период (без оценок качества).
    
4. `dt.list_activity_events` — сырые события (для дебага/проверки).
    

Рекомендация MCP — держать tools атомарными и хорошо документированными, а контекст (определения/схемы) отдавать ресурсами. ([MCP Protocol](https://modelcontextprotocol.info/docs/concepts/tools/?utm_source=chatgpt.com "Tools"))

---

Если вы хотите, следующим шагом я могу:

- взять ваш текущий сценарий “время за неделю/среднее за день” и оформить **конкретный** `dt.get_time_invested_summary` + `dt://catalogs/metrics` по этому шаблону (как эталон для команды),
    
- и одновременно предложить единый стандарт `data_quality` для всех будущих метрик.