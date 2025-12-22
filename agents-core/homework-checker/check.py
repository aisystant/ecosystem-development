#!/usr/bin/env python3
"""
ДЗ-чекер: проверка домашних заданий с использованием LLM.

Использование:
    python3 check.py --input answer.json --output result.json
    python3 check.py --input answers_batch.json --output results_batch.json --batch
    cat answer.json | python3 check.py --output result.json
"""

import argparse
import json
import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


# Корень агента
AGENT_ROOT = Path(__file__).parent
DEFAULT_CONFIG = AGENT_ROOT / "config.yaml"


def load_config(config_path: Path = DEFAULT_CONFIG) -> dict:
    """Загрузка конфигурации."""
    local_config = config_path.parent / "config.local.yaml"
    if local_config.exists():
        config_path = local_config

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_questions_map(config: dict) -> dict:
    """Загрузка карты вопросов."""
    path = AGENT_ROOT / config["paths"]["questions_map"]
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_rubrics(config: dict) -> dict:
    """Загрузка рубрик."""
    path = AGENT_ROOT / config["paths"]["rubrics"]
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompts(config: dict) -> dict:
    """Загрузка промптов."""
    prompts_dir = AGENT_ROOT / config["paths"]["prompts_dir"]
    prompts = {}

    system_prompt = prompts_dir / "system.txt"
    if system_prompt.exists():
        prompts["system"] = system_prompt.read_text(encoding="utf-8")

    check_template = prompts_dir / "check_template.txt"
    if check_template.exists():
        prompts["check_template"] = check_template.read_text(encoding="utf-8")

    return prompts


def find_question_context(question_id: str, course_id: str, questions_map: dict) -> Optional[dict]:
    """Поиск контекста вопроса в карте."""
    courses = questions_map.get("courses", {})
    course = courses.get(course_id, {})
    questions = course.get("questions", {})

    if question_id in questions:
        question_data = questions[question_id]
        return {
            "question_id": question_id,
            "guide_root": course.get("guide_root", ""),
            **question_data
        }

    # Поиск по всем курсам, если course_id не указан
    for cid, course_data in courses.items():
        questions = course_data.get("questions", {})
        if question_id in questions:
            return {
                "question_id": question_id,
                "guide_root": course_data.get("guide_root", ""),
                **questions[question_id]
            }

    return None


def get_rubric(rubric_id: str, rubrics: dict) -> Optional[dict]:
    """Получение рубрики по ID."""
    return rubrics.get("rubrics", {}).get(rubric_id)


def load_normative_content(question_context: dict, config: dict) -> str:
    """Загрузка нормативного контента из репозитория."""
    guides_root = AGENT_ROOT / config["paths"]["guides_root"]
    guide_root = question_context.get("guide_root", "")
    guide_path = question_context.get("guide_path", "")

    full_path = guides_root / guide_root / guide_path

    if not full_path.exists():
        return f"[Норматив не найден: {full_path}]"

    content = full_path.read_text(encoding="utf-8")

    # TODO: Извлечь конкретный раздел по guide_section
    # Пока возвращаем весь файл (для MVP)
    section = question_context.get("guide_section", "")
    if section:
        content = f"Раздел: {section}\n\n{content}"

    return content


def format_rubric_for_prompt(rubric: dict) -> str:
    """Форматирование рубрики для промпта."""
    if not rubric:
        return "[Рубрика не найдена]"

    lines = [f"### {rubric['name']}\n"]
    lines.append(f"Проходной балл: {rubric.get('passing_score', 60)}/100\n")
    lines.append("Критерии:\n")

    for criterion in rubric.get("criteria", []):
        lines.append(f"- **{criterion['name']}** (вес: {criterion['weight']})")
        lines.append(f"  {criterion['description']}")

    return "\n".join(lines)


