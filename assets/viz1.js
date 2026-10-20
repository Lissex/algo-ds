// Анимации раздела 1: сортировки, поиск, два указателя, окно, рекурсия, рост Big O.
(function () {
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const rnd = (n, lo = 1, hi = 40) => Array.from({ length: n }, () => lo + Math.floor(Math.random() * (hi - lo + 1)));

  // ---------- Пошаговый проигрыватель ----------
  // build(inputs) -> массив кадров {html, note}
  function player(el, title, inputsHtml, build, opts = {}) {
    el.innerHTML = `<div class="viz-h"><b>▶ ${esc(title)}</b><span class="muted" style="font-size:13px">по шагам</span></div>
      <div class="viz-ctl">${inputsHtml}${inputsHtml ? '<button class="p" data-a="go">применить</button><span class="sep"></span>' : ''}
        <button data-a="first" title="в начало">⏮</button><button data-a="prev" title="шаг назад">◀</button>
        <button class="p" data-a="play" title="воспроизвести">▶ пуск</button>
        <button data-a="next" title="шаг вперёд">▶︎|</button><button data-a="last" title="в конец">⏭</button>
        <select data-a="speed" aria-label="скорость"><option value="900">медленно</option><option value="450" selected>нормально</option><option value="150">быстро</option></select>
        ${opts.shuffle ? '<button data-a="shuffle">🎲 новые данные</button>' : ''}</div>
      <div class="viz-stage pl-stage"></div><div class="viz-log pl-log" aria-live="polite"></div>
      <div class="pl-bar"><input type="range" min="0" value="0" aria-label="шаг"><span class="pl-pos"></span></div>`;
    const stage = el.querySelector('.pl-stage'), log = el.querySelector('.pl-log'), range = el.querySelector('input[type=range]'), pos = el.querySelector('.pl-pos');
    const playBtn = el.querySelector('[data-a=play]'), speed = el.querySelector('[data-a=speed]');
    let frames = [], k = 0, timer = null;
    const show = () => {
      const f = frames[k] || { html: '', note: '' };
      const note = f.note || '', cut = note.indexOf('<span class="pl-cnt">');
      stage.innerHTML = f.html;
      log.innerHTML = cut < 0 ? `<span>${note}</span>` : `<span>${note.slice(0, cut)}</span>${note.slice(cut)}`;
      range.max = Math.max(frames.length - 1, 0); range.value = k; pos.textContent = `шаг ${k} / ${frames.length - 1}`;
    };
    const stop = () => { clearInterval(timer); timer = null; playBtn.textContent = '▶ пуск'; };
    const play = () => {
      if (timer) return stop();
      if (k >= frames.length - 1) k = 0;
      playBtn.textContent = '⏸ пауза';
      timer = setInterval(() => { if (!document.body.contains(el)) return stop(); if (k >= frames.length - 1) return stop(); k++; show(); }, +speed.value);
    };
    const rebuild = (fresh) => { stop(); try { frames = build(el, fresh) || []; } catch (e) { frames = [{ html: '', note: `<span class="err">${esc(e.message)}</span>` }]; } k = 0; show(); };
    el.querySelector('[data-a=first]').onclick = () => { stop(); k = 0; show(); };
    el.querySelector('[data-a=last]').onclick = () => { stop(); k = frames.length - 1; show(); };
    el.querySelector('[data-a=prev]').onclick = () => { stop(); k = Math.max(0, k - 1); show(); };
    el.querySelector('[data-a=next]').onclick = () => { stop(); k = Math.min(frames.length - 1, k + 1); show(); };
    playBtn.onclick = play;
    speed.onchange = () => { if (timer) { stop(); play(); } };
    range.oninput = () => { stop(); k = +range.value; show(); };
    const go = el.querySelector('[data-a=go]'); if (go) go.onclick = () => rebuild(false);
    const sh = el.querySelector('[data-a=shuffle]'); if (sh) sh.onclick = () => rebuild(true);
    el.querySelectorAll('.viz-ctl input').forEach(i => i.addEventListener('keydown', e => { if (e.key === 'Enter') rebuild(false); }));
    rebuild(true);
  }
  const parseNums = (s, max = 16) => {
    const a = String(s).split(/[\s,;]+/).filter(Boolean).map(Number);
    if (!a.length || a.some(x => !Number.isFinite(x))) throw new Error('введи числа через запятую');
    if (a.length > max) throw new Error(`не больше ${max} чисел — чтобы было наглядно`);
    return a;
  };

  // ---------- Сортировки ----------
  function bars(arr, mark = {}, done = new Set(), extra = '') {
    const mx = Math.max(...arr.map(Math.abs), 1);
    return `<div class="bars">${arr.map((v, i) => `<div class="bar ${mark[i] || ''} ${done.has(i) ? 'done' : ''}"><i style="height:${Math.max(6, Math.abs(v) / mx * 100)}%"></i><span>${esc(v)}</span><em>${i}</em></div>`).join('')}</div>${extra}`;
  }
  const SORTS = {
    selection(a, F) {
      const n = a.length, done = new Set();
      for (let i = 0; i < n - 1; i++) {
        let m = i;
        F(a, { [i]: 'cur', [m]: 'min' }, done, `i = ${i}: ищем минимум в a[${i}:]`);
        for (let j = i + 1; j < n; j++) {
          F(a, { [i]: 'cur', [m]: 'min', [j]: 'cmp' }, done, `сравниваем a[${j}] = ${a[j]} с текущим минимумом a[${m}] = ${a[m]}`, 'c');
          if (a[j] < a[m]) { m = j; F(a, { [i]: 'cur', [m]: 'min' }, done, `новый минимум: a[${m}] = ${a[m]}`); }
        }
        if (m !== i) { [a[i], a[m]] = [a[m], a[i]]; F(a, { [i]: 'swap', [m]: 'swap' }, done, `меняем a[${i}] и a[${m}] — минимум встал на место ${i}`, 's'); }
        done.add(i);
      }
      done.add(n - 1);
    },
    insertion(a, F) {
      const done = new Set([0]);
      for (let i = 1; i < a.length; i++) {
        const key = a[i]; let j = i - 1;
        F(a, { [i]: 'cur' }, done, `key = a[${i}] = ${key}: вставляем в отсортированную часть a[0:${i}]`);
        while (j >= 0) {
          F(a, { [j]: 'cmp', [j + 1]: 'cur' }, done, `a[${j}] = ${a[j]} > ${key}?`, 'c');
          if (!(a[j] > key)) break;
          a[j + 1] = a[j]; a[j] = key;
          F(a, { [j]: 'cur', [j + 1]: 'swap' }, done, `да — сдвигаем ${a[j + 1]} вправо`, 's');
          j--;
        }
        for (let t = 0; t <= i; t++) done.add(t);
        F(a, { [j + 1]: 'min' }, done, `key = ${key} встал на позицию ${j + 1}`);
      }
    },
    bubble(a, F) {
      const n = a.length, done = new Set();
      for (let i = 0; i < n - 1; i++) {
        let swapped = false;
        for (let j = 0; j < n - 1 - i; j++) {
          F(a, { [j]: 'cmp', [j + 1]: 'cmp' }, done, `проход ${i + 1}: a[${j}] = ${a[j]} > a[${j + 1}] = ${a[j + 1]}?`, 'c');
          if (a[j] > a[j + 1]) { [a[j], a[j + 1]] = [a[j + 1], a[j]]; swapped = true; F(a, { [j]: 'swap', [j + 1]: 'swap' }, done, 'да — меняем соседей', 's'); }
        }
        done.add(n - 1 - i);
        if (!swapped) { for (let t = 0; t < n; t++) done.add(t); F(a, {}, done, `за проход ${i + 1} не было обменов — массив отсортирован, выходим (флаг swapped)`); return; }
        F(a, {}, done, `проход ${i + 1} окончен: ${a[n - 1 - i]} «всплыл» на место ${n - 1 - i}`);
      }
      done.add(0);
    },
    merge(a, F) {
      const rec = (lo, hi, depth) => {
        if (hi - lo <= 1) return;
        const mid = (lo + hi) >> 1;
        const rng = {}; for (let t = lo; t < hi; t++) rng[t] = t < mid ? 'cur' : 'min';
        F(a, rng, new Set(), `делим a[${lo}:${hi}] на [${lo}:${mid}] и [${mid}:${hi}] (глубина ${depth})`);
        rec(lo, mid, depth + 1); rec(mid, hi, depth + 1);
        const L = a.slice(lo, mid), R = a.slice(mid, hi); let i = 0, j = 0, k = lo;
        while (i < L.length && j < R.length) {
          F(a, { [k]: 'cmp' }, new Set(), `сливаем: ${L[i]} (слева) ≤ ${R[j]} (справа)?`, 'c');
          a[k++] = L[i] <= R[j] ? L[i++] : R[j++];
          F(a, { [k - 1]: 'swap' }, new Set(), `записали ${a[k - 1]} в a[${k - 1}]`, 's');
        }
        while (i < L.length) { a[k++] = L[i++]; F(a, { [k - 1]: 'swap' }, new Set(), `дописываем остаток левой: ${a[k - 1]}`, 's'); }
        while (j < R.length) { a[k++] = R[j++]; F(a, { [k - 1]: 'swap' }, new Set(), `дописываем остаток правой: ${a[k - 1]}`, 's'); }
        const d = new Set(); for (let t = lo; t < hi; t++) d.add(t);
        F(a, {}, d, `a[${lo}:${hi}] отсортирован`);
      };
      rec(0, a.length, 0);
    },
    quick(a, F) {
      const done = new Set();
      const rec = (lo, hi) => {
        if (lo > hi) return;
        if (lo === hi) { done.add(lo); return; }
        const pivot = a[hi]; let i = lo;
        F(a, { [hi]: 'pivot' }, done, `partition a[${lo}..${hi}]: pivot = ${pivot} (последний)`);
        for (let j = lo; j < hi; j++) {
          F(a, { [hi]: 'pivot', [j]: 'cmp', [i]: 'cur' }, done, `a[${j}] = ${a[j]} < ${pivot}?  (граница меньших i = ${i})`, 'c');
          if (a[j] < pivot) { [a[i], a[j]] = [a[j], a[i]]; F(a, { [hi]: 'pivot', [i]: 'swap', [j]: 'swap' }, done, `да — обмен a[${i}] и a[${j}], i = ${i + 1}`, 's'); i++; }
        }
        [a[i], a[hi]] = [a[hi], a[i]]; done.add(i);
        F(a, { [i]: 'pivot' }, done, `pivot ${pivot} встал на своё окончательное место ${i}`, 's');
        rec(lo, i - 1); rec(i + 1, hi);
      };
      rec(0, a.length - 1);
    }
  };
  const SORT_NAMES = { selection: 'выбором', insertion: 'вставками', bubble: 'пузырьком', merge: 'слиянием', quick: 'быстрая (на месте, Ломуто)' };
  function sortViz(el, alg) {
    let data = rnd(10, 2, 30);
    player(el, 'Сортировка ' + SORT_NAMES[alg], `<input class="w" style="width:220px" data-i="arr" aria-label="массив">`, (root, fresh) => {
      const inp = root.querySelector('[data-i=arr]');
      if (fresh) { data = rnd(10, 2, 30); inp.value = data.join(', '); } else data = parseNums(inp.value);
      const a = data.slice(), frames = []; let cmp = 0, sw = 0;
      const F = (arr, mark, done, note, kind) => {
        if (kind === 'c') cmp++; if (kind === 's') sw++;
        frames.push({ html: bars(arr, mark, new Set(done)), note: `${note}<span class="pl-cnt">сравнений: <b>${cmp}</b> · ${alg === 'merge' ? 'записей' : alg === 'insertion' ? 'сдвигов' : 'обменов'}: <b>${sw}</b></span>` });
      };
      F(a, {}, new Set(), 'исходный массив');
      SORTS[alg](a, F);
      const all = new Set(a.map((_, i) => i));
      frames.push({ html: bars(a, {}, all), note: `<span class="ok">готово</span> · n = ${a.length}, сравнений ${cmp}, n² = ${a.length * a.length}<span class="pl-cnt">сравнений: <b>${cmp}</b></span>` });
      return frames;
    }, { shuffle: true });
    el.insertAdjacentHTML('beforeend', `<div class="pl-legend"><span><i class="lg cmp"></i>сравнение</span><span><i class="lg swap"></i>обмен / запись</span><span><i class="lg cur"></i>текущий</span><span><i class="lg min"></i>${alg === 'quick' ? 'граница' : 'минимум / вставлен'}</span>${alg === 'quick' ? '<span><i class="lg pivot"></i>pivot</span>' : ''}<span><i class="lg done"></i>на месте</span></div>`);
  }

  // ---------- Ячейки с указателями ----------
  function cells(arr, ptrs = {}, cls = {}, label = '') {
    const tags = {}; Object.entries(ptrs).forEach(([name, i]) => { if (i != null && i >= -1 && i <= arr.length) (tags[i] = tags[i] || []).push(name); });
    return `${label ? `<div class="cl-lbl">${label}</div>` : ''}<div class="cells">${arr.map((v, i) => `<div class="cell2 ${cls[i] || ''}"><em>${i}</em><b>${esc(v)}</b>${tags[i] ? `<span>${tags[i].join(' ')}</span>` : ''}</div>`).join('')}${tags[arr.length] ? `<div class="cell2 ghost"><em>${arr.length}</em><b></b><span>${tags[arr.length].join(' ')}</span></div>` : ''}</div>`;
  }
  const wrapRows = (...rows) => `<div class="rows">${rows.join('')}</div>`;

  function mergeViz(el) {
    player(el, 'Слияние двух отсортированных массивов', `<input class="w" style="width:140px" data-i="a" aria-label="массив a"><input class="w" style="width:140px" data-i="b" aria-label="массив b">`, (root, fresh) => {
      const ia = root.querySelector('[data-i=a]'), ib = root.querySelector('[data-i=b]');
      let a, b;
      if (fresh) { a = rnd(4, 1, 20).sort((x, y) => x - y); b = rnd(5, 1, 20).sort((x, y) => x - y); ia.value = a.join(', '); ib.value = b.join(', '); }
      else { a = parseNums(ia.value, 8); b = parseNums(ib.value, 8); if (a.some((x, i) => i && x < a[i - 1]) || b.some((x, i) => i && x < b[i - 1])) throw new Error('массивы должны быть отсортированы'); }
      const res = [], frames = []; let i = 0, j = 0;
      const F = (note, ca = {}, cb = {}) => frames.push({ html: wrapRows(cells(a, { i }, Object.assign({}, ...a.map((_, t) => t < i ? { [t]: 'used' } : {}), ca), 'a'), cells(b, { j }, Object.assign({}, ...b.map((_, t) => t < j ? { [t]: 'used' } : {}), cb), 'b'), cells(res.length ? res : [' '], {}, { [res.length - 1]: 'new' }, 'result')), note });
      F('i = 0, j = 0, result = []');
      while (i < a.length && j < b.length) {
        F(`сравниваем a[${i}] = ${a[i]} и b[${j}] = ${b[j]}`, { [i]: 'cmp' }, { [j]: 'cmp' });
        if (a[i] <= b[j]) { res.push(a[i]); i++; F(`${a[i - 1]} ≤ ${b[j]} → берём из a, i = ${i}`); }
        else { res.push(b[j]); j++; F(`${b[j - 1]} < ${a[i]} → берём из b, j = ${j}`); }
      }
      if (i < a.length) { while (i < a.length) res.push(a[i++]); F('b закончился — дописываем остаток a целиком'); }
      if (j < b.length) { while (j < b.length) res.push(b[j++]); F('a закончился — дописываем остаток b целиком'); }
      F(`<span class="ok">готово</span>: ${a.length} + ${b.length} = ${res.length} элементов, каждый взят один раз — O(n + m)`);
      return frames;
    }, { shuffle: true });
  }

  function twoPtrViz(el) {
    player(el, 'Палиндром: два указателя', `<input class="w" style="width:200px" data-i="s" value="шалаш" aria-label="строка">`, (root) => {
      const s = root.querySelector('[data-i=s]').value; if (s.length > 20) throw new Error('не больше 20 символов');
      const a = [...s], frames = []; let l = 0, r = a.length - 1;
      const F = (note, c = {}) => frames.push({ html: cells(a.map(x => x === ' ' ? '␣' : x), { left: l, right: r }, c), note });
      F(`left = 0, right = ${r}`);
      while (l < r) {
        if (a[l] !== a[r]) { F(`s[${l}] = '${a[l]}' ≠ s[${r}] = '${a[r]}' → <span class="err">не палиндром</span>`, { [l]: 'bad', [r]: 'bad' }); return frames; }
        F(`s[${l}] = '${a[l]}' == s[${r}] = '${a[r]}' → сдвигаем навстречу`, { [l]: 'okc', [r]: 'okc' });
        l++; r--;
      }
      F(`указатели встретились → <span class="ok">палиндром</span> · сравнений: ${Math.floor(a.length / 2)} из ${a.length} символов`);
      return frames;
    });
  }

  function windowViz(el) {
    player(el, 'Скользящее окно: подстрока без повторов', `<input class="w" style="width:200px" data-i="s" value="abcabcbb" aria-label="строка">`, (root) => {
      const s = root.querySelector('[data-i=s]').value; if (s.length > 20) throw new Error('не больше 20 символов');
      const a = [...s], frames = [], last = {}; let left = 0, bs = 0, bl = 0;
      const F = (right, note, extra = {}) => {
        const c = {}; for (let t = left; t <= right && t < a.length; t++) c[t] = 'win';
        for (let t = bs; t < bs + bl; t++) c[t] = (c[t] ? c[t] + ' ' : '') + 'best';
        Object.assign(c, extra);
        frames.push({ html: cells(a, { left, right }, c) + `<div class="cl-lbl" style="margin-top:12px">last = {${Object.entries(last).map(([k, v]) => `'${esc(k)}': ${v}`).join(', ')}}</div>`, note: note + `<span class="pl-cnt">лучшее: <b>"${esc(s.substr(bs, bl))}"</b> (${bl})</span>` });
      };
      for (let right = 0; right < a.length; right++) {
        const ch = a[right];
        if (ch in last && last[ch] >= left) {
          F(right, `'${ch}' уже есть в окне (на позиции ${last[ch]}) → left = ${last[ch] + 1}`, { [right]: 'bad', [last[ch]]: 'bad' });
          left = last[ch] + 1;
        }
        last[ch] = right;
        if (right - left + 1 > bl) { bs = left; bl = right - left + 1; }
        F(right, `окно [${left}, ${right}] = "${esc(s.slice(left, right + 1))}"`);
      }
      frames.push({ html: cells(a, {}, Object.fromEntries(Array.from({ length: bl }, (_, t) => [bs + t, 'best']))), note: `<span class="ok">ответ: "${esc(s.substr(bs, bl))}"</span>, длина ${bl} · right прошёл строку один раз — O(n)` });
      return frames;
    });
  }

  function bsearchViz(el) {
    let arr = [];
    player(el, 'Бинарный поиск', `<input class="w" style="width:220px" data-i="a" aria-label="отсортированный массив"><input data-i="t" aria-label="что ищем" placeholder="target">`, (root, fresh) => {
      const ia = root.querySelector('[data-i=a]'), it = root.querySelector('[data-i=t]');
      if (fresh) { arr = [...new Set(rnd(14, 1, 60))].sort((x, y) => x - y); ia.value = arr.join(', '); it.value = arr[Math.floor(Math.random() * arr.length)]; }
      else { arr = parseNums(ia.value, 20); if (arr.some((x, i) => i && x < arr[i - 1])) throw new Error('массив должен быть отсортирован'); }
      const t = Number(it.value); if (!Number.isFinite(t)) throw new Error('введи target');
      const frames = []; let lo = 0, hi = arr.length - 1, step = 0;
      const F = (mid, note, extra = {}) => { const c = {}; arr.forEach((_, i) => { if (i < lo || i > hi) c[i] = 'used'; }); Object.assign(c, extra); frames.push({ html: cells(arr, { lo, mid, hi }, c), note: note + `<span class="pl-cnt">шагов: <b>${step}</b> · log₂${arr.length} ≈ ${Math.ceil(Math.log2(arr.length + 1))}</span>` }); };
      F(null, `ищем ${t}: lo = 0, hi = ${hi}`);
      while (lo <= hi) {
        const mid = (lo + hi) >> 1; step++;
        if (arr[mid] === t) { F(mid, `a[${mid}] = ${arr[mid]} == ${t} → <span class="ok">нашли, индекс ${mid}</span>`, { [mid]: 'okc' }); return frames; }
        if (arr[mid] < t) { F(mid, `a[${mid}] = ${arr[mid]} < ${t} → искомое правее, lo = ${mid + 1}`, { [mid]: 'cmp' }); lo = mid + 1; }
        else { F(mid, `a[${mid}] = ${arr[mid]} > ${t} → искомое левее, hi = ${mid - 1}`, { [mid]: 'cmp' }); hi = mid - 1; }
      }
      F(null, `lo > hi → <span class="err">${t} нет в массиве, вернуть −1</span>`);
      return frames;
    }, { shuffle: true });
  }

  function linearViz(el, mode) {
    player(el, mode === 'minmax' ? 'Минимум и максимум за один проход' : 'Линейный поиск', `<input class="w" style="width:220px" data-i="a" aria-label="массив">${mode === 'minmax' ? '' : '<input data-i="t" placeholder="target" aria-label="что ищем">'}`, (root, fresh) => {
      const ia = root.querySelector('[data-i=a]'), it = root.querySelector('[data-i=t]');
      let arr;
      if (fresh) { arr = rnd(10, -20, 40); ia.value = arr.join(', '); if (it) it.value = arr[6]; } else arr = parseNums(ia.value, 18);
      const frames = [];
      if (mode === 'minmax') {
        let lo = arr[0], hi = arr[0], li = 0, hiI = 0;
        const F = (i, note) => frames.push({ html: cells(arr, { i }, { [li]: 'min2', [hiI]: 'max2', ...(i != null ? { [i]: 'cmp' } : {}) }), note: note + `<span class="pl-cnt">min = <b>${lo}</b> · max = <b>${hi}</b></span>` });
        F(0, `начинаем с первого элемента: min = max = ${arr[0]}`);
        for (let i = 1; i < arr.length; i++) {
          const x = arr[i];
          if (x < lo) { lo = x; li = i; F(i, `${x} < min → новый минимум`); }
          else if (x > hi) { hi = x; hiI = i; F(i, `${x} > max → новый максимум`); }
          else F(i, `${x} — не меньше min и не больше max`);
        }
        frames.push({ html: cells(arr, {}, { [li]: 'min2', [hiI]: 'max2' }), note: `<span class="ok">(min, max) = (${lo}, ${hi})</span> · один проход, ${arr.length} элементов — O(n)` });
      } else {
        const t = Number(it.value);
        for (let i = 0; i < arr.length; i++) {
          if (arr[i] === t) { frames.push({ html: cells(arr, { i }, { [i]: 'okc' }), note: `a[${i}] = ${arr[i]} == ${t} → <span class="ok">нашли, индекс ${i}</span> · сравнений: ${i + 1}` }); return frames; }
          frames.push({ html: cells(arr, { i }, { [i]: 'cmp', ...Object.fromEntries(Array.from({ length: i }, (_, k) => [k, 'used'])) }), note: `a[${i}] = ${arr[i]} ≠ ${t}` });
        }
        frames.push({ html: cells(arr, {}, Object.fromEntries(arr.map((_, k) => [k, 'used']))), note: `<span class="err">${t} не найден, −1</span> · просмотрены все ${arr.length} элементов — худший случай O(n)` });
      }
      return frames;
    }, { shuffle: true });
  }

  // ---------- Массив: вставка и удаление со сдвигом ----------
  function arrayViz(el) {
    el.innerHTML = `<div class="viz-h"><b>▶ Массив: сколько элементов сдвигается</b><span class="muted" style="font-size:13px">попробуй сам</span></div>
      <div class="viz-ctl"><input data-i="v" placeholder="знач." aria-label="значение"><input data-i="i" placeholder="idx" aria-label="индекс">
      <button class="p" data-a="append">append</button><button data-a="insert">insert(idx, v)</button><button data-a="pop">pop()</button><button data-a="popi">pop(idx)</button><button data-a="find">поиск v</button><span class="sep"></span><button data-a="reset">сброс</button></div>
      <div class="viz-stage"></div><div class="viz-log" aria-live="polite"></div>`;
    const stage = el.querySelector('.viz-stage'), log = el.querySelector('.viz-log');
    let a = [7, 2, 9, 4, 5], hl = {}, n = 10;
    const draw = () => { stage.innerHTML = cells(a.length ? a : [' '], {}, hl); hl = {}; };
    const val = () => { const i = el.querySelector('[data-i=v]'); const v = i.value.trim() || String(n++); i.value = ''; return isNaN(+v) ? v : +v; };
    const idx = (max) => { const v = parseInt(el.querySelector('[data-i=i]').value, 10); return isNaN(v) || v < 0 || v > max ? null : v; };
    const on = (k, f) => el.querySelector(`[data-a=${k}]`).onclick = f;
    on('append', () => { const v = val(); a.push(v); hl = { [a.length - 1]: 'new' }; draw(); log.innerHTML = `append(${esc(v)}) → в конец, <b>сдвигов 0</b> · O(1)`; });
    on('insert', () => { const i = idx(a.length); if (i === null) return log.innerHTML = `<span class="err">idx от 0 до ${a.length}</span>`; const v = val(); a.splice(i, 0, v); hl = { [i]: 'new' }; for (let t = i + 1; t < a.length; t++) hl[t] = 'cmp'; draw(); log.innerHTML = `insert(${i}, ${esc(v)}) → <b>сдвинуто вправо: ${a.length - 1 - i}</b> · O(n)`; });
    on('pop', () => { if (!a.length) return log.innerHTML = '<span class="err">IndexError: pop from empty list</span>'; const v = a.pop(); draw(); log.innerHTML = `pop() → ${esc(v)}, <b>сдвигов 0</b> · O(1)`; });
    on('popi', () => { const i = idx(a.length - 1); if (i === null || !a.length) return log.innerHTML = `<span class="err">idx от 0 до ${a.length - 1}</span>`; const v = a.splice(i, 1)[0]; for (let t = i; t < a.length; t++) hl[t] = 'cmp'; draw(); log.innerHTML = `pop(${i}) → ${esc(v)}, <b>сдвинуто влево: ${a.length - i}</b> · O(n)`; });
    on('find', () => { const raw = el.querySelector('[data-i=v]').value.trim(); if (!raw) return log.innerHTML = '<span class="err">введи значение</span>'; const v = isNaN(+raw) ? raw : +raw; const i = a.indexOf(v); for (let t = 0; t <= (i < 0 ? a.length - 1 : i); t++) hl[t] = 'used'; if (i >= 0) hl[i] = 'okc'; draw(); log.innerHTML = i >= 0 ? `нашли ${esc(v)} на позиции ${i} · <b>сравнений: ${i + 1}</b> · O(n)` : `<span class="err">${esc(v)} нет</span> · сравнений: ${a.length} — O(n)`; });
    on('reset', () => { a = [7, 2, 9, 4, 5]; draw(); log.innerHTML = ''; });
    draw(); log.innerHTML = 'Подсвечиваются элементы, которые пришлось сдвинуть. Сравни insert(0, …) и append';
  }

  // ---------- Дерево вызовов Фибоначчи ----------
  function recTree(el) {
    el.innerHTML = `<div class="viz-h"><b>▶ Дерево вызовов fib(n)</b><span class="muted" style="font-size:13px">попробуй сам</span></div>
      <div class="viz-ctl"><label class="muted" style="font-size:14px">n = <input type="range" min="1" max="7" value="5" data-i="n" style="width:120px;vertical-align:middle"> <b data-o="n">5</b></label>
      <span class="sep"></span><label style="font-size:14px;display:flex;gap:6px;align-items:center"><input type="checkbox" data-i="memo"> мемоизация</label></div>
      <div class="viz-stage" style="display:block;overflow-x:auto"></div><div class="viz-log"></div>`;
    const st = el.querySelector('.viz-stage'), lg = el.querySelector('.viz-log');
    const draw = () => {
      const n = +el.querySelector('[data-i=n]').value, memo = el.querySelector('[data-i=memo]').checked;
      el.querySelector('[data-o=n]').textContent = n;
      const seen = new Set(), cnt = {}; let calls = 0;
      const node = k => {
        calls++; cnt[k] = (cnt[k] || 0) + 1;
        if (memo && seen.has(k)) return `<li><span class="tn memo">fib(${k}) ✓ из memo</span></li>`;
        if (k <= 1) { seen.add(k); return `<li><span class="tn base">fib(${k}) = ${k}</span></li>`; }
        const kids = node(k - 1) + node(k - 2); seen.add(k);
        return `<li><span class="tn ${cnt[k] > 1 ? 'dup' : ''}">fib(${k})</span><ul>${kids}</ul></li>`;
      };
      const html = node(n);
      st.innerHTML = `<ul class="tree">${html}</ul>`;
      const dups = Object.entries(cnt).filter(([, c]) => c > 1).map(([k, c]) => `fib(${k})×${c}`).join(', ');
      lg.innerHTML = `вызовов: <b>${calls}</b> ${memo ? `· каждое значение считается один раз → ~2n вызовов, O(n)` : `· повторы: ${dups || 'нет'} · растёт как ~1.6ⁿ, то есть O(2ⁿ)`}`;
    };
    el.querySelectorAll('input').forEach(i => i.addEventListener('input', draw));
    draw();
  }

  // ---------- Рост функций Big O ----------
  function growth(el) {
    const FN = [
      ['O(1)', n => 1, '#13924f'], ['O(log n)', n => Math.log2(Math.max(n, 1)), '#0e9fb3'], ['O(n)', n => n, '#2357c6'],
      ['O(n log n)', n => n * Math.log2(Math.max(n, 1)), '#7c3aed'], ['O(n²)', n => n * n, '#c27a00'], ['O(2ⁿ)', n => 2 ** n, '#d1343b'], ['O(n!)', n => { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; }, '#8b0a3c']
    ];
    el.innerHTML = `<div class="viz-h"><b>▶ Как растёт число операций</b><span class="muted" style="font-size:13px">двигай n</span></div>
      <div class="viz-ctl"><label style="font-size:14px">n = <input type="range" min="1" max="40" value="10" data-i="n" style="width:200px;vertical-align:middle"> <b data-o="n">10</b></label></div>
      <div class="viz-stage" style="display:block"><svg class="gchart" viewBox="0 0 540 260" role="img" aria-label="график роста"></svg><div class="gtable"></div></div>`;
    const svg = el.querySelector('svg'), tbl = el.querySelector('.gtable'), inp = el.querySelector('[data-i=n]');
    const fmt = v => v >= 1e15 ? v.toExponential(1).replace('e+', '·10^') : v >= 1e6 ? (v / 1e6).toFixed(1) + ' млн' : Math.round(v * 10) / 10;
    const draw = () => {
      const n = +inp.value; el.querySelector('[data-o=n]').textContent = n;
      const W = 430, H = 210, X0 = 40, Y0 = 236, ymax = Math.max(n * n, 10);
      const X = x => X0 + (x - 1) / Math.max(n - 1, 1) * W, Y = y => Y0 - y / ymax * H;
      let paths = `<defs><clipPath id="gclip"><rect x="${X0}" y="${Y0 - H - 2}" width="${W + 2}" height="${H + 4}"/></clipPath></defs>
        <line x1="${X0}" y1="${Y0}" x2="${X0 + W}" y2="${Y0}" stroke="var(--line-2)"/><line x1="${X0}" y1="${Y0}" x2="${X0}" y2="${Y0 - H}" stroke="var(--line-2)"/>
        <text x="${X0 + W}" y="${Y0 + 16}" text-anchor="end" font-size="11" fill="var(--ink-3)">n = ${n}</text><text x="${X0 - 4}" y="${Y0 - H + 4}" text-anchor="end" font-size="10" fill="var(--ink-3)">${fmt(ymax)}</text><text x="${X0 - 4}" y="${Y0}" text-anchor="end" font-size="10" fill="var(--ink-3)">0</text>`;
      const labels = [];
      FN.forEach(([name, f, col]) => {
        let d = '', exitX = null;
        const step = name === 'O(n!)' ? 1 : Math.max((n - 1) / 160, 0.02);
        for (let x = 1; x <= n + 1e-9; x += step) {
          const y = f(x);
          d += (d ? 'L' : 'M') + X(x).toFixed(1) + ',' + Math.max(Y(Math.min(y, ymax * 3)), Y0 - H * 3).toFixed(1);
          if (y > ymax * 1.001) { exitX = x; break; }
        }
        paths += `<path d="${d}" fill="none" stroke="${col}" stroke-width="2.4" stroke-linejoin="round" clip-path="url(#gclip)"/>`;
        if (exitX === null) labels.push({ name, col, x: X0 + W + 4, y: Y(f(n)) + 4 });
        else labels.push({ name, col, x: Math.min(X(exitX) + 2, X0 + W - 30), y: Y0 - H - 6, top: true });
      });
      // раздвигаем подписи справа, чтобы не наезжали
      const side = labels.filter(l => !l.top).sort((a, b) => b.y - a.y);
      for (let i = 1; i < side.length; i++) if (side[i - 1].y - side[i].y < 12) side[i].y = side[i - 1].y - 12;
      const top = labels.filter(l => l.top).sort((a, b) => a.x - b.x);
      for (let i = 1; i < top.length; i++) if (top[i].x - top[i - 1].x < 52) top[i].x = top[i - 1].x + 52;
      labels.forEach(l => paths += `<text x="${l.x}" y="${l.y}" font-size="11" fill="${l.col}" font-weight="700">${l.name}${l.top ? ' ↑' : ''}</text>`);
      svg.innerHTML = paths;
      tbl.innerHTML = `<table class="ops" style="margin:14px 0 0"><tr><th>Класс</th><th>операций при n = ${n}</th><th>пример</th></tr>${FN.map(([name, f, col], i) => `<tr><td style="color:${col};font-weight:800">${name}</td><td>${fmt(f(n))}</td><td>${['a[i], append', 'бинарный поиск', 'линейный поиск, min/max', 'слиянием, быстрая', 'выбором, вставками, пузырьком', 'наивный Фибоначчи', 'все перестановки'][i]}</td></tr>`).join('')}</table><p class="muted" style="font-size:13px;margin-top:8px">Шкала графика обрезана по n² — 2ⁿ и n! улетают вверх уже при n ≈ 10.</p>`;
    };
    inp.addEventListener('input', draw); draw();
  }

  const base = window.VIZ.mount;
  window.VIZ.mount = function (el, type) {
    const [kind, arg] = type.split(':');
    const map1 = { sort: () => sortViz(el, arg), merge2: () => mergeViz(el), twoptr: () => twoPtrViz(el), window: () => windowViz(el), bsearch: () => bsearchViz(el), linear: () => linearViz(el, 'linear'), minmax: () => linearViz(el, 'minmax'), arrayops: () => arrayViz(el), rectree: () => recTree(el), growth: () => growth(el) };
    if (map1[kind]) { el.classList.add('viz'); map1[kind](); } else base(el, type);
  };
})();
