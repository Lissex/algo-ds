// Тренажёр: редактор кода + Python в браузере (Pyodide в Web Worker) + проверка тестами.
(function () {
  const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';
  const CM = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/';
  const TIME_LIMIT = 6000; // мс на один запуск
  const EX = window.EXERCISES;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  };
  const solved = () => new Set(store.get('solved', []));
  const markSolved = id => { const s = solved(); s.add(id); store.set('solved', [...s]); };

  // ---------- Web Worker с Pyodide ----------
  const WORKER_SRC = `
let py = null;
const out = [];
async function init() {
  importScripts('${PYODIDE}pyodide.js');
  py = await loadPyodide({ indexURL: '${PYODIDE}' });
  py.setStdout({ batched: s => out.push(s + '\\n') });
  py.setStderr({ batched: s => out.push(s + '\\n') });
  py.setStdin({ error: true });
  py.runPython(\`
import sys, traceback
def __run_main(code):
    ns = {"__name__": "__main__"}
    import linecache
    linecache.cache["solution.py"] = (len(code), None, code.splitlines(True), "solution.py")
    try:
        exec(compile(code, "solution.py", "exec"), ns)
    except SystemExit:
        pass
    except SyntaxError as e:
        print(f"SyntaxError: {e.msg}\\\\n  строка {e.lineno}: {(e.text or '').rstrip()}", file=sys.stderr)
    except BaseException as e:
        frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == "solution.py"]
        lines = [f"  строка {f.lineno}, в {f.name}: {(f.line or '').strip()}" for f in frames]
        name = type(e).__name__
        msg = str(e)
        if name == "OSError" and "stdin" in msg.lower():
            msg = "input() здесь не работает — задай данные прямо в коде"
        print("Traceback:\\\\n" + "\\\\n".join(lines) + f"\\\\n{name}: {msg}", file=sys.stderr)
\`);
}
onmessage = async (e) => {
  const m = e.data;
  try {
    if (!py) { await init(); postMessage({ type: 'ready' }); }
    if (m.type === 'warm') return;
    out.length = 0;
    if (m.type === 'run') {
      py.globals.get('__run_main')(m.code);
      postMessage({ type: 'done', id: m.id, output: out.join('') });
    } else if (m.type === 'check') {
      if (!py.globals.has('__run_tests')) py.runPython(m.harness);
      const res = py.globals.get('__run_tests')(m.code, m.common, m.tests);
      postMessage({ type: 'done', id: m.id, result: JSON.parse(res), output: out.join('') });
    }
  } catch (err) {
    postMessage({ type: 'done', id: m.id, fatal: String(err && err.message || err) });
  }
};`;

  let worker = null, ready = false, readyWaiters = [], pending = null, seq = 0;
  const listeners = new Set();
  const setStatus = s => listeners.forEach(f => f(s));
  function spawn() {
    ready = false;
    try {
      worker = new Worker(URL.createObjectURL(new Blob([WORKER_SRC], { type: 'text/javascript' })));
    } catch (e) { worker = null; setStatus('error'); return; }
    worker.onmessage = e => {
      const m = e.data;
      if (m.type === 'ready') { ready = true; setStatus('ready'); readyWaiters.splice(0).forEach(f => f()); }
      else if (m.type === 'done' && pending && pending.id === m.id) { clearTimeout(pending.timer); const p = pending; pending = null; p.resolve(m); }
    };
    worker.onerror = () => { setStatus('error'); if (pending) { const p = pending; pending = null; p.resolve({ fatal: 'Не удалось загрузить Python. Проверь интернет и обнови страницу.' }); } };
    setStatus('loading');
    worker.postMessage({ type: 'warm' });
  }
  function whenReady() { return ready ? Promise.resolve() : new Promise(r => readyWaiters.push(r)); }
  async function exec(msg) {
    if (!worker) spawn();
    if (pending) return { fatal: 'Подожди, предыдущий запуск ещё идёт' };
    await whenReady();
    return new Promise(resolve => {
      const id = ++seq;
      pending = { id, resolve, timer: setTimeout(() => {
        // бесконечный цикл или очень медленный код — убиваем воркер и поднимаем новый
        worker.terminate(); worker = null; pending = null;
        resolve({ timeout: true });
        spawn();
      }, TIME_LIMIT) };
      worker.postMessage(Object.assign({ id }, msg));
    });
  }

  // ---------- CodeMirror (лениво) ----------
  let cmPromise = null;
  function loadCM() {
    if (cmPromise) return cmPromise;
    const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = CM + 'codemirror.min.css'; document.head.appendChild(css);
    const js = src => new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); });
    cmPromise = js(CM + 'codemirror.min.js')
      .then(() => Promise.all([js(CM + 'mode/python/python.min.js'), js(CM + 'addon/edit/matchbrackets.min.js'), js(CM + 'addon/edit/closebrackets.min.js')]))
      .then(() => window.CodeMirror).catch(() => null);
    return cmPromise;
  }

  // ---------- Виджет ----------
  function mount(el, exId, helpers) {
    const ex = EX.ex[exId];
    if (!ex) { el.innerHTML = '<p class="muted">Для этого задания тренажёра нет.</p>'; return; }
    const key = 'code:' + exId;
    const saved = store.get(key, null);
    el.innerHTML = `<div class="tr ${solved().has(exId) ? 'solved' : ''}">
      <div class="tr-bar">
        <span class="tr-title">✍ Тренажёр <span class="tr-badge">решено ✓</span></span>
        <span class="tr-status" data-st>Python загрузится при первом запуске</span>
      </div>
      <div class="tr-ed"><textarea spellcheck="false" aria-label="Редактор кода">${esc(saved || ex.starter)}</textarea></div>
      <div class="tr-acts">
        <button class="btn sm" data-run title="Ctrl+Enter">▶ Запустить</button>
        <button class="btn sm pri" data-check title="Ctrl+Shift+Enter">✓ Проверить</button>
        <span style="flex:1"></span>
        <button class="btn sm" data-reset>Сбросить</button>
        <button class="btn sm" data-sol>Решение</button>
      </div>
      <div class="tr-out" data-out hidden></div>
      <div data-solbox hidden></div>
    </div>`;
    const root = el.firstElementChild;
    const ta = root.querySelector('textarea'), outEl = root.querySelector('[data-out]'), st = root.querySelector('[data-st]');
    let cm = null;
    const getCode = () => cm ? cm.getValue() : ta.value;
    const setCode = v => cm ? cm.setValue(v) : (ta.value = v);
    const save = () => store.set(key, getCode());

    // textarea-фолбэк: Tab = 4 пробела
    ta.addEventListener('keydown', e => {
      if (e.key === 'Tab' && !cm) { e.preventDefault(); const s = ta.selectionStart; ta.setRangeText('    ', s, ta.selectionEnd, 'end'); }
    });
    ta.addEventListener('input', save);
    loadCM().then(CodeMirror => {
      if (!CodeMirror || !document.body.contains(ta)) return;
      cm = CodeMirror.fromTextArea(ta, {
        mode: 'python', lineNumbers: true, indentUnit: 4, tabSize: 4, matchBrackets: true, autoCloseBrackets: true,
        extraKeys: {
          Tab: c => c.somethingSelected() ? c.indentSelection('add') : c.replaceSelection('    ', 'end'),
          'Shift-Tab': c => c.indentSelection('subtract'),
          'Ctrl-Enter': () => run(), 'Cmd-Enter': () => run(),
          'Shift-Ctrl-Enter': () => check(), 'Shift-Cmd-Enter': () => check(),
          'Ctrl-/': c => toggleComment(c), 'Cmd-/': c => toggleComment(c)
        }
      });
      cm.on('change', save);
      // подсвечиваем места, где нужно писать код, и прокручиваем к первому
      let first = -1;
      cm.eachLine(h => { if (/TODO: твой код|# твой код/.test(h.text)) { cm.addLineClass(h, 'background', 'tr-todo'); if (first < 0) first = cm.getLineNumber(h); } });
      if (first >= 0) {
        cm.setCursor({ line: first + 1, ch: cm.getLine(first + 1) ? cm.getLine(first + 1).length : 0 });
        const top = cm.charCoords({ line: Math.max(first - 4, 0), ch: 0 }, 'local').top;
        cm.scrollTo(null, top);
      }
    });
    function toggleComment(c) {
      const from = c.getCursor('from').line, to = c.getCursor('to').line;
      const lines = []; for (let i = from; i <= to; i++) lines.push(c.getLine(i));
      const all = lines.every(l => /^\s*#/.test(l) || !l.trim());
      c.operation(() => lines.forEach((l, k) => {
        const i = from + k;
        if (all) c.replaceRange(l.replace(/^(\s*)# ?/, '$1'), { line: i, ch: 0 }, { line: i, ch: l.length });
        else if (l.trim()) c.replaceRange(l.replace(/^(\s*)/, '$1# '), { line: i, ch: 0 }, { line: i, ch: l.length });
      }));
    }

    const statusText = { loading: '⏳ загружаю Python (~10 МБ, один раз)…', ready: '● Python готов', error: '⚠ Python не загрузился' };
    const onStatus = s => { if (document.body.contains(st)) st.textContent = statusText[s] || ''; st.className = 'tr-status ' + s; };
    listeners.add(onStatus);
    if (worker) onStatus(ready ? 'ready' : 'loading');

    const btns = root.querySelectorAll('.tr-acts button');
    const busy = b => btns.forEach(x => x.disabled = b);
    const show = html => { outEl.hidden = false; outEl.innerHTML = html; };
    const TO = `<div class="tr-err">⏱ Код выполнялся дольше ${TIME_LIMIT / 1000} с и был остановлен. Скорее всего, бесконечный цикл (проверь, что указатели/границы внутри <code>while</code> сдвигаются) или слишком медленный алгоритм — например, рекурсия без мемоизации или O(n²) там, где нужно O(n).</div>`;

    async function run() {
      busy(true); show('<div class="muted">выполняю…</div>');
      const r = await exec({ type: 'run', code: getCode() });
      busy(false);
      if (r.timeout) return show(TO);
      if (r.fatal) return show(`<div class="tr-err">${esc(r.fatal)}</div>`);
      show(`<div class="tr-lbl">вывод</div><pre class="tr-pre">${esc(r.output || '(ничего не напечатано)')}</pre>`);
    }
    async function check() {
      busy(true); show('<div class="muted">запускаю тесты…</div>');
      const r = await exec({ type: 'check', code: getCode(), harness: EX.harness, common: EX.common, tests: ex.tests });
      busy(false);
      if (r.timeout) return show(TO);
      if (r.fatal) return show(`<div class="tr-err">${esc(r.fatal)}</div>`);
      const res = r.result || {};
      if (res.error) return show(`<div class="tr-err">Код не запустился:<br><code>${esc(res.error)}</code></div>`);
      const list = res.results || [], ok = list.filter(x => x[1]).length, all = ok === list.length;
      if (all) { markSolved(exId); root.classList.add('solved'); }
      show(`<div class="tr-sum ${all ? 'ok' : 'bad'}">${all ? '🎉 Все тесты пройдены' : 'Пройдено тестов'}: ${ok} / ${list.length}</div>
        <ul class="tr-tests">${list.map(([n, p, m]) => `<li class="${p ? 'ok' : 'bad'}"><span>${p ? '✓' : '✗'}</span><div><b>${esc(n)}</b>${m ? `<div class="tr-msg">${esc(m)}</div>` : ''}</div></li>`).join('')}</ul>
        ${r.output ? `<div class="tr-lbl">вывод print</div><pre class="tr-pre">${esc(r.output)}</pre>` : ''}`);
      if (helpers && helpers.onSolved && all) helpers.onSolved(exId);
    }
    root.querySelector('[data-run]').addEventListener('click', run);
    root.querySelector('[data-check]').addEventListener('click', check);
    ta.addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); e.shiftKey ? check() : run(); } });
    let resetArmed = false;
    root.querySelector('[data-reset]').addEventListener('click', e => {
      const b = e.currentTarget;
      if (!resetArmed) { resetArmed = true; b.textContent = 'Точно сбросить?'; setTimeout(() => { resetArmed = false; b.textContent = 'Сбросить'; }, 2500); return; }
      resetArmed = false; b.textContent = 'Сбросить'; setCode(ex.starter); save(); outEl.hidden = true;
    });
    root.querySelector('[data-sol]').addEventListener('click', e => {
      const box = root.querySelector('[data-solbox]');
      box.hidden = !box.hidden;
      e.currentTarget.textContent = box.hidden ? 'Решение' : 'Скрыть решение';
      if (!box.hidden && !box.innerHTML && helpers) { box.innerHTML = helpers.codeBlock([{ label: 'эталонное решение', src: ex.solution }]); helpers.wire(box); }
    });
  }

  window.TRAINER = { mount, solved, has: id => !!(EX && EX.ex[id]), warm: () => { if (!worker) spawn(); } };
})();
