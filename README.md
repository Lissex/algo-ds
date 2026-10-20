# АиСД · Алгоритмы и структуры данных

Сайт для подготовки к экзамену по алгоритмам и структурам данных. Два раздела (переключатель в шапке):

- **Раздел 1 — алгоритмы:** Big O, сортировки (выбором, вставками, пузырьком, слиянием, быстрая), рекурсия, merge, два указателя, скользящее окно, бинарный и линейный поиск, массив, min/max. 15 вопросов с ответами, пошаговые анимации, 18 задач LeetCode.
- **Раздел 2 — структуры данных:** стек, очередь, связанные списки, deque, кольцевой массив, хэширование. 15 билетов с ответами, интерактивные модели, 14 задач LeetCode.

В обоих разделах — тренажёр: пишешь код прямо в браузере, запускаешь и проверяешь скрытыми тестами.

Python в браузере работает через [Pyodide](https://pyodide.org) (загружается с CDN при первом запуске, ~10 МБ), редактор — [CodeMirror 5](https://codemirror.net/5/).

Код структур основан на репозитории преподавателя [Bunyod2002/Data-structures](https://github.com/Bunyod2002/Data-structures).

## Как выложить на GitHub Pages

1. Зайди на [github.com/new](https://github.com/new) и создай **публичный** репозиторий, например `algo-ds`. Галочку «Add a README» не ставь.
2. Открой терминал в этой папке и выполни (подставь свой ник):
   ```bash
   git init
   git add .
   git commit -m "Сайт по АиСД, раздел 2"
   git branch -M main
   git remote add origin https://github.com/ТВОЙ_НИК/algo-ds.git
   git push -u origin main
   ```
   Без терминала: на странице нового репозитория нажми **uploading an existing file** и перетащи туда всё содержимое папки (включая `assets`, `code`, `tests`, `tools`).
3. В репозитории: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main`, папка `/ (root)` → Save**.
4. Через 1–2 минуты сайт откроется по адресу `https://ТВОЙ_НИК.github.io/algo-ds/`.

## Как смотреть локально

```bash
python -m http.server 8000
```
Потом открой http://localhost:8000. Можно и просто открыть `index.html` двойным кликом — тренажёр тоже заработает (нужен интернет для загрузки Python), но сравнение с SHA-256 на странице «Хэширование» работает только через сервер или на GitHub Pages.

## Структура

```
index.html            — страница сайта
assets/style.css      — оформление (светлая и тёмная тема)
assets/app.js         — навигация, поиск, билеты, режим экзамена
assets/viz.js         — интерактивные модели структур
assets/topics.js      — теория раздела 2
assets/topics1.js     — теория и вопросы раздела 1
assets/tickets.js     — билеты, методы, задачи LeetCode раздела 2
assets/problems1.js   — задачи LeetCode и задания тренажёра раздела 1
assets/viz1.js        — анимации раздела 1 (сортировки, поиск, окно, рекурсия, Big O)
assets/trainer.js     — тренажёр: редактор, запуск Python, проверка
assets/code.js        — код из папки code/ (генерируется)
assets/exercises.js   — заготовки и тесты тренажёра (генерируется)
code/algorithms/      — алгоритмы раздела 1
code/structures/      — структуры данных (исправленный код преподавателя + Stack, Queue, LinkedDeque)
code/leetcode/        — решения задач
code/teacher/         — оригинальные файлы преподавателя
tests/test_all.py     — тесты кода раздела 2
tests/test_section1.py — тесты кода раздела 1
tests/test_exercises.py — проверка тренажёра (эталон проходит, заготовка нет)
tools/build.py        — пересобирает assets/code.js и assets/exercises.js
tools/exercises_spec.py  — тесты и заготовки тренажёра (раздел 2)
tools/exercises_spec1.py — тесты и заготовки тренажёра (раздел 1)
```

## Если меняешь код

После правки любого `.py` в папке `code/`:

```bash
python tests/test_all.py        # проверить код раздела 2
python tests/test_section1.py   # проверить код раздела 1
python tools/build.py           # обновить код, тренажёр и метки версий
python tests/test_exercises.py  # проверить тесты тренажёра
```

## Если поменял только сайт (html/css/js)

Запусти `python tools/build.py` перед загрузкой на GitHub — он обновит метки `?v=...` в `index.html`, и браузеры сразу подхватят новые файлы, а не старые из кэша.

