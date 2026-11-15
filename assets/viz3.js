// Пошаговые модели деревьев и кучи для раздела 3.
(function () {
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let uid = 0;
  const playbacks = new WeakMap();
  const id = () => ++uid;
  const copy = n => n ? ({...n, left: copy(n.left), right: copy(n.right)}) : null;
  const labelOf = n => n.key ?? n.val;

  function controls(el) {
    const old = el.querySelector('.viz-playback'); if (old) old.remove();
    el.querySelector('.viz-log').insertAdjacentHTML('afterend', `<div class="viz-playback"><div class="viz-ctl">
      <button data-step="first" title="в начало" aria-label="В начало">⏮</button>
      <button data-step="prev" title="шаг назад" aria-label="Шаг назад">◀</button>
      <button class="p" data-step="play" title="воспроизвести">▶ пуск</button>
      <button data-step="next" title="шаг вперёд" aria-label="Шаг вперёд">▶︎|</button>
      <button data-step="last" title="в конец" aria-label="В конец">⏭</button>
      <select data-step="speed" aria-label="скорость"><option value="900">медленно</option><option value="450" selected>нормально</option><option value="150">быстро</option></select>
      </div><div class="pl-bar"><input data-step="range" type="range" min="0" value="0" aria-label="шаг"><span data-step="count" class="pl-pos"></span></div></div>`);
  }
  function animate(el, frames, draw) {
    const previous = playbacks.get(el); if (previous) previous();
    controls(el);
    const stage = el.querySelector('.viz-stage'), log = el.querySelector('.viz-log');
    const first = el.querySelector('[data-step=first]'), prev = el.querySelector('[data-step=prev]'), next = el.querySelector('[data-step=next]'), last = el.querySelector('[data-step=last]'), play = el.querySelector('[data-step=play]');
    const range = el.querySelector('[data-step=range]'), count = el.querySelector('[data-step=count]'), speed = el.querySelector('[data-step=speed]');
    let at = 0, timer = null;
    range.max = Math.max(0, frames.length - 1);
    const totalSteps = Math.max(0, frames.steps ?? frames.length - 2);
    const show = () => {
      const f = frames[at] || frames[0];
      if (f && !f.active) f.active = [];
      draw(stage, f);
      log.textContent = f.note;
      range.value = at;
      const shownStep = Math.min(totalSteps, at);
      count.textContent = `шаг ${shownStep} / ${totalSteps}`;
      first.disabled = prev.disabled = at === 0;
      next.disabled = last.disabled = at === frames.length - 1;
      play.disabled = frames.length < 2;
    };
    const stop = () => { clearInterval(timer); timer = null; play.textContent = '▶ пуск'; };
    playbacks.set(el, stop);
    const step = n => { at = Math.max(0, Math.min(frames.length - 1, n)); show(); if (at === frames.length - 1) stop(); };
    first.onclick = () => { stop(); step(0); };
    prev.onclick = () => { stop(); step(at - 1); };
    next.onclick = () => { stop(); step(at + 1); };
    last.onclick = () => { stop(); step(frames.length - 1); };
    range.oninput = () => { stop(); step(+range.value); };
    play.onclick = () => {
      if (timer) { stop(); return; }
      if (at >= frames.length - 1) step(0);
      play.textContent = '⏸ пауза';
      timer = setInterval(() => { if (!document.body.contains(el)) { stop(); return; } step(at + 1); }, +speed.value);
    };
    speed.onchange = () => { if (timer) { stop(); play.click(); } };
    show();
  }

  function drawBinary(stage, root, active = [], title = '', aux = null) {
    const nodes = []; let xIndex = 0, maxDepth = 0;
    function visit(n, depth) {
      if (!n) return;
      maxDepth = Math.max(maxDepth, depth);
      visit(n.left, depth + 1);
      nodes.push({n, depth, xIndex: xIndex++});
      visit(n.right, depth + 1);
    }
    visit(root, 0);
    const w = Math.max(460, nodes.length * 78 + 32), h = Math.max(170, (maxDepth + 1) * 86 + 30);
    const pos = new Map(nodes.map(({n, depth, xIndex:i}) => [n, {x: 32 + (i + .5) * (w - 64) / Math.max(1, nodes.length), y: 38 + depth * 78}]));
    const edges = [];
    nodes.forEach(({n}) => [n.left,n.right].filter(Boolean).forEach(ch => { const a=pos.get(n),b=pos.get(ch); edges.push(`<line x1="${a.x}" y1="${a.y+21}" x2="${b.x}" y2="${b.y-21}" stroke="var(--line-2)" stroke-width="2"/>`); }));
    const dots = nodes.map(({n}) => {
      const p=pos.get(n), hot=active.includes(n.id), val=labelOf(n), extra=aux?aux(n):'';
      return `<g><circle cx="${p.x}" cy="${p.y}" r="25" fill="${hot?'var(--hl)':'var(--card)'}" stroke="${hot?'var(--accent)':'var(--line-2)'}" stroke-width="${hot?3:2}"/><text x="${p.x}" y="${p.y+6}" text-anchor="middle" fill="${hot?'#11140a':'var(--ink)'}" font-size="16" font-weight="750">${esc(val)}</text>${extra?`<text x="${p.x}" y="${p.y+40}" text-anchor="middle" fill="var(--ink-2)" font-size="12">${esc(extra)}</text>`:''}</g>`;
    }).join('');
    stage.innerHTML = `<div class="muted" style="font-size:12px;margin:0 0 4px">${esc(title)}</div><svg viewBox="0 0 ${w} ${h}" style="width:100%;max-height:400px">${edges.join('')}${dots}</svg>`;
  }
  function drawHeap(stage, a, active, isMin) {
    let root = null;
    if (a.length) {
      const ns = a.map((v,i)=>({val:v,id:i,left:null,right:null}));
      ns.forEach((n,i)=>{if(i) {const p=ns[(i-1)>>1]; if(i%2) p.left=n; else p.right=n;}});
      root = ns[0];
    }
    drawBinary(stage,root,active.map(i=>i),`${isMin?'min':'max'}-heap · индекс i: дети 2i+1 и 2i+2`);
    stage.insertAdjacentHTML('beforeend', `<div style="display:flex;gap:6px;flex-wrap:wrap;margin:12px 0">${a.map((v,i)=>`<span style="padding:6px 10px;border-radius:7px;background:${active.includes(i)?'var(--hl)':'var(--bg-2)'};color:${active.includes(i)?'#11140a':'var(--ink)'};font:600 14px var(--f-mono)">${v}<small style="color:${active.includes(i)?'#36420f':'var(--ink-2)'}">[${i}]</small></span>`).join('')}</div>`);
  }
  function frame(root, note, active = []) { return {root:copy(root), note, active}; }

  function bst(el, avlMode) {
    const kind=avlMode?'AVL-дерево':'Бинарное дерево поиска';
    el.innerHTML=`<div class="viz-h"><b>▶ ${kind}</b><span class="muted" style="font-size:13px">сравнения, вставка, поиск${avlMode?' и балансировка':''}</span></div><div class="viz-ctl"><input data-v type="number" value="12" aria-label="ключ"><button class="p" data-a="add">вставить</button><button data-a="find">найти</button><button data-a="remove">удалить</button><button data-a="reset">сбросить</button></div><div class="viz-stage"></div><div class="viz-log" aria-live="polite"></div>`;
    const node=key=>({id:id(),key,left:null,right:null,height:0});
    let root=null;
    const height=n=>n?n.height:-1;
    const update=n=>{n.height=1+Math.max(height(n.left),height(n.right));};
    const snapshot=(frames,note,active=[])=>frames.push(frame(root,note,active));
    function rotateRight(a,frames){const b=a.left,mid=b.right;b.right=a;a.left=mid;update(a);update(b);if(root===a)root=b;snapshot(frames,`Правый поворот вокруг ${a.key}: ${b.key} поднимается выше.`,[a.id,b.id]);return b;}
    function rotateLeft(a,frames){const b=a.right,mid=b.left;b.left=a;a.right=mid;update(a);update(b);if(root===a)root=b;snapshot(frames,`Левый поворот вокруг ${a.key}: ${b.key} поднимается выше.`,[a.id,b.id]);return b;}
    function rebalance(n,frames){
      update(n); const b=height(n.left)-height(n.right);
      snapshot(frames,`Обновляем высоту ${n.key}: h=${n.height}, баланс=${b}.`,[n.id]);
      if(b>1){if(height(n.left.left)<height(n.left.right)){snapshot(frames,`Случай LR: сначала левый поворот в левом поддереве узла ${n.key}.`,[n.id,n.left.id]);n.left=rotateLeft(n.left,frames);}return rotateRight(n,frames);}
      if(b< -1){if(height(n.right.right)<height(n.right.left)){snapshot(frames,`Случай RL: сначала правый поворот в правом поддереве узла ${n.key}.`,[n.id,n.right.id]);n.right=rotateRight(n.right,frames);}return rotateLeft(n,frames);}
      return n;
    }
    function insert(n,k,frames){
      if(!n){const made=node(k); if(avlMode) update(made);snapshot(frames,`Пустое место найдено: вставляем ${k}.`,[made.id]);return made;}
      snapshot(frames,`${k} ${k<n.key?'меньше':'больше'} ${n.key}: ${k<n.key?'идём влево':'идём вправо'}.`,[n.id]);
      if(k<n.key){n.left=insert(n.left,k,frames);snapshot(frames,`Цепляем ${k} слева от ${n.key}.`,[n.id,n.left.id]);}
      else if(k>n.key){n.right=insert(n.right,k,frames);snapshot(frames,`Цепляем ${k} справа от ${n.key}.`,[n.id,n.right.id]);}
      else{snapshot(frames,`Ключ ${k} уже есть: дубликат не добавляем.`,[n.id]);return n;}
      return avlMode?rebalance(n,frames):n;
    }
    function remove(n,k,frames){
      if(!n){snapshot(frames,`Дошли до пустой ссылки: ключа ${k} нет.`);return null;}
      if(k<n.key){snapshot(frames,`${k} < ${n.key}: спускаемся влево.`,[n.id]);n.left=remove(n.left,k,frames);snapshot(frames,`Возвращаемся к ${n.key} и обновляем левую ссылку.`,[n.id,...(n.left?[n.left.id]:[])]);}
      else if(k>n.key){snapshot(frames,`${k} > ${n.key}: спускаемся вправо.`,[n.id]);n.right=remove(n.right,k,frames);snapshot(frames,`Возвращаемся к ${n.key} и обновляем правую ссылку.`,[n.id,...(n.right?[n.right.id]:[])]);}
      else {
        snapshot(frames,`Нашли ${k}. Проверяем его детей.`,[n.id]);
        if(!n.left){snapshot(frames,n.right?`У узла один ребёнок: поднимаем ${n.right.key} на его место.`:`Лист ${k} удаляется.`,[n.id,...(n.right?[n.right.id]:[])]);return n.right;}
        if(!n.right){snapshot(frames,`Поднимаем единственного ребёнка ${n.left.key} на место ${k}.`,[n.id,n.left.id]);return n.left;}
        let s=n.right;while(s.left){snapshot(frames,`Ищем inorder-преемника: у ${s.key} есть левый ребёнок.`,[s.id]);s=s.left;}
        snapshot(frames,`Преемник ${s.key} заменяет удаляемый ключ ${k}.`,[n.id,s.id]);n.key=s.key;n.right=remove(n.right,s.key,frames);
      }
      return avlMode&&n?rebalance(n,frames):n;
    }
    const val=()=>Number(el.querySelector('[data-v]').value);
    function run(action){const frames=[frame(root,`Начало операции «${action}».`)];const k=val();
      if(action==='add'){root=insert(root,k,frames);frames.push(frame(root,`Вставка ${k} завершена.`));}
      if(action==='remove'){root=remove(root,k,frames);frames.push(frame(root,`Удаление ${k} завершено.`));}
      if(action==='find'){let n=root;while(n){snapshot(frames,`Сравниваем ${k} с ${n.key}.`,[n.id]);if(k===n.key)break;n=k<n.key?n.left:n.right;}snapshot(frames,n?`Ключ ${k} найден.`:`Ключ ${k} отсутствует.`,n?[n.id]:[]);}
      const aux=avlMode?n=>`h=${n.height} · b=${height(n.left)-height(n.right)}`:null;
      animate(el,frames,(stage,f)=>{stage.classList.add('viz-stage-stack');drawBinary(stage,f.root,f.active,kind,aux);});
    }
    el.querySelector('[data-a=add]').onclick=()=>run('add');
    el.querySelector('[data-a=remove]').onclick=()=>run('remove');
    el.querySelector('[data-a=find]').onclick=()=>run('find');
    el.querySelector('[data-a=reset]').onclick=()=>{root=null;el.querySelector('[data-v]').value=12;[8,3,10,1,6,14,4,7,13].forEach(k=>{const f=[];root=insert(root,k,f);});const aux=avlMode?n=>`h=${n.height} · b=${height(n.left)-height(n.right)}`:null;animate(el,[frame(root,'Исходный пример восстановлен. Введи ключ и выбери операцию.')],(stage,f)=>{stage.classList.add('viz-stage-stack');drawBinary(stage,f.root,f.active,kind,aux);});};
    el.querySelector('[data-a=reset]').click();
  }

  function heap(el) {
    el.innerHTML=`<div class="viz-h"><b>▶ Двоичная куча</b><span class="muted" style="font-size:13px">просеивание по шагам</span></div><div class="viz-ctl"><input data-v type="number" value="9" aria-label="значение"><button class="p" data-a="add">добавить</button><button data-a="pop">извлечь корень</button><button data-a="build">heapify</button><button data-a="mode">max-heap</button><button data-a="reset">сбросить</button></div><div class="viz-stage"></div><div class="viz-log" aria-live="polite"></div>`;
    let a=[10,7,8,3,5,2], isMin=false;
    const better=(x,y)=>isMin?x<y:x>y;
    function start(note){return [{array:a.slice(),note,active:[]}];}
    function show(frames){animate(el,frames,(stage,f)=>{stage.classList.add('viz-stage-stack');drawHeap(stage,f.array,f.active,isMin);});}
    function siftUp(i,frames){while(i>0){const p=(i-1)>>1;frames.push({array:a.slice(),note:`Сравниваем ${a[i]} с родителем ${a[p]}.`,active:[i,p]});if(!better(a[i],a[p])){frames[frames.length-1].note+=` Порядок ${isMin?'min':'max'}-heap соблюдён: обмен не нужен.`;break;}[a[i],a[p]]=[a[p],a[i]];frames.push({array:a.slice(),note:`Нарушен порядок: меняем индексы ${i} и ${p}.`,active:[i,p]});i=p;}}
    function siftDown(i,frames){while(2*i+1<a.length){let c=2*i+1;if(c+1<a.length){frames.push({array:a.slice(),note:`Сравниваем детей ${a[c]} и ${a[c+1]}, чтобы выбрать ${isMin?'меньшего':'большего'}.`,active:[c,c+1]});if(better(a[c+1],a[c]))c++;}frames.push({array:a.slice(),note:`Сравниваем родителя ${a[i]} с лучшим ребёнком ${a[c]}.`,active:[i,c]});if(!better(a[c],a[i]))break;[a[i],a[c]]=[a[c],a[i]];frames.push({array:a.slice(),note:`Просеиваем ${a[i]} вниз, меняя индексы ${i} и ${c}.`,active:[i,c]});i=c;}}
    function build(){const frames=start('Начинаем heapify с последнего внутреннего узла.');for(let i=Math.floor(a.length/2)-1;i>=0;i--){frames.push({array:a.slice(),note:`Просеиваем вниз поддерево с корнем в индексе ${i}.`,active:[i]});siftDown(i,frames);}frames.push({array:a.slice(),note:'Heapify завершён: свойство кучи выполняется во всех поддеревьях.'});show(frames);}
    el.querySelector('[data-a=add]').onclick=()=>{const frames=start('Добавляем новый элемент в конец массива.');a.push(Number(el.querySelector('[data-v]').value));frames.push({array:a.slice(),note:`Элемент ${a[a.length-1]} добавлен в индекс ${a.length-1}.`,active:[a.length-1]});siftUp(a.length-1,frames);frames.steps=frames.length-1;show(frames);};
    el.querySelector('[data-a=pop]').onclick=()=>{const frames=start(a.length?'Корень содержит экстремальный элемент кучи.':'Куча пуста.');if(a.length){const result=a[0];if(a.length===1)a.pop();else{a[0]=a.pop();frames.push({array:a.slice(),note:`Удаляем ${result}; последний элемент переносим в корень.`,active:[0]});siftDown(0,frames);}frames.push({array:a.slice(),note:`Извлечено значение ${result}.`});}show(frames);};
    el.querySelector('[data-a=build]').onclick=()=>build();
    el.querySelector('[data-a=mode]').onclick=e=>{isMin=!isMin;e.currentTarget.textContent=isMin?'min-heap':'max-heap';build();};
    el.querySelector('[data-a=reset]').onclick=()=>{a=[10,7,8,3,5,2];isMin=false;el.querySelector('[data-a=mode]').textContent='max-heap';el.querySelector('[data-v]').value=9;show([{array:a.slice(),active:[],note:'Исходная max-heap восстановлена.'}]);};
    build();
  }

  function btree(el) {
    el.innerHTML=`<div class="viz-h"><b>▶ B-дерево степени 2</b><span class="muted" style="font-size:13px">поиск ключа и разделение полных узлов</span></div><div class="viz-ctl"><input data-v type="number" value="18" aria-label="ключ"><button class="p" data-a="add">вставить ключ</button><button data-a="find">найти ключ</button><button data-a="reset">сбросить</button></div><div class="viz-stage"></div><div class="viz-log" aria-live="polite"></div>`;
    const make=()=>({id:id(),keys:[],children:[]});let root=make();
    const clone=n=>n?({id:n.id,keys:n.keys.slice(),children:n.children.map(clone)}):null;
    function snap(frames,note,active=[]){frames.push({root:clone(root),note,active});}
    function split(parent,i,frames){const y=parent.children[i],z=make(),mid=y.keys[1];z.keys=y.keys.slice(2);y.keys=y.keys.slice(0,1);if(y.children.length){z.children=y.children.slice(2);y.children=y.children.slice(0,2);}parent.keys.splice(i,0,mid);parent.children.splice(i+1,0,z);snap(frames,`Узел заполнен: поднимаем средний ключ ${mid} к родителю.`,[parent.id,y.id,z.id]);}
    function insertNonFull(n,k,frames){let i=n.keys.length-1;if(!n.children.length){while(i>=0&&k<n.keys[i])i--;n.keys.splice(i+1,0,k);snap(frames,`Вставляем ${k} в лист и сохраняем порядок ключей.`,[n.id]);return;}
      while(i>=0&&k<n.keys[i])i--;i++;snap(frames,`Ищем диапазон для ${k}: переходим в ребёнка ${i}.`,[n.id]);
      if(n.children[i].keys.length===3){split(n,i,frames);if(k>n.keys[i])i++;}
      insertNonFull(n.children[i],k,frames);
    }
    function add(k){const frames=[{root:clone(root),note:`Начинаем вставку ${k}.`,active:[]}];if(find(root,k)){snap(frames,`Ключ ${k} уже есть: дубликат не добавляем.`);return frames;}
      if(root.keys.length===3){const old=root;root=make();root.children=[old];snap(frames,'Корень заполнен: создаём новый корень и разделяем старый.',[root.id,old.id]);split(root,0,frames);}
      insertNonFull(root,k,frames);snap(frames,`Вставка ${k} завершена. Все листья остались на одном уровне.`);return frames;
    }
    function find(n,k){let i=0;while(i<n.keys.length&&k>n.keys[i])i++;if(n.keys[i]===k)return true;return n.children.length?find(n.children[i],k):false;}
    function searchFrames(k){const frames=[{root:clone(root),note:`Ищем ${k}, двигаясь по диапазонам ключей.`,active:[]}];let n=root;while(n){let i=0;while(i<n.keys.length){snap(frames,`Сравниваем ${k} с разделителем ${n.keys[i]}.`,[n.id]);if(k===n.keys[i]){snap(frames,`Ключ ${k} найден в этом узле.`,[n.id]);return frames;}if(k<n.keys[i])break;i++;}if(!n.children.length){snap(frames,`Дошли до листа: ключа ${k} нет.`,[n.id]);return frames;}snap(frames,`Выбираем диапазон ${i+1}: переходим в ребёнка ${i}.`,[n.id]);n=n.children[i];}return frames;}
    function draw(stage,tree,active){const nodes=[];let leaf=0,maxDepth=0;
      function measure(n,d){maxDepth=Math.max(maxDepth,d);if(!n.children.length){n._start=leaf;n._span=1;leaf++;nodes.push({n,d});return;}const start=leaf;n.children.forEach(c=>measure(c,d+1));n._start=start;n._span=Math.max(1,leaf-start);nodes.push({n,d});}
      if(tree){measure(tree,0);if(!nodes.some(x=>x.n===tree))nodes.push({n:tree,d:0});}
      const slot=50,nodePad=18,w=Math.max(520,leaf*190+60),h=Math.max(190,(maxDepth+1)*112+24),pos=new Map();
      nodes.forEach(({n,d})=>pos.set(n,{x:40+(n._start+n._span/2)*((w-80)/Math.max(1,leaf)),y:42+d*104}));
      const lines=[];nodes.forEach(({n})=>n.children.forEach(c=>{const a=pos.get(n),b=pos.get(c);if(a&&b)lines.push(`<line x1="${a.x}" y1="${a.y+25}" x2="${b.x}" y2="${b.y-18}" stroke="var(--line-2)" stroke-width="2"/>`);}));
      const boxes=nodes.map(({n})=>{const p=pos.get(n),activeNode=active.includes(n.id),bw=Math.max(62,n.keys.length*slot+nodePad),left=p.x-bw/2;return `<g><rect x="${left}" y="${p.y-22}" width="${bw}" height="44" rx="9" fill="${activeNode?'var(--hl)':'var(--card)'}" stroke="${activeNode?'var(--accent)':'var(--line-2)'}" stroke-width="2"/>${n.keys.slice(1).map((_,i)=>`<line x1="${left+nodePad/2+(i+1)*slot}" y1="${p.y-20}" x2="${left+nodePad/2+(i+1)*slot}" y2="${p.y+20}" stroke="${activeNode?'#829c22':'var(--line-2)'}" stroke-width="1.5"/>`).join('')}${n.keys.map((k,i)=>`<text x="${left+nodePad/2+(i+.5)*slot}" y="${p.y+6}" text-anchor="middle" fill="${activeNode?'#11140a':'var(--ink)'}" font-size="16" font-weight="700">${k}</text>`).join('')}</g>`;}).join('');
      stage.innerHTML=`<svg viewBox="0 0 ${w} ${h}" style="width:100%;max-height:470px">${lines.join('')}${boxes}</svg><p class="muted" style="font-size:13px">Узел хранит отсортированные ключи; между соседними ключами лежит отдельный диапазон дочернего поддерева.</p>`;
    }
    function show(frames){animate(el,frames,(stage,f)=>{stage.classList.add('viz-stage-stack');draw(stage,f.root,f.active);});}
    el.querySelector('[data-a=add]').onclick=()=>show(add(Number(el.querySelector('[data-v]').value)));
    function seedFrames(){root=make();const frames=[{root:clone(root),note:'Пустое B-дерево. Воспроизведи построение: полные узлы будут разделяться.'}];[10,20,5,6,12,30,7,17].forEach(k=>frames.push(...add(k).slice(1)));return frames;}
    el.querySelector('[data-a=find]').onclick=()=>show(searchFrames(Number(el.querySelector('[data-v]').value)));
    el.querySelector('[data-a=reset]').onclick=()=>{el.querySelector('[data-v]').value=18;const sample=seedFrames();show([sample[sample.length-1]]);};
    const sample=seedFrames();show([sample[sample.length-1]]);
  }

  function trie(el) {
    el.innerHTML=`<div class="viz-h"><b>▶ Префиксное дерево Trie</b><span class="muted" style="font-size:13px">путь по символам и обрезка ветки</span></div><div class="viz-ctl"><input data-v value="care" aria-label="слово"><button class="p" data-a="add">добавить</button><button data-a="search">найти</button><button data-a="del">удалить</button><button data-a="reset">сбросить</button></div><div class="viz-stage"></div><div class="viz-log" aria-live="polite"></div>`;
    const make=()=>({id:id(),ch:'root',end:false,children:new Map()});const root=make();
    const clone=n=>({id:n.id,ch:n.ch,end:n.end,children:new Map([...n.children].map(([c,k])=>[c,clone(k)]))});
    function snap(frames,note,active=[]){frames.push({root:clone(root),note,active});}
    function add(word){const frames=[{root:clone(root),note:`Начинаем вставку слова «${word}».`,active:[]}];let n=root;for(const c of word){if(!n.children.has(c)){const next=make();next.ch=c;n.children.set(c,next);snap(frames,`Вершины для «${c}» не было: создаём её.`,[n.id,next.id]);}else{const next=n.children.get(c);snap(frames,`Переходим по ребру «${c}»: общий префикс сохраняется.`,[n.id,next.id]);}n=n.children.get(c);}n.end=true;snap(frames,`Помечаем конец слова «${word}».`,[n.id]);return frames;}
    function follow(word,frames){let n=root;for(const c of word){const next=n.children.get(c);snap(frames,next?`Ищем ребро «${c}» и переходим по нему.`:`Ребра «${c}» нет: дальнейшего пути не существует.`,next?[n.id,next.id]:[n.id]);if(!next)return null;n=next;}return n;}
    function remove(word){const frames=[{root:clone(root),note:`Начинаем удаление «${word}».`,active:[]}],path=[];let n=root;for(const c of word){const next=n.children.get(c);if(!next){snap(frames,`Символа «${c}» нет: слово не найдено.`,[n.id]);return frames;}path.push([n,c,next]);snap(frames,`Проходим символ «${c}».`,[n.id,next.id]);n=next;}if(!n.end){snap(frames,`Путь есть, но это не конец слова «${word}».` ,[n.id]);return frames;}n.end=false;snap(frames,`Снимаем отметку конца слова. Проверяем, можно ли удалить узлы пути.`,[n.id]);for(let i=path.length-1;i>=0;i--){const [parent,c,child]=path[i];if(!child.end&&!child.children.size){parent.children.delete(c);snap(frames,`Удаляем лишнюю вершину «${c}»: у неё больше нет потомков.`,[parent.id]);}else{snap(frames,`Оставляем «${c}»: она нужна другому слову или префиксу.`,[child.id]);break;}}return frames;}
    function draw(stage,tree,active){const positions=new Map(),nodes=[];let leaf=0,maxDepth=0;
      function measure(n,d){maxDepth=Math.max(maxDepth,d);const kids=[...n.children.values()].sort((a,b)=>a.ch.localeCompare(b.ch));if(!kids.length){positions.set(n,{x:leaf++,y:d});nodes.push(n);return;}kids.forEach(k=>measure(k,d+1));const xs=kids.map(k=>positions.get(k).x);positions.set(n,{x:(Math.min(...xs)+Math.max(...xs))/2,y:d});nodes.push(n);}
      measure(tree,0);const w=Math.max(440,leaf*74+70),h=Math.max(170,(maxDepth+1)*78+30),xStep=(w-70)/Math.max(1,leaf-1);
      const p=n=>({x:35+positions.get(n).x*xStep,y:34+positions.get(n).y*72});const lines=[];nodes.forEach(n=>n.children.forEach(ch=>{const a=p(n),b=p(ch);lines.push(`<line x1="${a.x}" y1="${a.y+18}" x2="${b.x}" y2="${b.y-18}" stroke="var(--line-2)" stroke-width="2"/><text x="${(a.x+b.x)/2}" y="${(a.y+b.y)/2}" fill="var(--ink-2)" stroke="var(--bg)" stroke-width="4" paint-order="stroke" font-size="13" font-weight="700" text-anchor="middle">${esc(ch.ch)}</text>`);}));
      const circles=nodes.map(n=>{const q=p(n),hot=active.includes(n.id),label=n.ch==='root'?'root':n.ch;return `<g><circle cx="${q.x}" cy="${q.y}" r="22" fill="${hot?'var(--hl)':n.end?'var(--hl)':'var(--card)'}" stroke="${hot?'var(--accent)':'var(--line-2)'}" stroke-width="2"/><text x="${q.x}" y="${q.y+5}" text-anchor="middle" fill="${hot||n.end?'#11140a':'var(--ink)'}" font-size="14" font-weight="700">${esc(label)}</text>${n.end?`<text x="${q.x}" y="${q.y-27}" text-anchor="middle" fill="var(--ink-2)" stroke="var(--bg)" stroke-width="3" paint-order="stroke" font-size="12" font-weight="700">конец</text>`:''}</g>`;}).join('');
      stage.innerHTML=`<svg viewBox="0 0 ${w} ${h}" style="width:100%;max-height:420px">${lines.join('')}${circles}</svg><p class="muted" style="font-size:12px">Заполненная вершина отмечает целое слово; другие ветви могут продолжаться.</p>`;
    }
    function show(frames){animate(el,frames,(stage,f)=>{stage.classList.add('viz-stage-stack');draw(stage,f.root,f.active);});}
    el.querySelector('[data-a=add]').onclick=()=>show(add(el.querySelector('[data-v]').value));
    el.querySelector('[data-a=del]').onclick=()=>show(remove(el.querySelector('[data-v]').value));
    el.querySelector('[data-a=search]').onclick=()=>{const word=el.querySelector('[data-v]').value,frames=[{root:clone(root),note:`Ищем слово «${word}».`,active:[]}],n=follow(word,frames);snap(frames,n&&n.end?`Слово «${word}» найдено.`:n?`Путь есть, но «${word}» не отмечено как слово.`:`Слово «${word}» отсутствует.` ,n?[n.id]:[]);show(frames);};
    el.querySelector('[data-a=reset]').onclick=()=>{root.children.clear();root.end=false;el.querySelector('[data-v]').value='care';['car','cart','cat','dog'].forEach(w=>add(w));show([{root:clone(root),active:[],note:'Исходный пример восстановлен: car, cart, cat и dog делят общий префикс.'}]);};
    el.querySelector('[data-a=reset]').click();
  }

  function heapsort(el) {
    el.innerHTML=`<div class="viz-h"><b>▶ Heapsort</b><span class="muted" style="font-size:13px">построение max-heap и сортировка на месте</span></div><div class="viz-ctl"><input data-v value="8, 3, 5, 1, 9, 2, 7" aria-label="массив чисел"><button class="p" data-a="sort">сортировать</button><button data-a="reset">сбросить</button></div><div class="viz-stage"></div><div class="viz-log" aria-live="polite"></div>`;
    const input=()=>el.querySelector('[data-v]').value.split(/[ ,;]+/).filter(Boolean).map(Number).filter(Number.isFinite);
    function run(values){const a=values.slice(),frames=[];const save=(end,note,active=[])=>frames.push({array:a.slice(),end,note,active});
      if(!a.length){save(0,'Массив пуст: сортировать нечего.');return frames;}
      save(a.length,`Исходный массив: [${a.join(', ')}]. Строим max-heap снизу вверх.`);
      function down(i,end){while(2*i+1<end){let c=2*i+1;if(c+1<end){save(end,`Сравниваем детей ${a[c]} и ${a[c+1]}; выбираем больший.`,[c,c+1]);if(a[c+1]>a[c])c++;}save(end,`Сравниваем родителя ${a[i]} с ребёнком ${a[c]}.`,[i,c]);if(a[i]>=a[c])break;[a[i],a[c]]=[a[c],a[i]];save(end,`Меняем их местами, чтобы восстановить свойство кучи.`,[i,c]);i=c;}}
      for(let i=Math.floor(a.length/2)-1;i>=0;i--){save(a.length,`Просеиваем вниз узел с индексом ${i}.`,[i]);down(i,a.length);}
      save(a.length,'Max-heap готова: на вершине находится максимум.');
      for(let end=a.length-1;end>0;end--){[a[0],a[end]]=[a[end],a[0]];save(end,`Переносим максимум ${a[end]} в конец массива; эта часть уже отсортирована.`,[0,end]);down(0,end);}
      save(0,`Готово: [${a.join(', ')}]. Сортировка выполнена на месте.`);return frames;
    }
    function show(frames){animate(el,frames,(stage,f)=>{stage.classList.add('viz-stage-stack');drawHeap(stage,f.array.slice(0,f.end),f.active.filter(i=>i<f.end),false);stage.insertAdjacentHTML('beforeend',`<div style="display:flex;gap:7px;flex-wrap:wrap;margin:12px 0">${f.array.map((v,i)=>`<span style="padding:7px 10px;border-radius:7px;background:${i>=f.end?'var(--hl)':f.active.includes(i)?'var(--hl)':'var(--bg-2)'};color:${i>=f.end||f.active.includes(i)?'#11140a':'var(--ink)'};font:600 14px var(--f-mono)">${v}<small style="color:${i>=f.end||f.active.includes(i)?'#36420f':'var(--ink-2)'}">[${i}]</small></span>`).join('')}</div><p class="muted" style="font-size:13px">Слева — куча в неотсортированной части; зелёные ячейки — готовый суффикс.</p>`);});}
    el.querySelector('[data-a=sort]').onclick=()=>show(run(input()));
    el.querySelector('[data-a=reset]').onclick=()=>{const sample=[8,3,5,1,9,2,7];el.querySelector('[data-v]').value=sample.join(', ');show(run(sample));};
    show(run(input()));
  }

  function traversal(el) {
    el.innerHTML=`<div class="viz-h"><b>▶ DFS и BFS</b><span class="muted" style="font-size:13px">по одному посещению на кадр</span></div><div class="viz-ctl"><button class="p" data-a="dfs">DFS preorder</button><button data-a="bfs">BFS по уровням</button><button data-a="reset">сбросить</button></div><div class="viz-stage"></div><div class="viz-log" aria-live="polite"></div>`;
    const root={id:id(),val:8,left:{id:id(),val:3,left:{id:id(),val:1},right:{id:id(),val:6,left:{id:id(),val:4},right:{id:id(),val:7}}},right:{id:id(),val:10,right:{id:id(),val:14,left:{id:id(),val:13}}}};
    function run(kind){const order=[];if(kind==='dfs'){function walk(n){if(!n)return;order.push(n);walk(n.left);walk(n.right);}walk(root);}else{const q=[root];while(q.length){const n=q.shift();order.push(n);if(n.left)q.push(n.left);if(n.right)q.push(n.right);}}
      const frames=[frame(root,`${kind==='dfs'?'DFS preorder':'BFS'}: начинаем от корня.`)];const seen=[];order.forEach((n,i)=>{seen.push(n.key??n.val);frames.push({...frame(root,`${kind==='dfs'?'DFS идёт в глубину':'BFS обрабатывает очередь'}: посещаем ${n.val} (${i+1} из ${order.length}).`,[n.id]),seen:seen.slice()});});frames.push({...frame(root,`Обход завершён: ${seen.join(' → ')}.`),seen});animate(el,frames,(stage,f)=>{stage.classList.add('viz-stage-stack');drawBinary(stage,f.root,f.active,'Одно и то же дерево для двух обходов');if(f.seen)stage.insertAdjacentHTML('beforeend',`<div class="muted" style="font-size:13px;margin-top:8px">Уже посещены: ${f.seen.join(' → ')}</div>`);});}
    el.querySelector('[data-a=dfs]').onclick=()=>run('dfs');el.querySelector('[data-a=bfs]').onclick=()=>run('bfs');el.querySelector('[data-a=reset]').onclick=()=>animate(el,[frame(root,'Исходный пример дерева восстановлен.')],(stage,f)=>{stage.classList.add('viz-stage-stack');drawBinary(stage,f.root,f.active,'Одно и то же дерево для двух обходов');});
    run('dfs');
  }

  const base=window.VIZ.mount;
  window.VIZ.mount=function(el,type){
    if(type==='tree')bst(el,false);
    else if(type==='avl')bst(el,true);
    else if(type==='heap')heap(el);
    else if(type==='heapsort')heapsort(el);
    else if(type==='btree')btree(el);
    else if(type==='trie')trie(el);
    else if(type==='traversal')traversal(el);
    else base(el,type);
  };
})();
