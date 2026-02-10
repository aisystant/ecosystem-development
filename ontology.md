# Онтология: Ecosystem Development

> **Тип:** Downstream-governance
> **Upstream:** spf-personal-pack, spf-ecosystem-pack, spf-digital-platform-pack
> **Базовая онтология:** [SPF/ontology.md](../SPF/ontology.md) (SPF.SPEC.002)
>
> Downstream ссылается на понятия Pack'ов и SPF. Новых онтологических понятий не вводит (SPF.SPEC.002 § 4.3).

---

## 1. Upstream-зависимости

| Уровень | Источник | Что используется |
|---------|----------|------------------|
| Pack | [spf-personal-pack](../spf-personal-pack/) | Знания о созидателе: характеристики, состояния, роли |
| Pack | [spf-ecosystem-pack](../spf-ecosystem-pack/) | Знания об экосистеме: компоненты, бесшовность, переходы |
| Pack | [spf-digital-platform-pack](../spf-digital-platform-pack/) | Архитектура платформы, агенты, MCP |
| SPF | [SPF/ontology.md](../SPF/ontology.md) | Базовая онтология (U.*) |
| FPF | Через SPF | Мета-онтология |

---

## 2. Используемые понятия из Pack

### Ядро A (Созидатель) ← spf-personal-pack

| Понятие | FPF-понятие | Как используется |
|---------|-------------|------------------|
| Созидатель | U.System | SoI ядра A — объект развития |
| Характеристика | U.Characteristic | Оси оценки созидателя |
| Состояние | U.Flow | Текущий этап развития |
| Роль | U.RoleAssignment | Контекстная функция созидателя |
| Программа развития | U.MethodDescription | Рецепт развития |

### Ядро B (Экосистема) ← spf-ecosystem-pack

| Понятие | FPF-понятие | Как используется |
|---------|-------------|------------------|
| Экосистема | U.System | SoI ядра B — среда развития |
| Компонент экосистемы | U.Holon | Часть экосистемы (ресурс, сервис, сообщество) |
| Бесшовность | U.Characteristic | Критерий качества переходов |
| Путь развития | U.Flow | Траектория от новичка до мастера |
| Точка входа | U.Boundary + U.Interaction | Начало взаимодействия с экосистемой |

### Ядро C (ИТ-платформа) ← spf-digital-platform-pack

| Понятие | FPF-понятие | Как используется |
|---------|-------------|------------------|
| Цифровая платформа | U.System | SoI ядра C — техническая реализация |
| ИИ-система | U.System + U.Capability | Агенты и инструменты |
| Цифровой двойник | U.System + U.Episteme | Модель созидателя в платформе |
| MCP-сервис | U.System + U.Interaction | Инструменты интеграции |

---

## 3. Терминология governance

| Термин в governance | Понятие Pack/SPF | Описание |
|---------------------|------------------|----------|
| Ядро (A, B, C) | U.BoundedContext | Семантическая рамка вокруг системы интереса |
| Семейство (F1-F9) | U.Episteme | Тип документа в матрице 3×3 |
| Source-of-truth | — | Pack как единственный источник знания |
| Реестр | — | Governance-список объектов со ссылками на Pack |

---

## 4. Связанные документы

- [spf-personal-pack/ontology.md](../spf-personal-pack/ontology.md) — онтология ядра A
- [spf-ecosystem-pack/ontology.md](../spf-ecosystem-pack/ontology.md) — онтология ядра B
- [spf-digital-platform-pack/ontology.md](../spf-digital-platform-pack/ontology.md) — онтология ядра C
- [SPF/ontology.md](../SPF/ontology.md) — базовая онтология (SPF.SPEC.002)
