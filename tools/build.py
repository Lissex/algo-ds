"""Собирает assets/code.js из .py файлов в папке code/.

Запуск (из корня проекта):  python tools/build.py
Нужно перезапускать после любого изменения .py файлов.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE = ROOT / "code"

files = {}
snippets = {}

for path in sorted(CODE.rglob("*.py")):
    rel = path.relative_to(CODE).as_posix()
    src = path.read_text(encoding="utf-8")
    files[rel] = src
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            snippets[f"{rel}::{node.name}"] = ast.get_source_segment(src, node)
        if isinstance(node, ast.ClassDef):
            snippets[f"{rel}::{node.name}"] = ast.get_source_segment(src, node)
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    seg = ast.get_source_segment(src, item, padded=True)
                    snippets[f"{rel}::{node.name}.{item.name}"] = (
                        "\n".join(line[4:] if line.startswith("    ") else line
                                  for line in seg.splitlines())
                    )

out = ROOT / "assets" / "code.js"
out.write_text(
    "// Сгенерировано tools/build.py — не редактируйте вручную.\n"
    "window.CODE = " + json.dumps({"files": files, "snip": snippets},
                                  ensure_ascii=False, indent=1) + ";\n",
    encoding="utf-8",
)
print(f"OK: {len(files)} файлов, {len(snippets)} фрагментов -> {out.relative_to(ROOT)}")


# ---------- Тренажёр: заготовки и тесты ----------
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import exercises_spec as spec


def blank_methods(src, names):
    """Заменяет тела методов на заглушку (docstring сохраняется)."""
    tree = ast.parse(src)
    lines = src.splitlines()
    cuts = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and f"{node.name}.{item.name}" in names:
                    body = item.body
                    first = body[0]
                    keep_doc = isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) and isinstance(first.value.value, str)
                    start = first.end_lineno + 1 if keep_doc else first.lineno
                    indent = " " * (item.col_offset + 4)
                    cuts.append((start, item.end_lineno, indent))
    for start, end, indent in sorted(cuts, reverse=True):
        lines[start - 1:end] = [f"{indent}# TODO: твой код", f"{indent}pass"]
    return "\n".join(lines) + "\n"


def demo_block(demo):
    return '\n\nif __name__ == "__main__":\n    # «Запустить» выполняет этот блок. «Проверить» запускает скрытые тесты.\n' + \
        "\n".join("    " + l if l else "" for l in demo.splitlines()) + "\n"


exercises = {}
for ex_id, (fname, names) in spec.METHOD_EX.items():
    src = files[fname]
    main_part = src.split("# ---------- Другой вариант")[0].rstrip() + "\n"   # альтернативы в заготовку не кладём
    exercises[ex_id] = {
        "starter": blank_methods(main_part, names).rstrip() + demo_block(spec.DEMO[ex_id]),
        "solution": src,
        "tests": spec.TESTS[ex_id],
    }
for ex_id, (starter, demo) in spec.PROBLEM_STARTER.items():
    exercises[ex_id] = {
        "starter": starter.rstrip() + demo_block(demo),
        "solution": files[spec.PROBLEM_FILES[ex_id]],
        "tests": spec.TESTS[ex_id],
    }

# ---------- Раздел 1 ----------
import exercises_spec1 as spec1


def extract_funcs(src, names):
    tree = ast.parse(src)
    parts = [ast.get_source_segment(src, n) for n in tree.body
             if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    return "\n\n\n".join(parts) + "\n"


for ex_id, d in spec1.S1.items():
    src = files[d["file"]]
    if d.get("only"):
        sol = d.get("header", "") + extract_funcs(src, d["only"].split(","))
    else:
        sol = src.split("# ---------- Другой вариант")[0].rstrip() + "\n"
    if d.get("rename"):
        old, new = d["rename"]
        sol = sol.replace(old, new)
    exercises[ex_id] = {"starter": d["starter"].rstrip() + demo_block(d["demo"]), "solution": sol, "tests": d["tests"]}
for ex_id, (starter, demo) in spec1.P1_STARTER.items():
    exercises[ex_id] = {"starter": starter.rstrip() + demo_block(demo), "solution": files[spec1.P1_FILES[ex_id]], "tests": spec1.P1_TESTS[ex_id]}

out2 = ROOT / "assets" / "exercises.js"
out2.write_text(
    "// Сгенерировано tools/build.py из tools/exercises_spec.py — не редактируйте вручную.\n"
    "window.EXERCISES = " + json.dumps({"harness": spec.HARNESS, "common": spec.COMMON_TESTS + spec1.COMMON1, "ex": exercises},
                                       ensure_ascii=False, indent=1) + ";\n",
    encoding="utf-8",
)
print(f"OK: {len(exercises)} заданий тренажёра -> {out2.relative_to(ROOT)}")


# ---------- Метка версии для index.html (чтобы браузер не брал старые файлы из кэша) ----------
import hashlib
import re

index = ROOT / "index.html"
html = index.read_text(encoding="utf-8")
def _bust(m):
    path = m.group(2)
    digest = hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]
    return f'{m.group(1)}{path}?v={digest}"'
html = re.sub(r'((?:src|href)=")(assets/[\w.-]+\.(?:js|css))(?:\?v=\w+)?"', _bust, html)
index.write_text(html, encoding="utf-8")
print("OK: метки версий в index.html обновлены")
