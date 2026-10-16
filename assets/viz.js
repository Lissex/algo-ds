// Интерактивные модели структур данных.
(function () {
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  let uid = 0;

  // FNV-1a 32 бит — как _hash у преподавателя (до взятия % capacity)
  function fnv1a(key) {
    const bytes = new TextEncoder().encode(String(key));
    let h = 0x811c9dc5;
    for (const b of bytes) { h ^= b; h = Math.imul(h, 0x01000193) >>> 0; }
    return h >>> 0;
  }
  const hex = n => '0x' + n.toString(16).padStart(8, '0');

  function shell(el, title, ctlHtml) {
    el.innerHTML = `<div class="viz-h"><b>▶ ${esc(title)}</b><span class="muted" style="font-size:13px">попробуй сам</span></div>
      <div class="viz-ctl">${ctlHtml}</div><div class="viz-stage"></div><div class="viz-log" aria-live="polite"></div>`;
    const stage = el.querySelector('.viz-stage');
    const logEl = el.querySelector('.viz-log');
    const $ = sel => el.querySelector(sel);
    const log = (html) => { logEl.innerHTML = html; };
    const on = (act, fn) => el.querySelectorAll(`[data-a="${act}"]`).forEach(b => b.addEventListener('click', fn));
    el.querySelectorAll('input').forEach(inp => inp.addEventListener('keydown', e => {
      if (e.key === 'Enter') { const b = el.querySelector('.viz-ctl button.p'); if (b) b.click(); }
    }));
    return { stage, log, $, on };
  }
  const val = (inp, fallback) => { const v = inp.value.trim(); return v === '' ? fallback : v; };
  const ok = s => `<span class="ok">${s}</span>`;
  const err = s => `<span class="err">${s}</span>`;

  // ---------- Стек ----------
  function stack(el) {
    const { stage, log, $, on } = shell(el, 'Модель стека на списке', `
      <input data-i="v" placeholder="знач." aria-label="значение">
      <button class="p" data-a="add">add → append</button><button data-a="remove">remove → pop()</button><button data-a="peek">peek → [-1]</button>
      <span class="sep"></span><button data-a="clear">очистить</button>`);
    let st = [{ v: 3, id: uid++ }, { v: 7, id: uid++ }, { v: 1, id: uid++ }], fresh = -1, flash = -1, n = 4;
    const draw = () => {
      stage.innerHTML = st.length ? `<div class="vstack"><div class="vstack-base"></div>${st.map((x, i) =>
        `<div class="vn ${x.id === fresh ? 'new' : ''} ${x.id === flash ? 'flash' : ''}">${esc(x.v)}${i === st.length - 1 ? '<span class="tag" style="bottom:auto;top:50%;left:auto;right:-46px;transform:translateY(-50%)">← top</span>' : ''}</div>`).join('')}</div>`
        : '<div class="vempty">стек пуст: top = None</div>';
      fresh = flash = -1;
    };
    on('add', () => { const inp = $('[data-i=v]'); const v = val(inp, n++); inp.value = ''; const x = { v, id: uid++ }; st.push(x); fresh = x.id; draw(); log(`add(${esc(v)}) → data.append(${esc(v)}) · на вершину (конец списка) · len = ${st.length}`); });
    on('remove', () => { if (!st.length) return log(err('IndexError: remove from empty stack')); const x = st.pop(); draw(); log(`remove() → ${ok(esc(x.v))} · data.pop(): последний элемент, ничего не сдвигается — O(1)`); });
    on('peek', () => { if (!st.length) return log(err('IndexError: peek from empty stack')); flash = st[st.length - 1].id; draw(); log(`peek() → ${ok(esc(st[st.length - 1].v))} · стек не изменился`); });
    on('clear', () => { st = []; draw(); log('стек очищен'); });
    draw(); log('LIFO: вершина — конец списка, append и pop() работают за O(1)');
  }

  // ---------- Очередь (на списке Python, как на парах) ----------
  function queue(el) {
    const { stage, log, $, on } = shell(el, 'Модель очереди на списке', `
      <input data-i="v" placeholder="знач." aria-label="значение">
      <button class="p" data-a="add">add → append</button><button data-a="remove">remove → pop(0)</button><button data-a="peek">peek → [0]</button>
      <span class="sep"></span><button data-a="clear">очистить</button>`);
    let q = ['A', 'B', 'C'].map(v => ({ v, id: uid++ })), fresh = -1, flash = -1, shifted = false, n = 0;
    const names = 'DEFGHIJKLMNOPQRSTUVWXYZ';
    const draw = () => {
      stage.innerHTML = q.length ? `<div class="vrow" style="gap:6px">${q.map((x, i) =>
        `<div class="vn ${x.id === fresh ? 'new' : ''} ${x.id === flash || (shifted && x.id !== fresh) ? 'flash' : ''}"><span class="ix">[${i}]</span>${esc(x.v)}${i === 0 ? '<span class="tag">начало</span>' : i === q.length - 1 ? '<span class="tag">конец</span>' : ''}</div>`).join('')}</div>`
        : '<div class="vempty">очередь пуста: data = []</div>';
      fresh = flash = -1; shifted = false;
    };
    on('add', () => { const inp = $('[data-i=v]'); const v = val(inp, names[n++ % names.length]); inp.value = ''; const x = { v, id: uid++ }; q.push(x); fresh = x.id; draw(); log(`add(${esc(v)}) → data.append(${esc(v)}) · в конец, O(1) · len = ${q.length}`); });
    on('remove', () => {
      if (!q.length) return log(err('IndexError: remove from empty queue'));
      const x = q.shift(); shifted = q.length > 0; draw();
      log(`remove() → ${ok(esc(x.v))} · data.pop(0): ${q.length ? `остальные ${q.length} элемент(а) сдвинулись на позицию влево — поэтому O(n)` : 'очередь опустела'}`);
    });
    on('peek', () => { if (!q.length) return log(err('IndexError: peek from empty queue')); flash = q[0].id; draw(); log(`peek() → ${ok(esc(q[0].v))} · data[0], очередь не изменилась`); });
    on('clear', () => { q = []; draw(); log('очередь очищена'); });
    draw(); log('FIFO: append в конец, pop(0) из начала. Нажми remove — увидишь сдвиг индексов');
  }

  // ---------- Связанные списки ----------
  function linked(el, dbl) {
    const { stage, log, $, on } = shell(el, dbl ? 'Модель двусвязного списка' : 'Модель связанного списка', `
      <input data-i="v" placeholder="val" aria-label="значение"><input data-i="i" placeholder="idx" aria-label="индекс">
      <button class="p" data-a="append">append(val)</button>
      ${dbl ? '<button data-a="appendleft">appendleft(val)</button>' : ''}
      <button data-a="insert">insert(idx, val)</button>
      <button data-a="get">[idx]</button><button data-a="set">[idx] = val</button>
      <button data-a="pop">pop(idx)</button><button data-a="remove">remove(val)</button>
      <button data-a="reverse">reverse()</button>`);
    let L = [5, 8, 2, 9].map(v => ({ v, id: uid++ })), fresh = -1, hot = -1, busy = false;
    const arrow = dbl ? '⇄' : '→';
    const draw = () => {
      const tagFor = i => {
        const t = [];
        if (i === 0) t.push('head');
        if (dbl && i === L.length - 1) t.push('tail');
        return t.length ? `<span class="tag">${t.join('·')}</span>` : '';
      };
      stage.innerHTML = L.length ? `<div class="vrow">${dbl ? '<span class="vnone">None</span><span class="varr">←</span>' : ''}${L.map((x, i) =>
        `<div class="vn ${x.id === fresh ? 'new' : ''} ${x.id === hot ? 'flash' : ''}"><span class="ix">${i}</span>${esc(x.v)}${tagFor(i)}</div>${i < L.length - 1 ? `<span class="varr">${arrow}</span>` : ''}`).join('')}
        <span class="varr">→</span><span class="vnone">None</span></div>` : `<div class="vempty">пустой список: head${dbl ? ' = tail' : ''} = None</div>`;
      fresh = -1;
    };
    const idxOf = (raw, allowEnd) => {
      let i = parseInt(raw, 10);
      if (isNaN(i)) return null;
      if (dbl && i < 0) i += L.length;
      if (i < 0 || i > L.length - (allowEnd ? 0 : 1)) return null;
      return i;
    };
    async function walk(i) {
      // показываем обход: от head (или от tail для двусвязного, если ближе)
      busy = true;
      const fromTail = dbl && i >= Math.floor(L.length / 2);
      const path = [];
      if (fromTail) for (let k = L.length - 1; k >= i; k--) path.push(k); else for (let k = 0; k <= i; k++) path.push(k);
      for (const k of path) { hot = L[k].id; draw(); await sleep(260); }
      hot = -1; busy = false;
      return { steps: path.length - 1, fromTail };
    }
    const nextVal = () => { const inp = $('[data-i=v]'); const v = val(inp, Math.floor(Math.random() * 90) + 10); inp.value = ''; return v; };
    on('append', () => { if (busy) return; const v = nextVal(); const x = { v, id: uid++ }; L.push(x); fresh = x.id; draw(); log(dbl ? `append(${esc(v)}) → tail.next = node, node.prev = tail, tail = node · O(1)` : `append(${esc(v)}) → прошли ${Math.max(L.length - 2, 0)} шаг(ов) до последнего узла · O(n)`); });
    on('appendleft', () => { if (busy) return; const v = nextVal(); const x = { v, id: uid++ }; L.unshift(x); fresh = x.id; draw(); log(`appendleft(${esc(v)}) → node.next = head, head.prev = node, head = node · O(1)`); });
    on('insert', async () => {
      if (busy) return;
      const i = idxOf($('[data-i=i]').value, true);
      if (i === null) return log(err(`IndexError: введи idx от 0 до ${L.length}`));
      const v = nextVal();
      if (i > 0) await walk(i - 1);
      const x = { v, id: uid++ }; L.splice(i, 0, x); fresh = x.id; draw();
      log(i === 0 ? `insert(0, ${esc(v)}) → новая голова · O(1)` : `insert(${i}, ${esc(v)}) → нашли prev = [${i - 1}], new.next = prev.next, prev.next = new`);
    });
    on('get', async () => {
      if (busy) return;
      const i = idxOf($('[data-i=i]').value, false);
      if (i === null) return log(err('IndexError: index out of range'));
      const r = await walk(i); hot = L[i].id; draw(); hot = -1;
      log(`[${i}] → ${ok(esc(L[i].v))} · ${r.steps} шаг(ов) от ${r.fromTail ? 'tail назад' : 'head вперёд'}`);
    });
    on('set', async () => {
      if (busy) return;
      const i = idxOf($('[data-i=i]').value, false);
      if (i === null) return log(err('IndexError: index out of range'));
      const v = nextVal();
      const r = await walk(i); L[i].v = v; hot = L[i].id; draw(); hot = -1;
      log(`[${i}] = ${esc(v)} → нашли узел за ${r.steps} шаг(ов), поменяли node.val; ссылки не трогали`);
    });
    on('pop', async () => {
      if (busy) return;
      if (!L.length) return log(err('IndexError: pop from empty list'));
      const raw = $('[data-i=i]').value.trim();
      const i = raw === '' && dbl ? L.length - 1 : idxOf(raw, false);
      if (i === null) return log(err(dbl ? 'IndexError: out of range' : 'IndexError: укажи idx'));
      if (!(dbl && (i === 0 || i === L.length - 1))) await walk(i);
      const x = L.splice(i, 1)[0]; draw();
      log(`pop(${raw === '' ? '' : i}) → ${ok(esc(x.v))}` + (dbl ? (i === L.length ? ' · удалили хвост: tail = tail.prev · O(1)' : i === 0 ? ' · удалили голову: head = head.next · O(1)' : ' · prev.next = next, next.prev = prev') : (i === 0 ? ' · head = head.next' : ' · prev.next = target.next')));
    });
    on('remove', async () => {
      if (busy) return;
      const inp = $('[data-i=v]'); const v = inp.value.trim(); inp.value = '';
      if (v === '') return log(err('введи значение в поле val'));
      const i = L.findIndex(x => String(x.v) === v);
      if (i < 0) { if (L.length) await walk(L.length - 1); draw(); return log(err(`ValueError: ${esc(v)} not in list`)); }
      busy = true;
      for (let k = 0; k <= i; k++) { hot = L[k].id; draw(); await sleep(260); }
      hot = -1; busy = false;
      L.splice(i, 1); draw();
      log(`remove(${esc(v)}) → ${i === 0 ? 'это голова: head = head.next' : `cur.next = cur.next.next (cur = [${i - 1}])`}`);
    });
    on('reverse', () => { if (busy) return; L.reverse(); L.forEach(x => {}); draw(); log(dbl ? 'reverse() → у каждого узла prev ⇄ next, затем head ⇄ tail' : 'reverse() → prev/cur/nxt: развернули каждую стрелку, head = prev'); });
    draw(); log(dbl ? 'Ссылки в обе стороны. [idx] идёт с ближнего конца — попробуй idx = 3' : 'Введи val и/или idx и нажми на операцию');
  }

  // ---------- Кольцевой массив / deque ----------
  function ring(el) {
    const { stage, log, $, on } = shell(el, 'Модель deque на кольцевом массиве', `
      <input data-i="v" placeholder="знач." aria-label="значение">
      <button class="p" data-a="append">append</button><button data-a="appendleft">appendleft</button>
      <button data-a="pop">pop (popright)</button><button data-a="popleft">popleft</button>
      <span class="sep"></span><button data-a="reset">сброс</button>`);
    let cap, head, size, arr, n, freshIdx = -1;
    const reset = () => { cap = 8; head = 5; size = 0; arr = Array(cap).fill(null); n = 1; ['a', 'b', 'c', 'd'].forEach(v => { arr[(head + size) % cap] = v; size++; }); };
    reset();
    const draw = () => {
      const N = cap, cx = 150, cy = 150, R = 132, r = 82;
      const pt = (rad, a) => [cx + rad * Math.cos(a), cy + rad * Math.sin(a)];
      let segs = '';
      for (let i = 0; i < N; i++) {
        const a0 = -Math.PI / 2 + (i / N) * 2 * Math.PI + 0.012, a1 = -Math.PI / 2 + ((i + 1) / N) * 2 * Math.PI - 0.012;
        const [x0, y0] = pt(R, a0), [x1, y1] = pt(R, a1), [x2, y2] = pt(r, a1), [x3, y3] = pt(r, a0);
        const filled = arr[i] !== null;
        const isHead = size > 0 && i === head, isTail = size > 0 && i === (head + size - 1) % cap;
        const fill = i === freshIdx ? 'var(--hl)' : filled ? 'var(--ink)' : 'var(--bg-2)';
        const stroke = isHead ? 'var(--blue)' : 'var(--line-2)';
        segs += `<path d="M${x0},${y0} A${R},${R} 0 0 1 ${x1},${y1} L${x2},${y2} A${r},${r} 0 0 0 ${x3},${y3} Z" fill="${fill}" stroke="${stroke}" stroke-width="${isHead ? 3 : 1}"/>`;
        const am = (a0 + a1) / 2, [tx, ty] = pt((R + r) / 2, am), [ix, iy] = pt(R + 12, am);
        if (filled && N <= 32) segs += `<text x="${tx}" y="${ty}" text-anchor="middle" dominant-baseline="central" font-size="${N > 16 ? 9 : 14}" font-weight="700" fill="${i === freshIdx ? '#11140a' : 'var(--bg)'}">${esc(String(arr[i]).slice(0, 3))}</text>`;
        if (N <= 16) segs += `<text x="${ix}" y="${iy}" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--ink-3)">${i}</text>`;
        if (isHead) { const [hx, hy] = pt(r - 16, am); segs += `<text x="${hx}" y="${hy}" text-anchor="middle" dominant-baseline="central" font-size="10" font-weight="700" fill="var(--blue)">H</text>`; }
        if (isTail && !isHead) { const [hx, hy] = pt(r - 16, am); segs += `<text x="${hx}" y="${hy}" text-anchor="middle" dominant-baseline="central" font-size="10" font-weight="700" fill="var(--ink-3)">T</text>`; }
      }
      const cells = arr.map((v, i) => `<div class="cell ${v !== null ? 'f' : ''} ${size && i === head ? 'h' : ''}"><i>${i}</i>${v === null ? '' : esc(String(v).slice(0, 3))}</div>`).join('');
      stage.innerHTML = `<div class="ring-wrap"><svg viewBox="-10 -10 320 320" role="img" aria-label="кольцевой массив">${segs}
        <text x="150" y="142" text-anchor="middle" font-size="12" fill="var(--ink-3)">size ${size}</text>
        <text x="150" y="162" text-anchor="middle" font-size="12" fill="var(--ink-3)">cap ${cap}</text></svg>
        <div><div class="ring-meta">head = <b>${head}</b> &nbsp; size = <b>${size}</b> &nbsp; capacity = <b>${cap}</b><br>
        последний: (head + size − 1) % cap = <b>${size ? (head + size - 1) % cap : '—'}</b><br>
        след. справа: (head + size) % cap = <b>${(head + size) % cap}</b><br>
        логически: [${Array.from({ length: size }, (_, i) => esc(arr[(head + i) % cap])).join(', ')}]</div>
        <div style="height:22px"></div><div class="ring-arr">${cells}</div></div></div>`;
      freshIdx = -1;
    };
    const resize = () => {
      const nw = Array(cap * 2).fill(null);
      for (let i = 0; i < size; i++) nw[i] = arr[(head + i) % cap];
      const old = cap; arr = nw; cap *= 2; head = 0; return `resize: ${old} → ${cap}, элементы «распрямлены», head = 0. `;
    };
    const nv = () => { const inp = $('[data-i=v]'); const v = val(inp, String(n++)); inp.value = ''; return v; };
    on('append', () => { let msg = ''; if (size === cap) { if (cap >= 32) return log(err('для наглядности модель ограничена 32 ячейками')); msg = resize(); } const v = nv(); const i = (head + size) % cap; arr[i] = v; size++; freshIdx = i; draw(); log(msg + `append(${esc(v)}) → ячейка (${head} + ${size - 1}) % ${cap} = ${i}`); });
    on('appendleft', () => { let msg = ''; if (size === cap) { if (cap >= 32) return log(err('для наглядности модель ограничена 32 ячейками')); msg = resize(); } const v = nv(); const old = head; head = (head - 1 + cap) % cap; arr[head] = v; size++; freshIdx = head; draw(); log(msg + `appendleft(${esc(v)}) → head = (${old} − 1) % ${cap} = ${head}`); });
    on('pop', () => { if (!size) return log(err('IndexError: pop from empty deque')); const i = (head + size - 1) % cap; const v = arr[i]; arr[i] = null; size--; draw(); log(`pop() → ${ok(esc(v))} из ячейки ${i}; head не изменился`); });
    on('popleft', () => { if (!size) return log(err('IndexError: popleft from empty deque')); const v = arr[head]; arr[head] = null; const old = head; head = (head + 1) % cap; size--; draw(); log(`popleft() → ${ok(esc(v))} · head = (${old} + 1) % ${cap} = ${head}`); });
    on('reset', () => { reset(); draw(); log('сброс: head = 5, элемент d «завернул» через конец массива в ячейку 0'); });
    draw(); log('head = 5: элемент d «завернул» в ячейку 0. Добавь ещё 5 элементов — увидишь resize');
  }

  // ---------- Hashset / Hashtable ----------
  function hashset(el, table) {
    const { stage, log, $, on } = shell(el, table ? 'Модель Hashtable (цепочки)' : 'Модель Hashset (цепочки)', `
      <input class="w" data-i="k" placeholder="key" aria-label="ключ">${table ? '<input data-i="v" placeholder="val" aria-label="значение">' : ''}
      <button class="p" data-a="add">${table ? 't[key] = val' : 'add(key)'}</button>
      <button data-a="find">${table ? 't[key]' : 'key in s'}</button><button data-a="remove">remove(key)</button>
      <span class="sep"></span><button data-a="rnd">+5 случайных</button><button data-a="reset">сброс</button>`);
    const LF = 0.75;
    let cap, buckets, size, freshKey = null, hit = -1, flashKey = null;
    const words = ['cat', 'dog', 'owl', 'fox', 'bee', 'ant', 'elk', 'yak', 'emu', 'cow', 'pig', 'hen', 'rat', 'bat', 'eel', 'cod', 'ram', 'koi', 'gnu', 'ape'];
    const reset = () => { cap = 4; buckets = Array.from({ length: cap }, () => []); size = 0; };
    const idx = k => fnv1a(k) % cap;
    const find = (k) => { const b = buckets[idx(k)]; return b.findIndex(n => n.k === k); };
    const rawPut = (k, v) => { const b = buckets[idx(k)]; const j = b.findIndex(n => n.k === k); if (j >= 0) { b[j].v = v; return false; } b.push({ k, v }); size++; return true; };
    const resize = () => { const old = buckets; cap *= 2; buckets = Array.from({ length: cap }, () => []); size = 0; old.forEach(b => b.forEach(n => rawPut(n.k, n.v))); };
    const put = (k, v) => {
      let msg = '';
      if (size / cap >= LF) { const o = cap; resize(); msg = `load factor ${(size / o).toFixed(2)} ≥ 0.75 → resize ${o} → ${cap}, все ключи переложены заново. `; }
      const i = idx(k), h = fnv1a(k), before = buckets[i].length;
      const added = rawPut(k, v);
      hit = i; freshKey = k;
      msg += `hash("${esc(k)}") = ${hex(h)} → ${h} % ${cap} = <b>${i}</b>. `;
      if (!added) msg += table ? 'ключ уже есть → обновили значение' : 'ключ уже есть → ничего не делаем';
      else if (before) msg += `<span class="err">коллизия!</span> в корзине уже ${before} — дописали в конец цепочки`;
      else msg += 'корзина была пустой';
      return msg;
    };
    reset(); ['cat', 'dog'].forEach((k, i) => rawPut(k, i + 1));
    const draw = () => {
      const lf = size / cap;
      stage.innerHTML = `<div class="hs"><div class="hs-meta"><span>size = <b>${size}</b></span><span>capacity = <b>${cap}</b></span>
        <span class="lf">load factor = <b>${lf.toFixed(2)}</b><span class="progress"><i class="${lf >= LF ? 'hi' : ''}" style="width:${Math.min(lf / 1, 1) * 100}%"></i></span></span></div>
        ${buckets.map((b, i) => `<div class="hs-row ${i === hit ? 'hit' : ''}"><span class="hs-i">${i}</span><span class="hs-b"></span>${b.length ? b.map((n, j) =>
          `<div class="vn ${n.k === freshKey && i === hit ? 'new' : ''} ${n.k === flashKey ? 'flash' : ''}">${esc(n.k)}${table ? `<span style="opacity:.6;font-weight:500">:${esc(n.v)}</span>` : ''}</div>${j < b.length - 1 ? '<span class="varr">→</span>' : ''}`).join('') : '<span class="vnone">None</span>'}</div>`).join('')}</div>`;
      freshKey = flashKey = null; hit = -1;
    };
    const key = () => { const inp = $('[data-i=k]'); const k = inp.value.trim(); return k; };
    on('add', () => {
      let k = key(); if (!k) k = words.find(w => find(w) < 0) || ('k' + Math.floor(Math.random() * 999));
      const vi = $('[data-i=v]'); const v = vi ? val(vi, Math.floor(Math.random() * 90) + 10) : null; if (vi) vi.value = '';
      $('[data-i=k]').value = '';
      const msg = put(k, v); draw(); log(msg);
    });
    on('find', () => {
      const k = key(); if (!k) return log(err('введи key'));
      const i = idx(k), j = find(k); hit = i; if (j >= 0) flashKey = k; draw();
      log(`корзина ${i}: ` + (j >= 0 ? (table ? `t["${esc(k)}"] → ${ok(esc(buckets[i][j].v))}` : ok('True')) + ` · ${j + 1} сравнени${j ? 'я' : 'е'} в цепочке` : (table ? err(`KeyError: '${esc(k)}'`) : err('False'))));
    });
    on('remove', () => {
      const k = key(); if (!k) return log(err('введи key'));
      const i = idx(k), j = find(k); hit = i;
      if (j < 0) { draw(); return log(err(`KeyError: '${esc(k)}'`) + ` · в корзине ${i} нет такого ключа`); }
      buckets[i].splice(j, 1); size--; $('[data-i=k]').value = ''; draw();
      log(`remove("${esc(k)}") → корзина ${i}, ` + (j === 0 ? 'первый в цепочке: buckets[i] = head.next' : 'head.next = head.next.next'));
    });
    on('rnd', () => { let msg = ''; for (let t = 0; t < 5; t++) { const k = words.find(w => find(w) < 0) || ('k' + Math.floor(Math.random() * 999)); msg = put(k, Math.floor(Math.random() * 90) + 10); } hit = -1; draw(); log('добавили 5 ключей. Последний: ' + msg); });
    on('reset', () => { reset(); draw(); log('пустая таблица, capacity = 4'); });
    draw(); log('Хэш — FNV-1a, как у преподавателя. Добавляй ключи и смотри на коллизии и resize');
  }

  // ---------- Хэш-функция ----------
  function hashDemo(el) {
    el.innerHTML = `<div class="viz-h"><b>▶ FNV-1a против SHA-256</b><span class="muted" style="font-size:13px">измени одну букву</span></div>
      <div class="viz-ctl"><input class="w" style="width:220px" data-i="s" value="hello" aria-label="строка"></div>
      <div class="viz-stage"><div class="hash-out"></div></div>`;
    const inp = el.querySelector('[data-i=s]'), out = el.querySelector('.hash-out');
    let prev = null;
    async function upd() {
      const s = inp.value, h = fnv1a(s);
      const bits = h.toString(2).padStart(32, '0');
      const pb = prev === null ? bits : prev.toString(2).padStart(32, '0');
      const diff = [...bits].filter((b, i) => b !== pb[i]).length;
      let sha = '…';
      try { const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); sha = [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join(''); }
      catch (e) { sha = 'недоступно (откройте сайт по https)'; }
      out.innerHTML = `
        <div class="row"><span>FNV-1a (32 бита)</span><b>${hex(h)}</b><span class="muted">= ${h}</span></div>
        <div class="bits">${[...bits].map((b, i) => `<span class="${b === '1' ? 'one' : ''} ${b !== pb[i] ? 'chg' : ''}">${b}</span>`).join('')}</div>
        <div class="row"><span>изменилось бит</span><b>${prev === null ? '—' : diff + ' из 32'}</b></div>
        <div class="row"><span>корзина при cap = 8</span><b>${h % 8}</b></div>
        <div class="row"><span>корзина при cap = 16</span><b>${h % 16}</b></div>
        <div class="row"><span>корзина при cap = 1000</span><b>${h % 1000}</b></div>
        <div class="row"><span>SHA-256 (256 бит)</span><b style="word-break:break-all;font-size:12px">${sha}</b></div>`;
      prev = h;
    }
    inp.addEventListener('input', upd); upd();
  }

  window.VIZ = {
    mount(el, type) {
      const map = { stack, queue, sll: e => linked(e, false), dll: e => linked(e, true), ring, hashset: e => hashset(e, false), hashtable: e => hashset(e, true), hash: hashDemo };
      if (map[type]) { el.classList.add('viz'); map[type](el); }
    },
    fnv1a
  };
})();
