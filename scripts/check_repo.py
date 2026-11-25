"""Проверка версионируемой конфигурации Cline.

Зачем. `~/.cline` содержит и переиспользуемые скилы, и приватные материалы
компаний, и runtime-данные. Git-репозиторий должен включать только текст
скилов/правил/команд, а перед публикацией — не содержать личных путей,
секретов и названий компаний.

Проверяется:

1. `registry.json` покрывает все `SKILL.md`, workflows и rules;
2. у каждого скила есть frontmatter `name` и `description`;
3. git не отслеживает `data/`, `logs/`, `memory/`, `tmp/`, `hooks/`, `*.pem`;
4. в `public`-элементах нет личных путей, токенов и company-specific маркеров.

Запуск: `python3 scripts/check_repo.py` или `make check`.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "registry.json"

#: Каталоги и файлы, которые не должны попадать в git.
FORBIDDEN_TRACKED_PREFIXES = ("data/", "logs/", "memory/", "tmp/", "hooks/")
FORBIDDEN_TRACKED_SUFFIXES = (".pem", ".env")

#: Признаки, недопустимые в public-элементах.
PATTERNS: dict[str, re.Pattern[str]] = {
    "personal path": re.compile(r"/home/[A-Za-z0-9._-]+"),
    "author handle": re.compile(r"\bmaxbogus\b", re.IGNORECASE),
    "billing-me": re.compile(r"billing[-_. ]?me", re.IGNORECASE),
    "vulnshop": re.compile(r"vulnshop", re.IGNORECASE),
    "syneps": re.compile(r"syneps", re.IGNORECASE),
    "company": re.compile(r"Семьсот дорог", re.IGNORECASE),
    "private key": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    "github token": re.compile(r"\b(?:ghp|gho|ghs)_[A-Za-z0-9]{20,}\b"),
    "aws key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}


def _load_registry(path: Path) -> dict[str, object]:
    """Прочитать registry.json.

    Args:
        path: Путь к файлу реестра.

    Returns:
        Словарь реестра.

    Raises:
        ValueError: Если файл не является JSON-объектом.
    """
    loaded: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: ожидался JSON-объект")
    return loaded


def _entries(registry: dict[str, object], key: str) -> list[dict[str, object]]:
    """Вернуть список записей реестра.

    Args:
        registry: Реестр.
        key: `skills`, `workflows` или `rules`.

    Returns:
        Список записей (пустой, если раздела нет).
    """
    value = registry.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _frontmatter(text: str) -> dict[str, str]:
    """Разобрать простой YAML frontmatter без внешних зависимостей.

    Args:
        text: Содержимое `SKILL.md`.

    Returns:
        Пары ключ → значение (многострочные значения склеены пробелом).
    """
    match = re.match(r"\A(?:\s*<!--.*?-->\s*)?---\s*\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    data: dict[str, str] = {}
    key: str | None = None
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if line[:1].isspace() and key:
            data[key] = (data[key] + " " + line.strip()).strip()
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            data[key] = "" if value in ("|", ">") else value.strip("\"'")
    return data


def _tracked_files() -> list[str]:
    """Вернуть файлы, отслеживаемые git в этом каталоге.

    Returns:
        Пути от корня `~/.cline`; пустой список, если git ещё не инициализирован.
    """
    try:
        completed = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line for line in completed.stdout.splitlines() if line]


def _scan(text: str) -> list[str]:
    """Найти недопустимые маркеры в тексте.

    Args:
        text: Содержимое файла.

    Returns:
        Список найденных маркеров.
    """
    found: list[str] = []
    for name, pattern in PATTERNS.items():
        match = pattern.search(text)
        if match:
            found.append(f"{name}: {match.group(0)[:40]!r}")
    return found


def check_repo(root: Path = REPO_ROOT) -> tuple[list[str], list[str]]:
    """Проверить реестр, покрытие и содержимое.

    Args:
        root: Корень `~/.cline`.

    Returns:
        Кортеж `(errors, warnings)`.
    """
    errors: list[str] = []
    warnings: list[str] = []
    registry = _load_registry(root / "registry.json")
    entries = {
        "skills": _entries(registry, "skills"),
        "workflows": _entries(registry, "workflows"),
        "rules": _entries(registry, "rules"),
    }

    expected = {
        "skills": {
            f"skills/{path.parent.name}/SKILL.md"
            for path in (root / "skills").glob("*/SKILL.md")
        },
        "workflows": {
            f"workflows/{path.name}" for path in (root / "workflows").glob("*.md")
        },
        "rules": {f"rules/{path.name}" for path in (root / "rules").glob("*.md")},
    }
    for kind in ("skills", "workflows", "rules"):
        declared = {str(item.get("path")) for item in entries[kind]}
        for path in sorted(expected[kind] - declared):
            errors.append(f"REGISTRY MISSING: {kind}: {path}")
        for path in sorted(declared - expected[kind]):
            errors.append(f"REGISTRY STALE: {kind}: {path}")

    for item in entries["skills"]:
        path = root / str(item.get("path"))
        text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
        meta = _frontmatter(text)
        if not meta.get("name"):
            errors.append(f"FRONTMATTER: {path}: нет name")
        if not meta.get("description"):
            errors.append(f"FRONTMATTER: {path}: нет description")

    for kind in ("skills", "workflows", "rules"):
        for item in entries[kind]:
            path = root / str(item.get("path"))
            if not path.is_file():
                continue
            visibility = str(item.get("visibility", "private"))
            for marker in _scan(path.read_text(encoding="utf-8", errors="replace")):
                message = f"{visibility.upper()}: {path}: {marker}"
                if visibility == "public":
                    errors.append(message)
                else:
                    warnings.append(message)

    for path in _tracked_files():
        if path.startswith(FORBIDDEN_TRACKED_PREFIXES) or path.endswith(
            FORBIDDEN_TRACKED_SUFFIXES
        ):
            errors.append(f"TRACKED RUNTIME FILE: {path}")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    """Точка входа CLI.

    Args:
        argv: Аргументы командной строки.

    Returns:
        0 — ошибок нет; 1 — есть ошибки.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)
    errors, warnings = check_repo(args.root.resolve())

    if warnings:
        print(f"check: {len(warnings)} warning(s)")
        for warning in warnings:
            print(f"  WARN {warning}")
    if errors:
        print(f"check: {len(errors)} error(s)")
        for error in errors:
            print(f"  FAIL {error}")
        return 1
    print("check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
