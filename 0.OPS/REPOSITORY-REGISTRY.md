# Реестр репозиториев экосистемы

> **Source-of-truth** для списка репозиториев экосистемы развития интеллекта.
> Обновляется при создании/удалении репозиториев.

## Типы репозиториев (4 типа)

| Тип | Критерий | Source-of-truth |
|-----|----------|-----------------|
| **Pack** | Source-of-truth области (что истинно и как проверять) | Да |
| **Framework** | Рамки корректности (FPF/SPF) | Да |
| **Format** | Протокол оформления | Да (для формата) |
| **Downstream** | Производные от Pack | Нет |

### Подтипы Downstream

| Подтип | Что делает |
|--------|------------|
| `instrument` | Код, сервисы, MCP, боты |
| `governance` | Управление, планы, реестры |
| `surface` | Курсы, гайды, документация |

---

## Pack (Source-of-truth областей)

| Репозиторий | Область | Владелец | Статус |
|-------------|---------|----------|--------|
| [spf-personal-pack](https://github.com/aisystant/spf-personal-pack) | Созидатель (персональное развитие) | aisystant | Active |
| [spf-ecosystem-pack](https://github.com/TserenTserenov/spf-ecosystem-pack) | Экосистема развития интеллекта | TserenTserenov | Active |
| [spf-digital-platform-pack](https://github.com/TserenTserenov/spf-digital-platform-pack) | ИТ-платформа и цифровой двойник | TserenTserenov | Active |

---

## Framework (Рамки корректности)

| Репозиторий | Роль | Владелец | Статус |
|-------------|------|----------|--------|
| [SPF](https://github.com/TserenTserenov/SPF) | Second Principles Framework | TserenTserenov | Active |
| [FPF](https://github.com/ailev/FPF) | First Principles Framework | ailev | External |

---

## Format (Протоколы оформления)

| Репозиторий | Роль | Владелец | Статус |
|-------------|------|----------|--------|
| [s2r](https://github.com/TserenTserenov/s2r) | Structured Second-level Repository | TserenTserenov | Active |

---

## Downstream/instrument (Код и сервисы)

| Репозиторий | Назначение | Upstream pack | Статус |
|-------------|------------|---------------|--------|
| [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | MCP-сервис цифрового двойника | spf-digital-platform-pack, spf-personal-pack | Active |
| [aist_bot](https://github.com/aisystant/aist_bot) | Telegram-бот марафона | spf-personal-pack | Active |

---

## Downstream/governance (Управление)

| Репозиторий | Назначение | Upstream packs | Статус |
|-------------|------------|----------------|--------|
| [ecosystem-development](https://github.com/aisystant/ecosystem-development) | Координация экосистемы | spf-ecosystem-pack, spf-personal-pack, spf-digital-platform-pack | Active |

---

## Downstream/surface (Курсы и гайды)

| Репозиторий | Назначение | Upstream pack | Статус |
|-------------|------------|---------------|--------|
| [docs](https://github.com/aisystant/docs) | VitePress документация | spf-personal-pack | Active |

---

## Граф зависимостей

```
FPF (ailev)
  │
  └──▶ SPF (Framework)
        │
        ├──▶ spf-personal-pack (Pack: созидатель)
        │     │
        │     ├──▶ aist_bot (Downstream/instrument)
        │     ├──▶ digital-twin-mcp (Downstream/instrument)
        │     └──▶ docs (Downstream/surface)
        │
        ├──▶ spf-ecosystem-pack (Pack: экосистема)
        │     │
        │     └──▶ ecosystem-development (Downstream/governance)
        │
        ├──▶ spf-digital-platform-pack (Pack: ИТ-платформа)
        │     │
        │     └──▶ digital-twin-mcp (Downstream/instrument)
        │
        └──▶ s2r (Format)
              │
              └──▶ ecosystem-development (Downstream/governance)
```

---

## Обязательный контракт

Каждый репозиторий экосистемы **ДОЛЖЕН** иметь:

### 1. Признак типа в README.md (первая строка после заголовка)

```markdown
> **Тип репозитория:** `Pack` | `Framework` | `Format` | `Downstream/instrument` | `Downstream/governance` | `Downstream/surface`
```

### 2. Файл `REPO-TYPE.md` с полями:

```markdown
# Тип репозитория

**Тип**: `Pack` | `Framework` | `Format` | `Downstream/instrument` | `Downstream/governance` | `Downstream/surface`

**Source-of-truth**: yes | no

## Upstream dependencies
- Список зависимостей

## Downstream outputs
- Что потребляет этот репозиторий

## Non-goals
- Что НЕ входит в scope
```

---

## Правила

1. **Pack — единственный source-of-truth**. Downstream меняется вслед за pack
2. **Один репозиторий — один тип**. Не смешивать pack и downstream
3. **При изменении pack** — обновить downstream
4. **При добавлении репозитория** — обновить этот реестр
5. **При удалении репозитория** — обновить этот реестр

---

*Последнее обновление: 2026-02-06*
