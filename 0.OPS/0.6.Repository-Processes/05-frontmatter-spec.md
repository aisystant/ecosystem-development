---
type: spec
status: active
created: 2026-01-18
updated: 2026-01-18
family: F0
scope: repository
---

# Спецификация Frontmatter

## Формат

YAML-блок в начале документа, ограниченный `---`:

```yaml
---
field: value
list:
  - item1
  - item2
---
```

## Обязательные поля

### type

Тип документа.

```yaml
type: doc | spec | process | report | template
```

| Значение | Описание |
|----------|----------|
| `doc` | Описательный документ |
| `spec` | Спецификация, требования |
| `process` | Описание процесса |
| `report` | Отчёт, результат |
| `template` | Шаблон |

### status

Статус зрелости.

```yaml
status: stub | draft | active | archived
```

| Значение | Описание |
|----------|----------|
| `stub` | Заглушка, только заголовок |
| `draft` | Черновик, в работе |
| `active` | Актуальный, используется |
| `archived` | Архивный |

### created

Дата создания в формате ISO 8601.

```yaml
created: 2026-01-14
```

### updated

Дата последнего обновления.

```yaml
updated: 2026-01-14
```

## Рекомендуемые поля

### family

Код семейства документа.

```yaml
family: FA4    # Ядро A, семейство 4
family: FB9    # Ядро B, семейство 9
family: F0     # Управление хранилищем
```

### kernel

Буква ядра.

```yaml
kernel: A | B | C | ...
```

### system

Система в рамках ядра.

```yaml
system: Suprasystem | System-of-Interest | Constructor
```

### role

Роль (угол зрения).

```yaml
role: Meaning | Architecture | Operations
```

### scope

Область применимости.

```yaml
scope: local-edge | project | ecosystem | universal
```

### layer

Слой знаний.

```yaml
layer: methodology | architecture | operations | data
```

### related

Связанные документы.

```yaml
related:
  - ../path/to/doc1.md
  - ../path/to/doc2.md
```

### fpf_patterns

Связанные паттерны FPF.

```yaml
fpf_patterns:
  - A.1       # Holonic Foundation
  - A.1.1     # Bounded Context
  - B.3       # Trust Calculus
```

### target_audience

Целевая аудитория.

```yaml
target_audience:
  - developers
  - managers
  - ai-agents
```

### tags

Свободные теги для поиска.

```yaml
tags:
  - architecture
  - api
  - security
```

## Полный пример

```yaml
---
type: spec
status: active
created: 2026-01-14
updated: 2026-01-14
family: FA5
kernel: A
system: System-of-Interest
role: Architecture
scope: project
layer: architecture
related:
  - ../A2.1.Meaning/requirements.md
  - ../A2.3.Operations/deployment.md
fpf_patterns:
  - A.1
  - A.7
target_audience:
  - developers
  - architects
tags:
  - api
  - design
---
```

## Валидация

Frontmatter должен:
1. Начинаться с `---`
2. Заканчиваться `---`
3. Быть валидным YAML
4. Содержать все обязательные поля

## См. также

- [02-standards.md](02-standards.md) — стандарты оформления
- [04-document-creation.md](04-document-creation.md) — процесс создания
