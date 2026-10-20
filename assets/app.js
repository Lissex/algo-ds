(function () {
  const app = document.getElementById('app');
  const T = window.TOPICS, M = window.METHODS, TK = window.TICKETS, P = window.PROBLEMS, Q = window.THEORY_Q, C = window.CODE;
  const topic = id => T.find(t => t.id === id);
  const prob = n => P.find(p => p.n === n);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const strip = h => String(h).replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/g, ' ').replace(/\s+/g, ' ').trim();
  const REPO = 'https://github.com/Bunyod2002/Data-structures';
  const lcUrl = p => `https://leetcode.com/problems/${p.slug}/`;

  // ---------- хранилище (безопасно) ----------
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  };
  // выбранный раздел: 1 — алгоритмы, 2 — структуры данных
  let SEC = store.get('sec', 2) === 1 ? 1 : 2;
  const QS = window.QUESTIONS1 || [];
  const LEARN_KEY = { 1: 'learned1', 2: 'learned' };
  const learnedSets = { 1: new Set(store.get('learned1', [])), 2: new Set(store.get('learned', [])) };
  let learned = learnedSets[SEC];
  const toggleLearned = (n, sec = SEC) => { const L = learnedSets[sec]; L.has(n) ? L.delete(n) : L.add(n); store.set(LEARN_KEY[sec], [...L]); };
  const TS = () => T.filter(t => t.section === SEC);
  const PS = () => P.filter(p => p.section === SEC);
  const qOfTopic = id => QS.filter(q => q.topic === id).map(q => q.n);
  function setSec(s, silent) {
    SEC = s === 1 ? 1 : 2; learned = learnedSets[SEC]; store.set('sec', SEC);
    document.querySelectorAll('.sec-switch button').forEach(b => b.classList.toggle('on', +b.dataset.sec === SEC));
    const tk = document.querySelector('[data-nav=tickets]');
    if (tk) { tk.textContent = SEC === 1 ? 'Вопросы' : 'Билеты'; tk.setAttribute('href', SEC === 1 ? '#/q' : '#/tickets'); }
    const te = document.querySelector('[data-nav=teacher]'); if (te) te.hidden = SEC === 1;
    const sm = document.querySelector('.logo-text small'); if (sm) sm.textContent = 'раздел ' + SEC;
  }

  // ---------- переключатель разделов ----------
  (function () {
    const tools = document.querySelector('.top-tools');
    const sw = document.createElement('div');
    sw.className = 'sec-switch'; sw.setAttribute('role', 'group'); sw.setAttribute('aria-label', 'Раздел');
    sw.innerHTML = '<button data-sec="1" title="Алгоритмы">Раздел 1</button><button data-sec="2" title="Структуры данных">Раздел 2</button>';
    tools.insertBefore(sw, tools.firstChild);
    sw.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      const s = +b.dataset.sec; if (s === SEC) return;
      setSec(s);
      const a = location.hash.replace(/^#\/?/, '').split('/')[0];
      const listOf = { topics: '#/topics', tickets: s === 1 ? '#/q' : '#/tickets', q: s === 1 ? '#/q' : '#/tickets', problems: '#/problems', practice: '#/practice', exam: '#/exam', teacher: '#/' };
      const target = listOf[a] || '#/';
      if (location.hash === target || (target === '#/' && !a)) route(); else location.hash = target;
    });
  })();
  setSec(SEC);

  // ---------- тема ----------
  document.getElementById('themeBtn').addEventListener('click', () => {
    const root = document.documentElement;
    const cur = root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) { }
  });

  // ---------- подсветка Python ----------
  const KW = new Set('False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield'.split(' '));
  const BI = new Set('len range print enumerate zip min max sum list dict set tuple str int float bool isinstance super object type abs sorted reversed map filter any all divmod IndexError ValueError KeyError AttributeError TypeError Exception Optional List deque'.split(' '));
  function hl(src) {
    const re = /(#[^\n]*)|([rbfRBF]{0,2}"""[\s\S]*?"""|[rbfRBF]{0,2}'''[\s\S]*?'''|[rbfRBF]{0,2}"(?:\\.|[^"\\\n])*"|[rbfRBF]{0,2}'(?:\\.|[^'\\\n])*')|(@\w+)|\b(0x[0-9a-fA-F]+|\d+\.?\d*)\b|([A-Za-z_]\w*)/g;
    let out = '', last = 0, m, prevWord = '';
    while ((m = re.exec(src))) {
      out += esc(src.slice(last, m.index)); last = re.lastIndex;
      const [t] = m;
      if (m[1]) out += `<span class="tk-com">${esc(t)}</span>`;
      else if (m[2]) out += `<span class="tk-str">${esc(t)}</span>`;
      else if (m[3]) out += `<span class="tk-dec">${esc(t)}</span>`;
      else if (m[4]) out += `<span class="tk-num">${esc(t)}</span>`;
      else {
        if (prevWord === 'def') out += `<span class="tk-fn">${t}</span>`;
        else if (prevWord === 'class') out += `<span class="tk-cls">${t}</span>`;
        else if (KW.has(t)) out += `<span class="tk-kw">${t}</span>`;
        else if (t === 'self') out += `<span class="tk-self">${t}</span>`;
        else if (BI.has(t)) out += `<span class="tk-bi">${t}</span>`;
        else out += t;
        prevWord = t; continue;
      }
      prevWord = '';
    }
    return out + esc(src.slice(last));
  }

  // ---------- блок кода (с вкладками) ----------
  let codeId = 0; const codeStore = {};
  function codeBlock(items, opts = {}) {
    // items: [{label, src, file}]
    items = items.filter(x => x.src);
    if (!items.length) return '';
    const id = 'cb' + (codeId++);
    codeStore[id] = items.map(x => x.src);
    const long = items.some(x => x.src.split('\n').length > 28) && !opts.full;
    return `<div class="code ${long ? 'collapsed' : ''}" id="${id}">
      <div class="code-h"><div class="tabs">${items.map((x, i) => `<button class="${i ? '' : 'on'}" data-tab="${i}">${esc(x.label)}</button>`).join('')}</div>
      <div class="acts"><button data-copy>копировать</button>${opts.download ? `<a href="code/${esc(items[0].file)}" download>.py</a>` : ''}</div></div>
      <pre><code>${hl(items[0].src)}</code></pre>${long ? '<button class="more">показать полностью ↓</button>' : ''}</div>`;
  }
  function wireCode(root) {
    root.querySelectorAll('.code').forEach(cb => {
      const items = codeStore[cb.id];
      let cur = 0;
      cb.querySelectorAll('[data-tab]').forEach(b => b.addEventListener('click', () => {
        cur = +b.dataset.tab; cb.querySelector('code').innerHTML = hl(items[cur]);
        cb.querySelectorAll('[data-tab]').forEach(x => x.classList.toggle('on', x === b));
      }));
      const cp = cb.querySelector('[data-copy]');
      cp.addEventListener('click', async () => {
        try { await navigator.clipboard.writeText(items[cur]); cp.textContent = 'скопировано ✓'; }
        catch (e) { const r = document.createRange(); r.selectNodeContents(cb.querySelector('code')); const s = getSelection(); s.removeAllRanges(); s.addRange(r); cp.textContent = 'выделено — Ctrl+C'; }
        setTimeout(() => cp.textContent = 'копировать', 1600);
      });
      const more = cb.querySelector('.more');
      if (more) more.addEventListener('click', () => { cb.classList.remove('collapsed'); more.remove(); });
    });
  }
  const snip = k => k.endsWith('::*') ? (C.files[k.slice(0, -3)] || '') : (C.snip[k] || '');
  const fileLabel = k => k.split('::')[0].split('/').pop();
  const snipLabel = k => { const [f, n] = k.split('::'); return n === '*' ? f.split('/').pop() : n.includes('.') ? n.split('.').pop() + '()' : n + (/^[a-z_]/.test(n) ? '()' : ''); };

  // ---------- общие куски ----------
  const ticketsForTopic = id => TK.filter(t => t.theory === id || M[t.method].topic === id).map(t => t.n);
  const chipsQ = ns => ns.map(n => `<a class="chip" href="#/q/${n}">вопрос ${n}</a>`).join('');
  const ticketsForProblem = n => TK.filter(t => t.lc === n).map(t => t.n);
  const chipsTickets = ns => ns.map(n => `<a class="chip" href="#/tickets/${n}">билет ${n}</a>`).join('');
  const opsTable = ops => `<div class="tbl-wrap"><table class="ops"><tr><th>Операция</th><th>Время</th><th>Память</th><th>Почему так</th></tr>${ops.map(o => `<tr><td>${esc(o[0])}</td><td>${esc(o[1])}</td><td>${esc(o[2])}</td><td>${esc(o[3])}</td></tr>`).join('')}</table></div>`;
  const BIGO_NOTE = `<p class="muted" style="font-size:14px"><b>Время</b> — сколько шагов делает операция в худшем случае. <b>Память</b> — сколько <i>дополнительной</i> памяти ей нужно, не считая самой структуры (O(1) — несколько переменных, сколько бы ни было элементов). <b>*</b> и «амортизированно» — иногда операция дорогая, но в среднем на серию операций выходит указанная оценка.</p>`;
  const examWithSpace = t => wrapTables(t.exam) + `<p><b>Память:</b> ${t.space}</p>`;
  const tmKv = (time, mem, why) => `<dl class="kv"><dt>Время</dt><dd>${time}</dd><dt>Память</dt><dd>${mem}</dd></dl><div class="callout why"><span class="lbl">почему так</span><p>${why}</p></div>`;
  const wrapTables = html => html.replace(/<table class="cmp">/g, '<div class="tbl-wrap"><table class="cmp">').replace(/<\/table>/g, '</table></div>');

  function page(html, nav) {
    app.innerHTML = `<div class="page">${html}</div>`;
    document.querySelectorAll('[data-nav]').forEach(a => a.classList.toggle('on', a.dataset.nav === nav));
    wireCode(app);
    app.querySelectorAll('[data-viz]').forEach(el => window.VIZ.mount(el, el.dataset.viz));
    const trHelpers = { codeBlock, wire: wireCode };
    const mountTr = el => { if (!el.dataset.mounted) { el.dataset.mounted = 1; window.TRAINER.mount(el, el.dataset.trainer, trHelpers); } };
    app.querySelectorAll('[data-trainer]').forEach(el => { if (!el.closest('[hidden]')) mountTr(el); });
    app.querySelectorAll('.qtabs').forEach(tb => {
      const panes = tb.parentElement.querySelectorAll(':scope > [data-qp]');
      tb.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
        tb.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b));
        panes.forEach(p => { p.hidden = p.dataset.qp !== b.dataset.qt; if (!p.hidden) p.querySelectorAll('[data-trainer]').forEach(mountTr); });
        if (b.dataset.qt === '1') window.TRAINER.warm();
      }));
    });
    app.querySelectorAll('[data-learn]').forEach(b => b.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      const n = +b.dataset.learn; toggleLearned(n);
      const on = learned.has(n);
      b.classList.toggle('on', on); b.textContent = on ? '✓ выучен' : 'отметить выученным';
      const card = b.closest('.tk'); if (card) card.classList.toggle('done', on);
      const pr = document.getElementById('prog'); if (pr) pr.innerHTML = progHtml();
    }));
  }
  const learnBtn = n => `<button class="learn ${learned.has(n) ? 'on' : ''}" data-learn="${n}">${learned.has(n) ? '✓ выучен' : 'отметить выученным'}</button>`;
  const progHtml = () => { const tot = SEC === 1 ? QS.length : TK.length; return `<div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px"><span>Выучено ${SEC === 1 ? 'вопросов' : 'билетов'}</span><b>${learned.size} / ${tot}</b></div><div class="progress"><i style="width:${learned.size / tot * 100}%"></i></div>`; };

  function ticketCard(t) {
    const p = prob(t.lc);
    return `<a class="card tk ${learned.has(t.n) ? 'done' : ''}" href="#/tickets/${t.n}">
      <div class="tk-h"><span class="tk-n"><small>билет</small>${t.n}</span></div>
      <ol><li>${esc(Q[t.theory])}</li><li>${esc(M[t.method].title)}</li><li>LeetCode ${p.n} · ${esc(p.title)}</li></ol>
      <div>${learnBtn(t.n)}</div></a>`;
  }

  // ---------- страницы ----------
  function home() {
    const heroArt2 = `<div class="hero-art" aria-hidden="true">
      <div class="ha-lbl">linked list</div>
      <div class="ha-row"><span class="ha-arr" style="padding-left:0">head</span><span class="ha-arr">→</span><span class="ha-node on">5</span><span class="ha-arr">→</span><span class="ha-node">8</span><span class="ha-arr">→</span><span class="ha-node">2</span><span class="ha-arr">→</span><span class="ha-arr blink">None</span></div>
      <div class="ha-lbl">hashset · buckets</div>
      <div class="ha-row"><span class="ha-arr" style="padding-left:0">0 ┃</span><span class="ha-node">cat</span><span class="ha-arr">→</span><span class="ha-node on">owl</span></div>
      <div class="ha-row" style="margin-top:-8px"><span class="ha-arr" style="padding-left:0">1 ┃</span><span class="ha-arr">None</span></div>
      <div class="ha-row" style="margin-top:-8px"><span class="ha-arr" style="padding-left:0">2 ┃</span><span class="ha-node">dog</span></div>
      <div class="ha-lbl">stack · LIFO</div>
      <div class="ha-row"><span class="ha-node">1</span><span class="ha-node" style="margin-left:5px">7</span><span class="ha-node on" style="margin-left:5px">3</span><span class="ha-arr blink">← top</span></div>
    </div>`;
    const hb = [12, 20, 7, 28, 16, 24, 9, 31, 14, 22];
    const heroArt1 = `<div class="hero-art" aria-hidden="true">
      <div class="ha-lbl">sorting · O(n log n)</div>
      <div style="display:flex;align-items:flex-end;gap:5px;height:120px;margin:12px 0 18px">${hb.map((v, i) => `<div style="flex:1;height:${v / 31 * 100}%;border-radius:4px 4px 1px 1px;background:${i === 3 || i === 7 ? '#c8f53c' : '#3a3f49'}"></div>`).join('')}</div>
      <div class="ha-lbl">binary search · O(log n)</div>
      <div class="ha-row">${[3, 8, 15, 21, 34, 42, 57].map((v, i) => `<span class="ha-node ${i === 3 ? 'on' : ''}" style="margin-right:4px;${i < 2 || i > 5 ? 'opacity:.35' : ''}">${v}</span>`).join('')}</div>
      <div class="ha-lbl">recursion</div>
      <div class="ha-row" style="font-size:13px;color:#c5c8ce">fib(n) = fib(n−1) + fib(n−2)<span class="ha-arr blink">▍</span></div>
    </div>`;
    const ts = TS(), ps = PS();
    const s1 = SEC === 1;
    page(`<div class="wrap">
      <section class="hero">
        <div><div class="eyebrow">алгоритмы и структуры данных · раздел ${SEC}</div>
          ${s1 ? `<h1>Алгоритмы <em>без зубрёжки</em></h1>
          <p class="lead">Big O, сортировки, рекурсия, бинарный поиск, два указателя и скользящее окно. Теория с пошаговыми анимациями, ответы на 15 вопросов и разбор 18 задач LeetCode на Python.</p>
          <div class="hero-cta"><a class="btn pri" href="#/q">Вопросы →</a><a class="btn" href="#/exam">Тренировка экзамена</a><a class="btn" href="#/practice">✍ Тренажёр</a></div>`
          : `<h1>Структуры данных <em>без зубрёжки</em></h1>
          <p class="lead">Стек, очередь, связанные списки, deque, кольцевой массив и хэширование. Теория с живыми моделями, 15 билетов с готовыми ответами и разбор 14 задач LeetCode на Python.</p>
          <div class="hero-cta"><a class="btn pri" href="#/tickets">Билеты →</a><a class="btn" href="#/exam">Тренировка экзамена</a><a class="btn" href="#/practice">✍ Тренажёр</a></div>`}
        </div>${s1 ? heroArt1 : heroArt2}
      </section>
      <div class="stats">
        <a class="card stat" href="#/topics" style="text-decoration:none;color:inherit"><b>${ts.length}</b><span>тем с ${s1 ? 'анимациями' : 'моделями'}</span></a>
        <a class="card stat" href="${s1 ? '#/q' : '#/tickets'}" style="text-decoration:none;color:inherit"><b>${s1 ? QS.length : TK.length}</b><span>${s1 ? 'вопросов' : 'билетов'} с ответами</span></a>
        <a class="card stat" href="#/problems" style="text-decoration:none;color:inherit"><b>${ps.length}</b><span>задач LeetCode</span></a>
        <div class="card stat" id="prog" style="display:flex;flex-direction:column;justify-content:center">${progHtml()}</div>
      </div>
      <section class="sec"><div class="sec-h"><h2>Темы</h2><a href="#/topics">все темы →</a></div>
        <div class="grid g3">${ts.map((t, i) => topicCard(t, i)).join('')}</div></section>
      <section class="sec"><div class="sec-h"><h2>${s1 ? 'Вопросы' : 'Билеты'}</h2><a href="${s1 ? '#/q' : '#/tickets'}">все ${s1 ? 'вопросы' : 'билеты'} →</a></div>
        <div class="grid g3">${s1 ? QS.slice(0, 6).map(questionCard).join('') : TK.slice(0, 6).map(ticketCard).join('')}</div></section>
      <p class="muted" style="margin-top:36px;font-size:14px">Другой раздел — переключатель «Раздел 1 · Раздел 2» в шапке.</p>
    </div>`, '');
  }
  const topicCard = (t, i) => `<a class="card tcard" href="#/topics/${t.id}"><span class="num">${String(i + 1).padStart(2, '0')} · ${esc(t.tag)}</span><h3>${esc(t.title)}</h3><p>${esc(t.summary)}</p><div class="chips">${t.section === 1 ? qOfTopic(t.id).map(n => `<span class="chip">в. ${n}</span>`).join('') : ticketsForTopic(t.id).map(n => `<span class="chip">б. ${n}</span>`).join('')}</div></a>`;
  function questionCard(q) {
    const tp = topic(q.topic);
    return `<a class="card tk ${learned.has(q.n) ? 'done' : ''}" href="#/q/${q.n}">
      <div class="tk-h"><span class="tk-n"><small>вопрос</small>${q.n}</span>${q.ex ? '<span class="chip">✍ код</span>' : ''}</div>
      <p class="q-text">${esc(q.text)}</p>
      <div>${learnBtn(q.n)}</div></a>`;
  }

  function topics() {
    page(`<div class="wrap"><div class="eyebrow">теория</div><h1>Темы раздела ${SEC}</h1>
      <p class="lead">В каждой теме: короткий ответ для экзамена, подробное объяснение, ${SEC === 1 ? 'пошаговая анимация' : 'интерактивная модель'}, время и память и код на Python.</p>
      <div class="grid g3" style="margin-top:28px">${TS().map(topicCard).join('')}</div></div>`, 'topics');
  }

  function topicPage(id) {
    const t = topic(id); if (!t) return notFound();
    if (t.section !== SEC) setSec(t.section);
    const TT = TS(), i = TT.indexOf(t), prev = TT[i - 1], next = TT[i + 1];
    const codeItems = t.code.map((k, i) => ({ label: (t.codeLabels && t.codeLabels[i]) || snipLabel(k), src: snip(k), file: k.split('::')[0] }));
    const tks = t.section === 1 ? [] : ticketsForTopic(id), qs = t.section === 1 ? qOfTopic(id) : [];
    const relProbs = P.filter(p => p.topic === id);
    page(`<div class="wrap">
      <div class="eyebrow"><a href="#/topics">теория</a> / ${String(i + 1).padStart(2, '0')} · ${esc(t.tag)}</div>
      <h1>${esc(t.title)}</h1><p class="lead">${esc(t.summary)}</p>
      <div class="topic-layout"><article class="prose">
        <section id="exam"><div class="exam-ans"><span class="lbl">ответ на экзамене</span>${examWithSpace(t)}</div></section>
        ${t.viz ? `<section id="model"><h2>${t.section === 1 ? 'Анимация' : 'Модель'}</h2><div data-viz="${t.viz}"></div></section>` : ''}
        <section id="details"><h2>Подробнее</h2>${wrapTables(t.body)}</section>
        <section id="ops"><h2>Сложность: время и память</h2>${BIGO_NOTE}${opsTable(t.ops)}<h3>Память самой структуры</h3><p>${t.space}</p></section>
        <section id="code"><h2>Код на Python</h2>${codeBlock(codeItems, { download: codeItems.length === 1 })}
          <p class="muted" style="font-size:14px">${t.section === 1 ? 'Код проверен тестами: пустые массивы, дубликаты, случайные данные.' : `Код основан на <a href="${REPO}" target="_blank" rel="noopener">репозитории преподавателя</a>, проверен тестами.`}</p></section>
        ${relProbs.length ? `<section id="lc"><h2>Задачи LeetCode на эту тему</h2><div class="card plist">${relProbs.map(p => `<a class="prow" href="#/problems/${p.n}"><span class="pn">${p.n}</span><span class="pt"><b>${esc(p.title)}</b><span>${esc(p.ru)} · <span class="diff ${p.diff}">${p.diff}</span></span></span><span></span><span class="ptk">${p.time}</span></a>`).join('')}</div></section>` : ''}
        <section id="links"><h2>Ссылки</h2><ul>${t.links.map(l => `<li><a href="${esc(l[1])}" target="_blank" rel="noopener">${esc(l[0])}</a></li>`).join('')}</ul></section>
        <div class="ticket-nav">${prev ? `<a class="btn" href="#/topics/${prev.id}">← ${esc(prev.title)}</a>` : '<span></span>'}${next ? `<a class="btn" href="#/topics/${next.id}">${esc(next.title)} →</a>` : ''}</div>
      </article>
      <aside class="toc"><b>на странице</b>
        <a href="#/topics/${id}" data-jump="exam">Ответ на экзамене</a>${t.viz ? `<a href="#/topics/${id}" data-jump="model">Модель</a>` : ''}<a href="#/topics/${id}" data-jump="details">Подробнее</a><a href="#/topics/${id}" data-jump="ops">Сложность</a><a href="#/topics/${id}" data-jump="code">Код</a><a href="#/topics/${id}" data-jump="links">Ссылки</a>
        ${tks.length ? `<b style="margin-top:22px">в билетах</b><div class="chips">${chipsTickets(tks)}</div>` : ''}${qs.length ? `<b style="margin-top:22px">вопрос</b><div class="chips">${chipsQ(qs)}</div>` : ''}
        <b style="margin-top:22px">связанные темы</b><div class="chips">${t.related.map(r => `<a class="chip" href="#/topics/${r}">${esc(topic(r).title)}</a>`).join('')}</div>
      </aside></div></div>`, 'topics');
    app.querySelectorAll('[data-jump]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); document.getElementById(a.dataset.jump).scrollIntoView({ behavior: 'smooth' }); }));
  }

  let tkFilter = 'all';
  function tickets() {
    if (SEC !== 2) setSec(2);
    const list = TK.filter(t => tkFilter === 'all' || (tkFilter === 'todo' ? !learned.has(t.n) : learned.has(t.n)));
    page(`<div class="wrap"><div class="eyebrow">раздел 2</div><h1>Билеты</h1>
      <p class="lead">В каждом билете три вопроса: теория, реализация метода и задача LeetCode. Отмечай выученные билеты, прогресс сохранится в этом браузере.</p>
      <div style="display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin:26px 0 18px">
        <div class="tk-filters">${[['all', 'Все'], ['todo', 'Не выучены'], ['done', 'Выучены']].map(([k, l]) => `<button data-f="${k}" class="${tkFilter === k ? 'on' : ''}">${l}</button>`).join('')}</div>
        <div id="prog" style="min-width:240px">${progHtml()}</div></div>
      <div class="grid g3">${list.map(ticketCard).join('') || '<p class="muted">Здесь пока пусто.</p>'}</div></div>`, 'tickets');
    app.querySelectorAll('[data-f]').forEach(b => b.addEventListener('click', () => { tkFilter = b.dataset.f; tickets(); }));
  }

  function methodBlock(mid) {
    const m = M[mid];
    const items = [{ label: snipLabel(m.snip), src: snip(m.snip) }];
    (m.extra || []).forEach(k => items.push({ label: snipLabel(k) + ' (вспомог.)', src: snip(k) }));
    if (m.alt) items.push({ label: 'на двусвязном списке', src: snip(m.alt) });
    return `${codeBlock(items)}
      <h3>Как работает</h3><ol class="steps">${m.steps.map(s => `<li>${s}</li>`).join('')}</ol>
      <h3>Сложность</h3>${tmKv(m.time, m.mem, m.why)}
      <dl class="kv"><dt>Крайние случаи</dt><dd>${m.edges.join(' · ')}</dd></dl>
      ${m.note ? `<div class="callout info">${m.note}</div>` : ''}
      <p><a href="#/topics/${m.topic}">Тема «${esc(topic(m.topic).title)}» с моделью →</a></p>`;
  }
  function problemBlock(p, short) {
    return `<p>${p.task}</p><div class="example">${esc(p.example)}</div>
      <h3>Идея решения</h3><p>${p.idea}</p>
      <h3>Сложность</h3>${tmKv(p.time, p.mem, p.why)}
      ${codeBlock([{ label: p.file.split('/').pop(), src: C.files[p.file], file: p.file }], { download: true })}
      <p><a href="${lcUrl(p)}" target="_blank" rel="noopener">Открыть задачу на LeetCode ↗</a>${short ? ` · <a href="#/problems/${p.n}">страница задачи</a>` : ''}</p>`;
  }
  const withTrainer = (exId, body) => `<div class="qtabs"><button class="on" data-qt="0">Разбор</button><button data-qt="1">✍ Написать самому${trainerDone(exId) ? ' ✓' : ''}</button></div>
    <div data-qp="0">${body}</div><div data-qp="1" hidden><div data-trainer="${exId}"></div></div>`;
  const THEORY_EX = { stack: 'stack-list', queue: 'queue-list' };
  const trainerDone = id => window.TRAINER.solved().has(id);
  const qCard = (n, kind, title, body) => `<section class="card q"><div class="q-h"><span class="q-n">${n}</span><div><div class="q-kind">${kind}</div><h2>${title}</h2></div></div><div class="q-b">${body}</div></section>`;

  function ticketPage(n) {
    const t = TK.find(x => x.n === n); if (!t) return notFound();
    if (SEC !== 2) setSec(2);
    const tp = topic(t.theory), m = M[t.method], p = prob(t.lc);
    const prev = TK.find(x => x.n === n - 1), next = TK.find(x => x.n === n + 1);
    page(`<div class="wrap narrow">
      <div class="eyebrow"><a href="#/tickets">билеты</a> / раздел 2</div>
      <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap"><h1 style="margin:0">Билет ${n}</h1>${learnBtn(n)}</div>
      ${qCard(1, 'теория', esc(Q[t.theory]), (() => { const body = `<div class="exam-ans"><span class="lbl">ответ</span>${examWithSpace(tp)}</div><p style="margin-top:14px"><a href="#/topics/${tp.id}">Полная тема с моделью и кодом →</a></p>`; const ex = THEORY_EX[t.theory]; return ex ? withTrainer(ex, body) : body; })())}
      ${qCard(2, 'реализация', 'Реализовать метод ' + esc(m.title), withTrainer(t.method, methodBlock(t.method)))}
      ${qCard(3, `задача LeetCode ${p.n} · <span class="diff ${p.diff}">${p.diff}</span>`, `${esc(p.title)} <span class="muted" style="font-weight:500;font-size:.8em">— ${esc(p.ru)}</span>`, withTrainer('lc-' + p.n, problemBlock(p, true)))}
      <div class="ticket-nav">${prev ? `<a class="btn" href="#/tickets/${prev.n}">← Билет ${prev.n}</a>` : '<span></span>'}<a class="btn" href="#/exam">Случайный билет</a>${next ? `<a class="btn" href="#/tickets/${next.n}">Билет ${next.n} →</a>` : '<span></span>'}</div>
    </div>`, 'tickets');
  }

  // ---------- вопросы раздела 1 ----------
  function questions() {
    if (SEC !== 1) setSec(1);
    const list = QS.filter(q => tkFilter === 'all' || (tkFilter === 'todo' ? !learned.has(q.n) : learned.has(q.n)));
    page(`<div class="wrap"><div class="eyebrow">раздел 1 · алгоритмы</div><h1>Вопросы</h1>
      <p class="lead">15 вопросов к экзамену. В каждом — готовый ответ, анимация, оценка времени и памяти; где нужно что-то реализовать — код и тренажёр с проверкой.</p>
      <div style="display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin:26px 0 18px">
        <div class="tk-filters">${[['all', 'Все'], ['todo', 'Не выучены'], ['done', 'Выучены']].map(([k, l]) => `<button data-f="${k}" class="${tkFilter === k ? 'on' : ''}">${l}</button>`).join('')}</div>
        <div id="prog" style="min-width:240px">${progHtml()}</div></div>
      <div class="grid g3">${list.map(questionCard).join('') || '<p class="muted">Здесь пока пусто.</p>'}</div></div>`, 'tickets');
    app.querySelectorAll('[data-f]').forEach(b => b.addEventListener('click', () => { tkFilter = b.dataset.f; questions(); }));
  }
  function questionPage(n) {
    const q = QS.find(x => x.n === n); if (!q) return notFound();
    if (SEC !== 1) setSec(1);
    const tp = topic(q.topic), prev = QS.find(x => x.n === n - 1), next = QS.find(x => x.n === n + 1);
    const rel = P.filter(p => p.topic === q.topic);
    let k = 1;
    const answer = `<div class="exam-ans"><span class="lbl">ответ</span>${examWithSpace(tp)}</div>
      <h3>Время и память</h3>${opsTable(tp.ops)}
      <p style="margin-top:14px"><a href="#/topics/${tp.id}">Полная тема: подробности, код и ссылки →</a></p>`;
    page(`<div class="wrap narrow">
      <div class="eyebrow"><a href="#/q">вопросы</a> / раздел 1</div>
      <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap"><h1 style="margin:0">Вопрос ${n}</h1>${learnBtn(n)}</div>
      <p class="lead" style="margin-top:12px">${esc(q.text)}</p>
      ${qCard(k++, 'теория', esc(tp.title), answer)}
      ${tp.viz ? qCard(k++, 'анимация', 'Посмотри, как это работает', `<div data-viz="${tp.viz}"></div>`) : ''}
      ${q.ex ? qCard(k++, 'реализация', esc(M[q.ex].title), withTrainer(q.ex, methodBlock(q.ex))) : ''}
      ${q.ex2 ? qCard(k++, 'реализация', esc(M[q.ex2].title), withTrainer(q.ex2, methodBlock(q.ex2))) : ''}
      ${rel.length ? qCard(k++, 'практика', 'Задачи LeetCode на эту тему', `<div class="chips">${rel.map(p => `<a class="chip" href="#/problems/${p.n}">${p.n}. ${esc(p.title)}</a>`).join('')}</div>`) : ''}
      <div class="ticket-nav">${prev ? `<a class="btn" href="#/q/${prev.n}">← Вопрос ${prev.n}</a>` : '<span></span>'}<a class="btn" href="#/exam">Случайный вопрос</a>${next ? `<a class="btn" href="#/q/${next.n}">Вопрос ${next.n} →</a>` : '<span></span>'}</div>
    </div>`, 'tickets');
  }

  function problems() {
    page(`<div class="wrap"><div class="eyebrow">leetcode · раздел ${SEC}</div><h1>Задачи</h1>
      <p class="lead">${SEC === 1 ? 'Задачи первого раздела' : 'Все задачи из билетов'}: условие, идея, решение на Python, время и память с объяснением.</p>
      <div class="card plist" style="margin-top:26px">${PS().map(p => `<a class="prow" href="#/problems/${p.n}"><span class="pn">${p.n}</span><span class="pt"><b>${esc(p.title)}</b><span>${esc(p.ru)} · <span class="diff ${p.diff}">${p.diff}</span></span></span>
        <span class="chips">${p.tags.map(x => `<span class="chip">${esc(x)}</span>`).join('')}</span><span class="ptk">${p.section === 1 ? esc(topic(p.topic).title) : 'билет ' + ticketsForProblem(p.n).join(', ')}</span></a>`).join('')}</div></div>`, 'problems');
  }
  function problemPage(n) {
    const p = prob(n); if (!p) return notFound();
    if (p.section !== SEC) setSec(p.section);
    const PP = PS(), i = PP.indexOf(p), prev = PP[i - 1], next = PP[i + 1];
    page(`<div class="wrap narrow"><div class="eyebrow"><a href="#/problems">задачи</a> / leetcode ${p.n} · <span class="diff ${p.diff}">${p.diff}</span></div>
      <h1>${esc(p.title)}</h1><p class="lead">${esc(p.ru)}</p>
      <div class="chips" style="margin:14px 0 26px">${p.tags.map(x => `<span class="chip acc">${esc(x)}</span>`).join('')}${chipsTickets(ticketsForProblem(p.n))}${p.topic ? `<a class="chip" href="#/topics/${p.topic}">тема: ${esc(topic(p.topic).title)}</a>` : ''}</div>
      <div class="card" style="padding:22px">${withTrainer('lc-' + p.n, '<h3 style="margin-top:0">Условие</h3>' + problemBlock(p, false))}</div>
      <div class="ticket-nav">${prev ? `<a class="btn" href="#/problems/${prev.n}">← ${prev.n}. ${esc(prev.title)}</a>` : '<span></span>'}${next ? `<a class="btn" href="#/problems/${next.n}">${next.n}. ${esc(next.title)} →</a>` : ''}</div></div>`, 'problems');
  }

  // ---------- режим экзамена ----------
  let examTimer = null;
  function exam() {
    clearInterval(examTimer);
    if (SEC === 1) return exam1();
    const pool = TK.filter(t => !learned.has(t.n));
    const src = pool.length ? pool : TK;
    const t = src[Math.floor(Math.random() * src.length)];
    const tp = topic(t.theory), m = M[t.method], p = prob(t.lc);
    const hidden = (body) => `<div class="reveal hidden"><button class="btn pri reveal-btn">Показать ответ</button><div class="reveal-body">${body}</div></div>`;
    page(`<div class="wrap narrow"><div class="eyebrow">тренировка</div>
      <div class="exam-top"><h1 style="margin:0">Билет ${t.n}</h1><div style="display:flex;gap:10px;align-items:center"><span class="timer" id="timer">00:00</span><button class="btn" id="again">Другой билет ↻</button></div></div>
      <p class="lead" style="margin-top:10px">Ответь на вопросы сам, засеки время, потом открой ответы. ${pool.length ? `Билеты берутся из ещё не выученных (${pool.length}).` : 'Все билеты выучены, берём любой.'}</p>
      ${qCard(1, 'теория', esc(Q[t.theory]), hidden(`<div class="exam-ans">${examWithSpace(tp)}</div>`))}
      ${qCard(2, 'реализация', 'Реализовать метод ' + esc(m.title), `<p class="muted" style="font-size:14px">Напиши метод в редакторе и нажми «Проверить». Ответ — ниже.</p><div data-trainer="${t.method}"></div><h3>Ответ</h3>` + hidden(methodBlock(t.method)))}
      ${qCard(3, `задача LeetCode ${p.n}`, esc(p.title) + ` <span class="muted" style="font-weight:500;font-size:.8em">— ${esc(p.ru)}</span>`, `<p>${p.task}</p><div class="example">${esc(p.example)}</div><div data-trainer="lc-${p.n}"></div><h3>Разбор</h3>` + hidden(`<h3>Идея</h3><p>${p.idea}</p>${codeBlock([{ label: p.file.split('/').pop(), src: C.files[p.file] }])}`))}
      <div class="ticket-nav"><span>${learnBtn(t.n)}</span><a class="btn" href="#/tickets/${t.n}">Открыть билет полностью →</a></div></div>`, 'exam');
    app.querySelectorAll('.reveal-btn').forEach(b => b.addEventListener('click', () => b.parentElement.classList.remove('hidden')));
    document.getElementById('again').addEventListener('click', exam);
    const t0 = Date.now(), el = document.getElementById('timer');
    examTimer = setInterval(() => {
      if (!document.body.contains(el)) return clearInterval(examTimer);
      const s = Math.floor((Date.now() - t0) / 1000); el.textContent = `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
    }, 1000);
  }

  function exam1() {
    const pool = QS.filter(q => !learned.has(q.n)), src = pool.length ? pool : QS;
    const q = src[Math.floor(Math.random() * src.length)], tp = topic(q.topic);
    const hidden = (body) => `<div class="reveal hidden"><button class="btn pri reveal-btn">Показать ответ</button><div class="reveal-body">${body}</div></div>`;
    let k = 1;
    const impl = id => qCard(++k, 'реализация', esc(M[id].title), `<p class="muted" style="font-size:14px">Напиши код и нажми «Проверить». Ответ — ниже.</p><div data-trainer="${id}"></div><h3>Ответ</h3>` + hidden(methodBlock(id)));
    page(`<div class="wrap narrow"><div class="eyebrow">тренировка · раздел 1</div>
      <div class="exam-top"><h1 style="margin:0">Вопрос ${q.n}</h1><div style="display:flex;gap:10px;align-items:center"><span class="timer" id="timer">00:00</span><button class="btn" id="again">Другой вопрос ↻</button></div></div>
      <p class="lead" style="margin-top:10px">${esc(q.text)}</p>
      <p class="muted">Ответь вслух или на бумаге, назови время и память, потом открой ответ. ${pool.length ? `Вопросы берутся из ещё не выученных (${pool.length}).` : 'Все вопросы выучены, берём любой.'}</p>
      ${qCard(1, 'теория', esc(tp.title), hidden(`<div class="exam-ans">${examWithSpace(tp)}</div>${opsTable(tp.ops)}`))}
      ${q.ex ? impl(q.ex) : ''}${q.ex2 ? impl(q.ex2) : ''}
      <div class="ticket-nav"><span>${learnBtn(q.n)}</span><a class="btn" href="#/q/${q.n}">Открыть вопрос полностью →</a></div></div>`, 'exam');
    app.querySelectorAll('.reveal-btn').forEach(b => b.addEventListener('click', () => b.parentElement.classList.remove('hidden')));
    document.getElementById('again').addEventListener('click', exam);
    const t0 = Date.now(), el = document.getElementById('timer');
    examTimer = setInterval(() => {
      if (!document.body.contains(el)) return clearInterval(examTimer);
      const s = Math.floor((Date.now() - t0) / 1000); el.textContent = `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
    }, 1000);
  }

  // ---------- код преподавателя ----------
  const BUGS = {
    'Hash_set.py': ['<b>add:</b> при коллизии (дописывание в конец цепочки) нет <code>self.size += 1</code> — size меньше реального количества ключей.', '<b>remove:</b> <code>while head:</code> + <code>head.next.key</code> → <code>AttributeError</code>, если ключа нет в цепочке. Нужно <code>while head.next:</code>.'],
    'Hash_table.py': ['<b>__getitem__:</b> <code>while head.next:</code> пропускает последний узел цепочки (KeyError для существующего ключа) и падает на пустой корзине. Нужно <code>while head:</code>.', '<b>remove:</b> в цикле нет <code>head = head.next</code> — бесконечный цикл, если ключ не второй в цепочке.', '<b>keys():</b> опечатка <code>j.keys</code> → должно быть <code>j.key</code>.']
  };
  const FIXED = { 'Hash_set.py': 'hashset', 'Hash_table.py': 'hashtable', 'Linked_list.py': 'linked-list', 'Double_linked_list.py': 'doubly-linked-list', 'Deque.py': 'deque' };
  function teacher() {
    if (SEC !== 2) setSec(2);
    const files = Object.keys(C.files).filter(f => f.startsWith('teacher/'));
    page(`<div class="wrap narrow"><div class="eyebrow">исходники</div><h1>Код преподавателя</h1>
      <p class="lead">Файлы из репозитория <a href="${REPO}" target="_blank" rel="noopener">Bunyod2002/Data-structures</a> без изменений. Найденные ошибки отмечены. Исправленные версии лежат в соответствующих темах.</p>
      ${files.map(f => { const name = f.split('/').pop(); return `<section class="sec" id="${name}"><div class="sec-h"><h2 style="font-family:var(--f-mono);font-size:20px">${esc(name)}</h2><span class="chips"><a class="chip" href="#/topics/${FIXED[name]}">тема →</a><a class="chip" href="${REPO}/blob/main/${esc(name)}" target="_blank" rel="noopener">GitHub ↗</a></span></div>
        ${BUGS[name] ? `<div class="callout warn">${BUGS[name].map(b => `<p>${b}</p>`).join('')}</div>` : ''}${codeBlock([{ label: name, src: C.files[f], file: f }], { download: true })}</section>`; }).join('')}
    </div>`, 'teacher');
  }

  // ---------- тренажёр ----------
  const practiceItems = () => [
    ...Object.entries(M).filter(([, m]) => m.section === SEC).map(([id, m]) => { if (m.section === 1) { const qs = QS.filter(q => q.ex === id || q.ex2 === id).map(q => q.n); return { id, kind: 'метод', title: m.title, sub: 'вопрос ' + qs.join(', '), topic: m.topic }; } const own = TK.filter(t => t.method === id).map(t => t.n), th = TK.filter(t => t.theory === m.topic).map(t => t.n); return { id, kind: 'метод', title: m.title, sub: own.length ? 'билеты ' + own.join(', ') : 'теория, билет ' + th.join(', '), topic: m.topic }; }),
    ...PS().map(p => ({ id: 'lc-' + p.n, kind: 'LeetCode ' + p.n, title: p.title, sub: p.ru + ' · ' + p.diff + (p.section === 1 ? ' · ' + topic(p.topic).title : ' · билет ' + ticketsForProblem(p.n).join(', ')) }))
  ];
  function practice() {
    const done = window.TRAINER.solved(), items = practiceItems();
    const n = items.filter(x => done.has(x.id)).length;
    const row = x => `<a class="prow" href="#/practice/${x.id}"><span class="pn">${done.has(x.id) ? '<span style="color:var(--accent)">✓</span>' : '○'}</span><span class="pt"><b>${esc(x.title)}</b><span>${esc(x.sub)}</span></span><span></span><span class="ptk">${esc(x.kind)}</span></a>`;
    page(`<div class="wrap"><div class="eyebrow">практика · раздел ${SEC}</div><h1>Тренажёр</h1>
      <p class="lead">Пиши код прямо в браузере. «Запустить» выполняет твой код, «Проверить» прогоняет скрытые тесты с крайними случаями. Python работает на твоём устройстве, ничего устанавливать не нужно.</p>
      <div class="card" style="padding:16px 20px;margin:24px 0 10px;max-width:420px"><div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px"><span>Решено заданий</span><b>${n} / ${items.length}</b></div><div class="progress"><i style="width:${n / items.length * 100}%"></i></div></div>
      <section class="sec" style="margin-top:28px"><div class="sec-h"><h2>${SEC === 1 ? 'Алгоритмы из вопросов' : 'Методы из билетов'}</h2></div><div class="card plist">${items.filter(x => x.kind === 'метод').map(row).join('')}</div></section>
      <section class="sec"><div class="sec-h"><h2>Задачи LeetCode</h2></div><div class="card plist">${items.filter(x => x.kind !== 'метод').map(row).join('')}</div></section></div>`, 'practice');
  }
  function practicePage(id) {
    const want = M[id] ? M[id].section : (prob(+id.slice(3)) || {}).section;
    if (want && want !== SEC) setSec(want);
    const items = practiceItems(), i = items.findIndex(x => x.id === id);
    if (i < 0) return notFound();
    const prev = items[i - 1], next = items[i + 1];
    let head;
    if (M[id]) {
      const m = M[id];
      head = `<div class="eyebrow"><a href="#/practice">тренажёр</a> / ${m.section === 1 ? 'алгоритм' : 'метод'}</div><h1>${esc(m.title)}</h1>
        <p class="lead">${m.lead || 'Реализуй метод в классе ниже: остальные методы уже написаны.'} ${m.section === 1 ? 'Вопрос ' + QS.filter(q => q.ex === id || q.ex2 === id).map(q => `<a href="#/q/${q.n}">${q.n}</a>`).join(', ') : 'Встречается в билетах ' + TK.filter(t => t.method === id || (m.lead && t.theory === m.topic)).map(t => `<a href="#/tickets/${t.n}">${t.n}</a>`).join(', ')}.</p>
        <div class="chips" style="margin:12px 0 20px"><span class="chip" style="white-space:normal">время ${m.time}</span><span class="chip">память ${m.mem}</span><a class="chip" href="#/topics/${m.topic}">тема: ${esc(topic(m.topic).title)}</a></div>
        <details class="hint"><summary>Подсказка: план решения</summary><ol class="steps">${m.steps.map(s => `<li>${s}</li>`).join('')}</ol><p class="muted">Крайние случаи: ${m.edges.join(' · ')}</p><p class="muted">${m.why}</p></details>`;
    } else {
      const p = prob(+id.slice(3));
      head = `<div class="eyebrow"><a href="#/practice">тренажёр</a> / leetcode ${p.n} · <span class="diff ${p.diff}">${p.diff}</span></div><h1>${esc(p.title)}</h1><p class="lead">${esc(p.ru)}</p>
        <div class="card" style="padding:18px 20px;margin:18px 0"><p>${p.task}</p><div class="example">${esc(p.example)}</div></div>
        <details class="hint"><summary>Подсказка: идея решения</summary><p>${p.idea}</p><p class="muted">Время ${p.time}, память ${p.mem}.</p><p class="muted">${p.why}</p></details>`;
    }
    page(`<div class="wrap narrow">${head}<div data-trainer="${id}"></div>
      <div class="ticket-nav">${prev ? `<a class="btn" href="#/practice/${prev.id}">← ${esc(prev.title)}</a>` : '<span></span>'}${next ? `<a class="btn" href="#/practice/${next.id}">${esc(next.title)} →</a>` : ''}</div></div>`, 'practice');
  }

  function notFound() { page(`<div class="wrap"><h1>Страница не найдена</h1><p><a href="#/">На главную</a></p></div>`, ''); }

  // ---------- роутер ----------
  function route() {
    const h = location.hash.replace(/^#\/?/, '');
    const [a, b] = h.split('/');
    if (!a) home();
    else if (a === 'topics' && b) topicPage(b);
    else if (a === 'topics') topics();
    else if (a === 'tickets' && b) ticketPage(+b);
    else if (a === 'tickets') tickets();
    else if (a === 'q' && b) questionPage(+b);
    else if (a === 'q') questions();
    else if (a === 'problems' && b) problemPage(+b);
    else if (a === 'problems') problems();
    else if (a === 'exam') exam();
    else if (a === 'practice' && b) practicePage(b);
    else if (a === 'practice') practice();
    else if (a === 'teacher') teacher();
    else notFound();
    window.scrollTo(0, 0);
    const h1 = app.querySelector('h1');
    document.title = (h1 && a ? h1.textContent + ' · ' : '') + 'АиСД · Раздел ' + SEC;
  }
  window.addEventListener('hashchange', route);
  route();

  // ---------- поиск ----------
  const idx = [];
  QS.forEach(q => idx.push({ k: 'вопрос', t: `Вопрос ${q.n} (раздел 1)`, s: q.text, u: `#/q/${q.n}`, x: q.text }));
  T.forEach(t => idx.push({ k: 'тема ' + t.section, t: t.title, s: t.summary, u: `#/topics/${t.id}`, x: strip(t.tag + ' ' + t.exam + ' ' + t.body) }));
  TK.forEach(t => idx.push({ k: 'билет', t: `Билет ${t.n}`, s: `${Q[t.theory]} · ${M[t.method].title} · LeetCode ${t.lc}`, u: `#/tickets/${t.n}`, x: `билет ${t.n} ${Q[t.theory]} ${M[t.method].title} ${prob(t.lc).title}` }));
  P.forEach(p => idx.push({ k: 'задача ' + p.section, t: `${p.n}. ${p.title}`, s: p.ru, u: `#/problems/${p.n}`, x: strip(`${p.n} ${p.title} ${p.ru} ${p.tags.join(' ')} ${p.task} ${p.idea}`) }));
  Object.entries(M).forEach(([id, m]) => idx.push({ k: m.section === 1 ? 'тренажёр' : 'метод', t: m.title, s: TK.some(t => t.method === id) ? 'Билеты ' + TK.filter(t => t.method === id).map(t => t.n).join(', ') : 'Тренажёр', u: TK.find(t => t.method === id) ? `#/tickets/${TK.find(t => t.method === id).n}` : `#/practice/${id}`, x: strip(m.steps.join(' ')) }));
  const modal = document.getElementById('searchModal'), inp = document.getElementById('searchInput'), res = document.getElementById('searchResults');
  let sel = 0, found = [];
  const norm = s => s.toLowerCase().replace(/ё/g, 'е');
  function doSearch() {
    const q = norm(inp.value.trim());
    if (!q) { found = idx.filter(e => e.k === 'тема ' + SEC); }
    else {
      const words = q.split(/\s+/);
      found = idx.map(e => {
        const t = norm(e.t + ' ' + e.s), x = norm(e.x); let sc = 0;
        for (const w of words) { if (t.includes(w)) sc += 3; else if (x.includes(w)) sc += 1; else return null; }
        if (norm(e.t).startsWith(q)) sc += 5;
        return { e, sc };
      }).filter(Boolean).sort((a, b) => b.sc - a.sc).slice(0, 14).map(r => r.e);
    }
    sel = 0;
    const mark = s => { let h = esc(s); if (!q) return h; q.split(/\s+/).forEach(w => { if (w.length > 1) h = h.replace(new RegExp('(' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<mark>$1</mark>'); }); return h; };
    res.innerHTML = found.length ? found.map((e, i) => `<a href="${e.u}" class="${i === sel ? 'sel' : ''}"><span class="sk">${e.k}</span><span><b>${mark(e.t)}</b><span class="ss">${mark(e.s)}</span></span></a>`).join('') : '<div class="search-empty">Ничего не нашлось. Попробуй «стек», «коллизия», «reverse» или номер задачи.</div>';
  }
  const openSearch = () => { modal.hidden = false; inp.value = ''; doSearch(); inp.focus(); };
  const closeSearch = () => { modal.hidden = true; };
  document.getElementById('searchBtn').addEventListener('click', openSearch);
  modal.addEventListener('click', e => { if (e.target === modal) closeSearch(); });
  res.addEventListener('click', e => { if (e.target.closest('a')) closeSearch(); });
  inp.addEventListener('input', doSearch);
  inp.addEventListener('keydown', e => {
    const links = res.querySelectorAll('a');
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault(); if (!links.length) return;
      sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
      links.forEach((a, i) => a.classList.toggle('sel', i === sel)); links[sel].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter' && links[sel]) { location.hash = links[sel].getAttribute('href'); closeSearch(); }
    else if (e.key === 'Escape') closeSearch();
  });
  document.addEventListener('keydown', e => {
    const typing = /INPUT|TEXTAREA/.test(document.activeElement.tagName);
    if ((e.key === '/' && !typing) || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) { e.preventDefault(); openSearch(); }
    else if (e.key === 'Escape' && !modal.hidden) closeSearch();
  });
})();