def build_llm_request(
    request: dict,
    question_context: dict,
    normative_content: str,
    rubric: dict,
    prompts: dict,
    config: dict
) -> dict:
    """Сборка запроса к LLM."""

    check_prompt = prompts.get("check_template", "")

    # Подставляем переменные
    user_content = check_prompt.format(
        question_text=request["question"]["text"],
        answer_text=request["answer"]["text"],
        normative_content=normative_content[:8000],  # Ограничение размера
        rubric_criteria=format_rubric_for_prompt(rubric)
    )

    return {
        "model": config["llm"]["model"],
        "max_tokens": config["llm"]["max_tokens"],
        "temperature": config["llm"]["temperature"],
        "messages": [
            {
                "role": "system",
                "content": prompts.get("system", "")
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    }


def call_llm(llm_request: dict, config: dict) -> dict:
    """Вызов LLM API."""
    provider = config["llm"]["provider"]

    # TODO: Реализовать вызовы к реальным API
    # Для MVP возвращаем заглушку

    print(f"[INFO] Вызов {provider} API с моделью {llm_request['model']}", file=sys.stderr)
    print(f"[INFO] Промпт: {len(llm_request['messages'][1]['content'])} символов", file=sys.stderr)

    # Заглушка — в реальности здесь будет вызов API
    return {
        "verdict": "needs_revision",
        "score": 75,
        "strengths": [
            "Ответ содержит ключевую идею",
            "Приведён собственный пример"
        ],
        "issues": [
            {
                "criterion": "terminology",
                "issue": "Терминология курса использована не полностью",
                "suggestion": "Рекомендуется использовать термины из материалов"
            }
        ],
        "next_step": "Перечитайте раздел о терминологии и дополните ответ",
        "criterion_scores": {
            "main_idea": 35,
            "own_example": 25,
            "terminology": 10,
            "completeness": 5
        }
    }


def check_answer(request: dict, config: dict, questions_map: dict, rubrics: dict, prompts: dict) -> dict:
    """Основная функция проверки одного ответа."""

    question_id = request["question"]["id"]
    course_id = request["question"].get("course_id", "")

    # 1. Найти контекст вопроса
    question_context = find_question_context(question_id, course_id, questions_map)
    if not question_context:
        return {
            "error": f"Вопрос {question_id} не найден в карте вопросов",
            "attempt_id": request.get("attempt_id")
        }

    # 2. Загрузить рубрику
    rubric_id = question_context.get("rubric_id")
    rubric = get_rubric(rubric_id, rubrics) if rubric_id else None

    # 3. Загрузить норматив
    normative_content = load_normative_content(question_context, config)

    # 4. Собрать запрос к LLM
    llm_request = build_llm_request(
        request, question_context, normative_content, rubric, prompts, config
    )

    # 5. Вызвать LLM
    llm_result = call_llm(llm_request, config)

    # 6. Обогатить результат метаданными
    result = {
        **llm_result,
        "attempt_id": request.get("attempt_id"),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "model_used": config["llm"]["model"],
        "guide_reference": {
            "path": question_context.get("guide_path"),
            "section": question_context.get("guide_section")
        }
    }

    return result


def format_result_markdown(result: dict, config: dict) -> str:
    """Форматирование результата в Markdown."""
    verdicts = config.get("verdicts", {})
    verdict_info = verdicts.get(result.get("verdict", "unknown"), {})

    strengths_list = "\n".join(f"- {s}" for s in result.get("strengths", []))

    issues_list = ""
    for issue in result.get("issues", []):
        issues_list += f"- **{issue['criterion']}**: {issue['issue']}\n"
        issues_list += f"  _Рекомендация: {issue['suggestion']}_\n"

    if not issues_list:
        issues_list = "- Замечаний нет"

    model_info = f"Проверено: {result.get('model_used', 'N/A')}"
    ref = result.get("guide_reference", {})
    reference_info = f"По материалам: {ref.get('section', 'N/A')}"

    template = config.get("output", {}).get("markdown_template", "")

    return template.format(
        verdict_emoji=verdict_info.get("emoji", "?"),
        verdict_text=verdict_info.get("text", result.get("verdict")),
        score=result.get("score", 0),
        strengths_list=strengths_list or "- Не выявлено",
        issues_list=issues_list,
        next_step=result.get("next_step", ""),
        model_info=model_info,
        reference_info=reference_info
    )


def main():
    parser = argparse.ArgumentParser(description="ДЗ-чекер: проверка домашних заданий")
    parser.add_argument("--input", "-i", type=str, help="Входной JSON-файл")
    parser.add_argument("--output", "-o", type=str, help="Выходной файл (JSON или Markdown)")
    parser.add_argument("--config", "-c", type=str, help="Путь к конфигурации")
    parser.add_argument("--batch", "-b", action="store_true", help="Batch-режим (массив запросов)")
    parser.add_argument("--format", "-f", choices=["json", "markdown"], help="Формат вывода")
    parser.add_argument("--dry-run", action="store_true", help="Показать запрос без вызова LLM")

    args = parser.parse_args()

    # Загрузка конфигурации
    config_path = Path(args.config) if args.config else DEFAULT_CONFIG
    config = load_config(config_path)

    # Загрузка данных
    questions_map = load_questions_map(config)
    rubrics = load_rubrics(config)
    prompts = load_prompts(config)

    # Чтение входных данных
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            input_data = json.load(f)
    else:
        input_data = json.load(sys.stdin)

    # Обработка
    if args.batch:
        results = [check_answer(req, config, questions_map, rubrics, prompts) for req in input_data]
    else:
        results = check_answer(input_data, config, questions_map, rubrics, prompts)

    # Форматирование вывода
    output_format = args.format or config.get("output", {}).get("format", "json")

    if output_format == "markdown":
        if args.batch:
            output_text = "\n\n---\n\n".join(format_result_markdown(r, config) for r in results)
        else:
            output_text = format_result_markdown(results, config)
    else:
        output_text = json.dumps(results, ensure_ascii=False, indent=2)

    # Запись результата
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"[INFO] Результат записан в {args.output}", file=sys.stderr)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
