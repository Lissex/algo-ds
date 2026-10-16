# АиСД · Раздел 2

Сайт для подготовки к экзамену по алгоритмам и структурам данных: теория с интерактивными моделями, 15 билетов с ответами, решения 14 задач LeetCode на Python и тренажёр — пишешь код прямо в браузере, запускаешь и проверяешь тестами.

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
assets/topics.js      — теория по темам
assets/tickets.js     — билеты, методы, задачи LeetCode
assets/trainer.js     — тренажёр: редактор, запуск Python, проверка
assets/code.js        — код из папки code/ (генерируется)
assets/exercises.js   — заготовки и тесты тренажёра (генерируется)
code/structures/      — структуры данных (исправленный код преподавателя + Stack, Queue, LinkedDeque)
code/leetcode/        — решения задач
code/teacher/         — оригинальные файлы преподавателя
tests/test_all.py     — тесты всего кода
tests/test_exercises.py — проверка тренажёра (эталон проходит, заготовка нет)
tools/build.py        — пересобирает assets/code.js и assets/exercises.js
tools/exercises_spec.py — тесты и заготовки тренажёра
```

## Если меняешь код

После правки любого `.py` в папке `code/`:

```bash
python tests/test_all.py        # проверить, что всё работает
python tools/build.py           # обновить код и тренажёр на сайте
python tests/test_exercises.py  # проверить тесты тренажёра
```

## Добавить раздел 1

Темы добавляются в `assets/topics.js`, билеты и задачи — в `assets/tickets.js`, код — в `code/`.
