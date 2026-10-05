import difflib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

ROOT_FOLDER = Path(__file__).parent.absolute()
WORK_DIR = ROOT_FOLDER / ".translation_work"

ENTRY_RE = re.compile(
    r'^    "(?P<key>[^"]+)": \{\n'
    r'        "name": (?P<name>"(?:[^"\\]|\\.)*"),\n'
    r'        "doc": (?P<doc>"(?:[^"\\]|\\.)*"),\n'
    r'        "sha256": "(?P<sha256>[0-9a-f]{64})"\n'
    r"    \}",
    re.MULTILINE,
)
ARGUMENT_HEADING_RE = re.compile(
    r"[*_]*(args|arguments|parameters)[*_]*::?[*_]*(\s+.*)?", re.IGNORECASE
)
ARGUMENT_ITEM_RE = re.compile(r"^  - ``(?P<name>[^`]+)``: ")
CODE_SPAN_RE = re.compile(r"``(?:(?!``).)+``")
URL_RE = re.compile(r"https?://[^\s|\]]+")
MIN_CONTINUATION = 4
WARNINGS = ("code spans missing", "URLs missing", "argument docs missing")
LOCALIZED_HEADING_RE = re.compile(r"^\*[^*\s][^*]*:\*$", re.MULTILINE)


def spec(version: str) -> dict:
    spec_file = WORK_DIR / f"spec_{version}.json"
    if not spec_file.exists():
        venv = WORK_DIR / f"venv_{version}"
        python = venv / "bin" / "python"
        if not python.exists():
            subprocess.run(
                ["uv", "venv", "--quiet", "--python", "3.12", str(venv)], check=True
            )
            subprocess.run(
                [
                    "uv",
                    "pip",
                    "install",
                    "--quiet",
                    "--python",
                    str(python),
                    f"robotframework-browser=={version}",
                ],
                check=True,
            )
        subprocess.run(
            [str(python), "-m", "Browser.entry", "translation", str(spec_file)],
            check=True,
        )
    return json.loads(spec_file.read_text(encoding="utf-8"))


def _canonical(doc: str) -> list[str]:
    words = []
    for line in doc.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"\|\s*=[^|]*=\s*\|\s*=[^|]*=\s*\|", stripped):
            continue
        if ARGUMENT_HEADING_RE.fullmatch(stripped):
            continue
        stripped = re.sub(r"^- ", "", stripped)
        stripped = stripped.replace("|", " ").replace("``", "").replace("`", "")
        stripped = stripped.replace("&", " ")
        words.extend(stripped.split())
    return [word.rstrip(":") for word in words]


@dataclass
class ReleaseChanges:
    diff_dir: Path
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    checksum_only_changes: list[str] = field(default_factory=list)
    formatting_changes: list[str] = field(default_factory=list)
    genuine_changes: list[str] = field(default_factory=list)
    off_baseline: dict[str, list[str]] = field(default_factory=dict)


def compare_releases(
    baseline: str, target: str, translations: dict[str, Path]
) -> ReleaseChanges:
    old, new = spec(baseline), spec(target)
    result = ReleaseChanges(WORK_DIR / f"changes_{baseline}_{target}")
    shutil.rmtree(result.diff_dir, ignore_errors=True)
    result.diff_dir.mkdir(parents=True)
    result.added = sorted(set(new) - set(old))
    result.removed = sorted(set(old) - set(new))
    for keyword in sorted(set(old) & set(new)):
        old_doc, new_doc = old[keyword]["doc"], new[keyword]["doc"]
        if old[keyword]["sha256"] == new[keyword]["sha256"]:
            result.unchanged.append(keyword)
            continue
        if old_doc == new_doc:
            result.checksum_only_changes.append(keyword)
            continue
        if _canonical(old_doc) == _canonical(new_doc):
            result.formatting_changes.append(keyword)
        else:
            result.genuine_changes.append(keyword)
        (result.diff_dir / f"{keyword}.diff").write_text(
            "".join(
                difflib.unified_diff(
                    old_doc.splitlines(keepends=True),
                    new_doc.splitlines(keepends=True),
                    f"{baseline}/{keyword}",
                    f"{target}/{keyword}",
                )
            ),
            encoding="utf-8",
        )
    for language, path in translations.items():
        entries = read_entries(path)
        result.off_baseline[language] = sorted(
            key
            for key, entry in entries.items()
            if key in old and entry["sha256"] != old[key]["sha256"]
        )
    return result


def read_entries(path: Path) -> dict[str, dict[str, str]]:
    return _parse_entries(path.read_text(encoding="utf-8"), path)


def _parse_entries(text: str, path: Path) -> dict[str, dict[str, str]]:
    entries = {
        match["key"]: {
            "name": json.loads(match["name"]),
            "doc": json.loads(match["doc"]),
            "sha256": match["sha256"],
        }
        for match in ENTRY_RE.finditer(text)
    }
    if entries != json.loads(text):
        raise ValueError(f"{path} is not in the expected entry layout")
    return entries


