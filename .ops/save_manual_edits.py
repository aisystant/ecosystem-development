#!/usr/bin/env python3
"""
Скрипт для сохранения ручных правок из таблицы в JSON

ВАЖНО: Работает на уровне ЯЧЕЕК, а не строк!

Использование:
    python .ops/save_manual_edits.py

Как это работает:
1. Читает таблицу из документа 0.6
2. Для КАЖДОЙ ячейки проверяет наличие эмодзи:
   - БЕЗ 🟡 = ручная правка, сохраняется
   - С 🟡 = AI-предложение, НЕ сохраняется
3. Сохраняет только измененные ячейки в .ops/manual_classifications.json
4. При следующем запуске classify_documents.py:
   - Зеленые ячейки 🟢 (ручные правки) НЕ ИЗМЕНЯТСЯ
   - Желтые ячейки 🟡 (AI) могут обновиться

Пример:
   Вы изменили только ячейку "audience" в строке 3.
   JSON будет:
   {
     "0. Управление/0.2. План работ.md": {
       "audience": "mixed"
     }
   }

   Только эта ячейка станет зеленой 🟢, остальные - желтые 🟡.
"""

import re
import json
from pathlib import Path
from typing import Dict, List

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"
STRUCTURE_DOC = CONTENT_DIR / "0. Управление" / "0.6. Структура этого хранилища.md"
MANUAL_EDITS_FILE = BASE_DIR / "ops" / "manual_classifications.json"


def extract_value_from_cell(cell: str) -> tuple[str, bool]:
    """
    Извлекает значение из ячейки и определяет, является ли оно ручной правкой

    Args:
        cell: содержимое ячейки

    Returns:
        Tuple (значение, is_manual)
        - is_manual=True если это 🟢 зеленый круг (ручная правка)
        - is_manual=False если это 🟡 желтый круг (AI-предложение)
    """
    cell = cell.strip()

    # Проверяем, есть ли желтый круг 🟡 (AI-предложение)
    if cell.startswith('🟡'):
        # Это AI-предложение, НЕ сохраняем
        value = cell.replace('🟡', '').strip()
        return value, False

    # Проверяем, есть ли зеленый круг 🟢 (ручная правка)
    if cell.startswith('🟢'):
        # Это ручная правка, сохраняем
        value = cell.replace('🟢', '').strip()
        return value, True

    # Обычный текст без эмодзи - это тоже ручная правка
    return cell, True


def save_manual_edits_from_table():
    """
    Извлекает ручные правки из таблицы и сохраняет в JSON

    ВАЖНО: Сохраняются только значения БЕЗ <mark> тегов!
    """
    # Проверяем, что скрипт запущен из корневой директории
    if not STRUCTURE_DOC.exists():
        print(f"❌ Документ не найден: {STRUCTURE_DOC}")
        print()
        print("⚠️  Возможно, скрипт запущен НЕ из корневой директории проекта!")
        print()
        print("📍 Правильно:")
        print(f"   cd {BASE_DIR}")
        print("   python3 .ops/save_manual_edits.py")
        print()
        print("❌ Неправильно:")
        print(f"   cd {BASE_DIR}/ops")
        print("   python3 save_manual_edits.py")
        return

    with open(STRUCTURE_DOC, 'r', encoding='utf-8') as f:
        content = f.read()

    # Находим таблицу классификации
    lines = content.split('\n')

    table_rows = []
    in_table = False

    for line in lines:
        # Начало таблицы
        if '| №' in line and '| Документ' in line and '| Type' in line:
            in_table = True
            continue

        # Разделитель таблицы (пропускаем)
        if in_table and line.strip().startswith('|') and '---' in line:
            continue

        # Конец таблицы
        if in_table and (line.startswith('**Итого') or line.startswith('---') or not line.strip()):
            if line.startswith('**Итого') or line.startswith('---'):
                break
            continue

        # Строки с данными
        if in_table and line.strip().startswith('|'):
            table_rows.append(line)

    if not table_rows:
        print("❌ Таблица классификации не найдена в документе 0.6")
        return

    # Парсим строки таблицы
    row_pattern = r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|'

    manual_edits = {}
    manual_count = 0
    ai_count = 0

    for row in table_rows:
        match = re.match(row_pattern, row)
        if not match:
            continue

        row_num = match.group(1)
        doc_name = match.group(2).strip()
        folder = match.group(3).strip()

        # Извлекаем значения и проверяем каждую ячейку отдельно
        type_val, type_manual = extract_value_from_cell(match.group(4))
        audience_val, audience_manual = extract_value_from_cell(match.group(5))
        edit_mode_val, edit_mode_manual = extract_value_from_cell(match.group(6))
        layer_val, layer_manual = extract_value_from_cell(match.group(7))
        scope_val, scope_manual = extract_value_from_cell(match.group(8))
        security_val, security_manual = extract_value_from_cell(match.group(9))

        # Определяем путь к документу
        doc_path = f"{folder}/{doc_name}"

        # НОВАЯ ЛОГИКА: Сохраняем ТОЛЬКО те ячейки, которые были изменены вручную
        doc_manual_edits = {}

        if type_manual:
            doc_manual_edits["type"] = type_val
            manual_count += 1
        if audience_manual:
            doc_manual_edits["audience"] = audience_val
            manual_count += 1
        if edit_mode_manual:
            doc_manual_edits["edit_mode"] = edit_mode_val
            manual_count += 1
        if layer_manual:
            doc_manual_edits["layer"] = layer_val
            manual_count += 1
        if scope_manual:
            doc_manual_edits["scope"] = scope_val
            manual_count += 1
        if security_manual:
            doc_manual_edits["security"] = security_val
            manual_count += 1

        # Если есть хотя бы одна ручная правка - сохраняем документ
        if doc_manual_edits:
            manual_edits[doc_path] = doc_manual_edits
            cells_list = ", ".join(doc_manual_edits.keys())
            print(f"✅ {doc_name}: {cells_list}")
            ai_count += (6 - len(doc_manual_edits))  # Остальные ячейки - AI
        else:
            ai_count += 6  # Все 6 ячеек - AI

    # Сохраняем в JSON
    with open(MANUAL_EDITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(manual_edits, f, ensure_ascii=False, indent=2)

    print()
    print(f"📊 Статистика:")
    print(f"  ✅ Ручных правок (зеленые ячейки): {manual_count}")
    print(f"  🤖 AI-предложений (желтые ячейки): {ai_count}")
    print(f"  📄 Документов с правками: {len(manual_edits)}")
    print()
    print(f"💾 Ручные правки сохранены в: {MANUAL_EDITS_FILE}")
    print()
    print("🔒 Защита данных:")
    print("  • Зеленые ЯЧЕЙКИ НИКОГДА не будут изменены AI")
    print("  • Желтые ячейки в той же строке могут обновиться AI")
    print("  • Только человек может изменить зеленые ячейки")
    print("  • При запуске classify_documents.py зеленые останутся зелеными")


def main():
    """Главная функция"""
    print("💾 Сохранение ручных правок из таблицы...\n")
    save_manual_edits_from_table()


if __name__ == "__main__":
    main()
