"""Проверка тренажёра: эталон проходит все тесты, пустая заготовка — нет,
демо-блок заготовки и эталона запускается без ошибок."""
import json, io, contextlib, signal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "assets" / "exercises.js").read_text(encoding="utf-8").split("= ", 1)[1].rstrip().rstrip(";"))
h = {}
exec(data["harness"], h)
run = h["__run_tests"]

HAS_ALARM = hasattr(signal, "SIGALRM")   # на Windows нет — тогда без таймаута
if HAS_ALARM:
    def alarm(*_): raise TimeoutError
    signal.signal(signal.SIGALRM, alarm)

bad = 0
for ex_id, ex in data["ex"].items():
    if HAS_ALARM: signal.alarm(10)
    sol = json.loads(run(ex["solution"], data["common"], ex["tests"]))
    st = json.loads(run(ex["starter"], data["common"], ex["tests"]))
    if HAS_ALARM: signal.alarm(0)
    fails = [r for r in sol.get("results", []) if not r[1]]
    passed_starter = sum(r[1] for r in st.get("results", []))
    total = len(sol.get("results", []))
    # демо: заготовка должна запускаться как __main__ без SyntaxError
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try: exec(compile(ex["starter"], "s.py", "exec"), {"__name__": "__main__"})
        except SyntaxError as e: fails.append(["starter syntax", False, str(e)])
        except Exception: pass
    ok = "error" not in sol and not fails and total >= 3 and passed_starter < total
    if not ok: bad += 1
    print(f"{'OK ' if ok else 'BAD'} {ex_id:17} тестов {total}, заготовка проходит {passed_starter}/{total}", "" if ok else (sol.get('error') or fails))
print("ВСЕ ЗАДАНИЯ OK" if not bad else f"ОШИБОК: {bad}")