def _uses_ascii_escapes(text: str) -> bool:
    return text.count("\\u") >= sum(1 for char in text if not char.isascii())


def _render_entry(key: str, entry: dict[str, str], ascii_only: bool) -> str:
    def dump(value: str) -> str:
        return json.dumps(value, ensure_ascii=ascii_only)

    return (
        f"    {dump(key)}: {{\n"
        f'        "name": {dump(entry["name"])},\n'
        f'        "doc": {dump(entry["doc"])},\n'
        f'        "sha256": "{entry["sha256"]}"\n'
        "    }"
    )


def write_entries(path: Path, updates: dict[str, dict[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    ascii_only = _uses_ascii_escapes(text)
    current = _parse_entries(text, path)

    def replace(match: re.Match) -> str:
        key = match["key"]
        if key not in updates or updates[key] == current[key]:
            return match[0]
        return _render_entry(key, updates[key], ascii_only)

    text = ENTRY_RE.sub(replace, text)
    new_keys = [key for key in updates if key not in current]
    if new_keys:
        blocks = ",\n".join(
            _render_entry(key, updates[key], ascii_only) for key in new_keys
        )
        head, tail = text.rstrip().rsplit("\n}", 1)
        text = f"{head},\n{blocks}\n}}{tail}\n"
    if _parse_entries(text, path) != {**current, **updates}:
        raise ValueError(f"{path} would not round-trip, nothing written")
    path.write_text(text, encoding="utf-8")


def argument_section(doc: str) -> tuple[bool, list[str], list[str]]:
    lines = doc.splitlines()
    for index, line in enumerate(lines):
        if not ARGUMENT_HEADING_RE.fullmatch(line.strip()) or line[:1].isspace():
            continue
        names, problems = [], []
        if index and lines[index - 1].strip():
            problems.append("no blank line before the argument heading")
        for item in lines[index + 1 :]:
            if item and not item[:2].isspace():
                break
            match = ARGUMENT_ITEM_RE.match(item)
            if match:
                names.append(match["name"])
            elif item.strip() and len(item) - len(item.lstrip()) < MIN_CONTINUATION:
                problems.append(f"shallow continuation line: {item.strip()[:60]}")
        return True, names, problems
    return False, [], []


def _argument_name(name: str) -> str:
    return name.strip().strip("`").lstrip("*").split("=")[0]


def _first_table_cells(doc: str) -> list[str]:
    return [
        line.strip().strip("|").split("|")[0]
        for line in doc.splitlines()
        if line.lstrip().startswith("|")
    ]


def _markup_problems(english: str, translated: str) -> list[str]:
    problems = [
        f"suffix glued to code span: {match[0]}"
        for match in CODE_SPAN_RE.finditer(translated)
        if re.match(r"[-\w]", translated[match.end() :])
    ]
    if translated.count("``") % 2:
        problems.append("unbalanced ``")
    if english.startswith("*DEPRECATED") != translated.startswith("*DEPRECATED"):
        problems.append("*DEPRECATED* marker differs from English")
    return problems


def _argument_problems(english: str, translated: str) -> list[str]:
    has_en, names_en, _ = argument_section(english)
    has_tr, names_tr, problems = argument_section(translated)
    if has_en and not has_tr:
        if LOCALIZED_HEADING_RE.search(translated):
            problems.append("argument heading is translated")
        else:
            problems.append("argument docs missing")
    allowed = {_argument_name(name) for name in names_en}
    table_names = allowed - {_argument_name(c) for c in _first_table_cells(english)}
    if any(_argument_name(c) in table_names for c in _first_table_cells(translated)):
        problems.append("old argument table still present")
    problems.extend(
        f"argument not in English section: {name}"
        for name in names_tr
        if _argument_name(name) not in allowed
    )
    if len(set(names_tr)) != len(names_tr):
        problems.append("duplicate argument item")
    return problems


def _coverage_problems(english: str, translated: str) -> list[str]:
    problems = []
    for label, pattern in (("code spans", CODE_SPAN_RE), ("URLs", URL_RE)):
        missing = sorted(
            set(pattern.findall(english)) - set(pattern.findall(translated))
        )
        if missing:
            problems.append(f"{label} missing: {', '.join(missing)}")
    return problems


def validate_entry(english: str, translated: str) -> list[str]:
    return [
        *_markup_problems(english, translated),
        *_argument_problems(english, translated),
        *_coverage_problems(english, translated),
    ]


def validate(path: Path, english: dict) -> dict[str, list[str]]:
    entries = read_entries(path)
    report = {}
    for key, entry in entries.items():
        if key not in english:
            report[key] = ["obsolete keyword"]
            continue
        problems = validate_entry(english[key]["doc"], entry["doc"])
        if entry["sha256"] != english[key]["sha256"]:
            problems.insert(0, "checksum differs from target")
        if problems:
            report[key] = problems
    for key in sorted(set(english) - set(entries)):
        report[key] = ["missing keyword"]
    return report


def is_error(problem: str) -> bool:
    return not problem.startswith(WARNINGS)
