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
