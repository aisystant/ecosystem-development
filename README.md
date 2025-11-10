# ecosystem-development
Канонический репозиторий экосистемы: идеи изменения мира, целевые системы для людей, и метасистема их создания.
## Слои
- `content/` — человеческий слой (синхронизируется с Obsidian).
- `artifacts/` — выходы ИИ до ревью.
- `agents-core/` — код/манифесты (Apps SDK / MCP).
- `contracts/` — форматы интерфейсов и правила обмена.

## Правила
- `main` — защищена: изменения только через PR.
- Агенты создают ветки `ai/<agent>/<YYYY-MM-DD>` → PR в `main`.
- Только человек переносит утверждённое из `artifacts/` в `content/`.

## Поток
Obsidian → `content/` → (Агенты) → `artifacts/` → PR → ревью → `content/`.

## Родственные репозитории
- `ecosystem-development` (этот, канон)
- `agents-core` (код агентов / manifests)
- `ecosystem-platform` (исполняемые сервисы)
