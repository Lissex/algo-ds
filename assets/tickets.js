// Методы (практическая часть билетов), билеты раздела 2 и задачи LeetCode.

window.METHODS = {
  "ll-remove": {
    title: "remove для связанного списка",
    topic: "linked-list",
    snip: "structures/linked_list.py::Linked_list.remove",
    complexity: "O(n) — в худшем случае проходим весь список",
    steps: [
      "Список пустой → значения точно нет, бросаем <code>ValueError</code>.",
      "Значение в голове → просто сдвигаем <code>head = head.next</code>. Это отдельный случай, потому что у головы нет предыдущего узла.",
      "Иначе идём указателем <code>cur</code>, пока <b>следующий</b> узел не окажется искомым. Останавливаемся на узле <i>перед</i> удаляемым — именно его ссылку будем менять.",
      "Дошли до конца и не нашли → <code>ValueError</code>.",
      "«Перепрыгиваем» узел: <code>cur.next = cur.next.next</code>. Удалённый узел больше ни на что не ссылается — его уберёт сборщик мусора.",
      "Не забываем <code>size -= 1</code>."
    ],
    edges: ["пустой список", "удаляем голову", "удаляем последний узел", "значения нет", "несколько одинаковых значений — удаляется первое"]
  },
  "ll-append": {
    title: "append для связанного списка",
    topic: "linked-list",
    snip: "structures/linked_list.py::Linked_list.append",
    complexity: "O(n) — нужно дойти до последнего узла. С указателем tail было бы O(1).",
    steps: [
      "Создаём новый узел <code>Node(val)</code>; его <code>next</code> уже <code>None</code> — он станет последним.",
      "Список пустой → новый узел становится головой.",
      "Иначе идём от головы, пока у узла есть <code>next</code>: <code>while cur.next</code>. Останавливаемся на последнем узле.",
      "Цепляем новый узел: <code>cur.next = new_node</code>.",
      "<code>size += 1</code>."
    ],
    edges: ["пустой список", "список из одного элемента"]
  },
  "ll-reverse": {
    title: "reverse для связанного списка",
    topic: "linked-list",
    snip: "structures/linked_list.py::Linked_list.reverse",
    complexity: "O(n) по времени, O(1) по памяти — новых узлов не создаём",
    steps: [
      "Заводим <code>prev = None</code> (у будущего последнего узла <code>next</code> будет None) и <code>cur = head</code>.",
      "Пока <code>cur</code> не кончился: запоминаем <code>nxt = cur.next</code> — иначе после разворота стрелки потеряем остаток списка.",
      "Разворачиваем стрелку: <code>cur.next = prev</code>.",
      "Сдвигаем оба указателя на шаг вперёд: <code>prev = cur</code>, <code>cur = nxt</code>.",
      "Когда <code>cur</code> стал <code>None</code>, <code>prev</code> указывает на бывший последний узел — это новая голова: <code>head = prev</code>."
    ],
    edges: ["пустой список", "один элемент"],
    note: "Тот же приём используется в задаче LeetCode 234 (палиндром) и пригодится в задаче 206 Reverse Linked List."
  },
  "ll-insert": {
    title: "insert для связанного списка",
    topic: "linked-list",
    snip: "structures/linked_list.py::Linked_list.insert",
    complexity: "O(n) на поиск позиции; вставка в начало — O(1)",
    steps: [
      "Проверяем индекс: допустимо <code>0 ≤ idx ≤ size</code> (<code>idx == size</code> — вставка в конец).",
      "<code>idx == 0</code> → новый узел ставим перед головой: <code>new.next = head</code>, <code>head = new</code>.",
      "Иначе находим узел <b>перед</b> позицией: <code>prev = _get_item(idx - 1)</code>.",
      "Сначала цепляем хвост: <code>new.next = prev.next</code>, и только потом <code>prev.next = new</code>. В обратном порядке хвост потеряется.",
      "<code>size += 1</code>."
    ],
    edges: ["idx = 0", "idx = size (в конец)", "idx вне диапазона", "пустой список"]
  },
  "ll-setitem": {
    title: "__setitem__ для связанного списка",
    topic: "linked-list",
    snip: "structures/linked_list.py::Linked_list.__setitem__",
    extra: ["structures/linked_list.py::Linked_list._get_item"],
    complexity: "O(n) — поиск узла по индексу",
    steps: [
      "<code>lst[idx] = value</code> в Python вызывает <code>lst.__setitem__(idx, value)</code>.",
      "Находим узел по индексу вспомогательным методом <code>_get_item</code>: проверяем границы и делаем <code>idx</code> шагов от головы.",
      "Меняем только значение: <code>node.val = value</code>. Ссылки не трогаем — структура списка не меняется."
    ],
    edges: ["индекс вне диапазона → IndexError", "idx = 0 и idx = size - 1"]
  },
  "dll-pop": {
    title: "pop для двусвязного списка",
    topic: "doubly-linked-list",
    snip: "structures/double_linked_list.py::Double_Linked_List.pop",
    extra: ["structures/double_linked_list.py::Double_Linked_List._get_node"],
    complexity: "O(1) для краёв (pop() по умолчанию берёт последний), O(n) для середины",
    steps: [
      "Пустой список → <code>IndexError</code>.",
      "Находим узел по индексу (по умолчанию <code>-1</code>, то есть хвост). <code>_get_node</code> поддерживает отрицательные индексы и идёт с ближнего конца.",
      "Запоминаем соседей: <code>prev_node = node.prev</code>, <code>next_node = node.next</code>.",
      "Если <code>prev_node</code> есть — <code>prev_node.next = next_node</code>, иначе мы удаляем голову: <code>head = next_node</code>.",
      "Если <code>next_node</code> есть — <code>next_node.prev = prev_node</code>, иначе удаляем хвост: <code>tail = prev_node</code>.",
      "<code>size -= 1</code>, возвращаем <code>node.val</code>."
    ],
    edges: ["пустой список", "единственный элемент — head и tail становятся None", "удаление головы", "удаление хвоста", "отрицательный индекс"]
  },
  "dll-getitem": {
    title: "__getitem__ для двусвязного списка",
    topic: "doubly-linked-list",
    snip: "structures/double_linked_list.py::Double_Linked_List.__getitem__",
    extra: ["structures/double_linked_list.py::Double_Linked_List._get_node"],
    complexity: "O(n), но не больше n/2 шагов",
    steps: [
      "<code>lst[idx]</code> вызывает <code>__getitem__</code>, а он — вспомогательный <code>_get_node</code>.",
      "Отрицательный индекс переводим в обычный: <code>idx += size</code> (так <code>lst[-1]</code> — последний).",
      "Проверяем границы: <code>0 ≤ idx &lt; size</code>, иначе <code>IndexError</code>.",
      "Если <code>idx &lt; size // 2</code> — идём от <code>head</code> вперёд по <code>next</code>, иначе от <code>tail</code> назад по <code>prev</code>. В этом главное преимущество двусвязного списка.",
      "Возвращаем <code>node.val</code>."
    ],
    edges: ["отрицательный индекс", "индекс вне диапазона", "первый и последний элемент"],
    note: "У преподавателя метод называется <code>__get_item</code> (с двумя подчёркиваниями — Python «искажает» такое имя внутри класса). Логика та же."
  },
  "dll-setitem": {
    title: "__setitem__ для двусвязного списка",
    topic: "doubly-linked-list",
    snip: "structures/double_linked_list.py::Double_Linked_List.__setitem__",
    extra: ["structures/double_linked_list.py::Double_Linked_List._get_node"],
    complexity: "O(n), но не больше n/2 шагов",
    steps: [
      "<code>lst[idx] = value</code> вызывает <code>__setitem__(idx, value)</code>.",
      "Находим узел через <code>_get_node</code>: отрицательные индексы, проверка границ, обход с ближнего конца.",
      "Меняем только значение: <code>node.val = value</code>. Ссылки <code>prev</code>/<code>next</code> не трогаем."
    ],
    edges: ["отрицательный индекс", "индекс вне диапазона"]
  },
  "deque-popleft": {
    title: "popleft для deque",
    topic: "deque",
    snip: "structures/deque_ring.py::Deque.popleft",
    alt: "structures/deque_dll.py::LinkedDeque.popleft",
    complexity: "O(1)",
    steps: [
      "Пустой дек → <code>IndexError</code>.",
      "Левый (первый) элемент всегда лежит в ячейке <code>head</code> — берём его значение.",
      "Очищаем ячейку (<code>None</code>), чтобы не держать ссылку на объект.",
      "Сдвигаем начало вправо по кольцу: <code>head = (head + 1) % capacity</code>. Если head был в последней ячейке — он «завернёт» на 0.",
      "<code>size -= 1</code>, возвращаем значение."
    ],
    edges: ["пустой дек", "head в последней ячейке массива (заворот)", "один элемент"]
  },
  "deque-popright": {
    title: "popright (pop) для deque",
    topic: "deque",
    snip: "structures/deque_ring.py::Deque.pop",
    alt: "structures/deque_dll.py::LinkedDeque.pop",
    complexity: "O(1)",
    steps: [
      "В коде преподавателя и в <code>collections.deque</code> этот метод называется <code>pop</code>; <code>popright</code> — то же самое.",
      "Пустой дек → <code>IndexError</code>.",
      "Индекс правого (последнего) элемента: <code>(head + size - 1) % capacity</code>.",
      "Забираем значение, очищаем ячейку.",
      "<code>head</code> не меняется — уменьшаем только <code>size -= 1</code>."
    ],
    edges: ["пустой дек", "элементы «завернули» через конец массива"]
  },
  "deque-append": {
    title: "append для deque",
    topic: "deque",
    snip: "structures/deque_ring.py::Deque.append",
    extra: ["structures/deque_ring.py::Deque._resize"],
    alt: "structures/deque_dll.py::LinkedDeque.append",
    complexity: "O(1) амортизированно (resize — O(n), но редко)",
    steps: [
      "Массив заполнен (<code>size == capacity</code>) → <code>_resize()</code>: новый массив вдвое больше, элементы копируются по порядку начиная с head, <code>head = 0</code>.",
      "Первая свободная ячейка справа: <code>(head + size) % capacity</code>.",
      "Кладём туда значение, <code>size += 1</code>. <code>head</code> не меняется."
    ],
    edges: ["пустой дек", "полный дек → resize", "свободная ячейка «за краем» — заворот на начало"]
  },
  "deque-appendleft": {
    title: "appendleft для deque",
    topic: "deque",
    snip: "structures/deque_ring.py::Deque.appendleft",
    extra: ["structures/deque_ring.py::Deque._resize"],
    alt: "structures/deque_dll.py::LinkedDeque.appendleft",
    complexity: "O(1) амортизированно",
    steps: [
      "Массив заполнен → <code>_resize()</code>.",
      "Сдвигаем начало на шаг влево по кольцу: <code>head = (head - 1) % capacity</code>. Если head был 0, станет <code>capacity - 1</code> (в Python остаток от деления на положительное число всегда ≥ 0).",
      "Кладём значение в <code>deque[head]</code>, <code>size += 1</code>."
    ],
    edges: ["head = 0 → заворот в конец массива", "полный дек → resize"]
  },
  "hs-add": {
    title: "add для hashset",
    topic: "hashset",
    snip: "structures/hash_set.py::Hashset.add",
    extra: ["structures/hash_set.py::Hashset._resize"],
    complexity: "O(1) в среднем, O(n) в худшем",
    steps: [
      "Проверяем коэффициент заполнения: если <code>size / capacity ≥ 0.75</code> — <code>_resize()</code> (удвоить capacity и переложить все ключи).",
      "Считаем номер корзины: <code>idx = _hash(key)</code>.",
      "Корзина пустая → кладём туда новый узел, <code>size += 1</code>.",
      "Иначе идём по цепочке: если встретили такой же ключ — выходим (во множестве нет дубликатов). Запоминаем последний узел в <code>prev</code>.",
      "Ключа нет → коллизия: дописываем узел в конец цепочки <code>prev.next = Node(key)</code> и <b>обязательно</b> <code>size += 1</code> (у преподавателя этой строки нет — это ошибка)."
    ],
    edges: ["ключ уже есть", "коллизия", "пора делать resize"]
  },
  "hs-remove": {
    title: "remove для hashset",
    topic: "hashset",
    snip: "structures/hash_set.py::Hashset.remove",
    complexity: "O(1) в среднем, O(n) в худшем",
    steps: [
      "Считаем номер корзины <code>idx = _hash(key)</code>.",
      "Корзина пустая → <code>KeyError</code>.",
      "Ключ в первом узле цепочки → корзина начинается со следующего: <code>buckets[idx] = head.next</code>.",
      "Иначе идём <code>while head.next</code>: если <code>head.next.key == key</code> — вырезаем <code>head.next = head.next.next</code>.",
      "Не нашли → <code>KeyError</code>. При успешном удалении <code>size -= 1</code>."
    ],
    edges: ["пустая корзина", "ключ первый в цепочке", "ключ последний в цепочке", "ключа нет"],
    note: "У преподавателя цикл <code>while head:</code> — если ключа нет, на последнем узле <code>head.next.key</code> падает с <code>AttributeError</code>."
  }
};

window.TICKETS = [
  { n: 1,  theory: "stack",              method: "ll-remove",       lc: 1 },
  { n: 2,  theory: "queue",              method: "ll-append",       lc: 20 },
  { n: 3,  theory: "linked-list",        method: "dll-pop",         lc: 155 },
  { n: 4,  theory: "doubly-linked-list", method: "deque-popleft",   lc: 3 },
  { n: 5,  theory: "deque",              method: "hs-add",          lc: 13 },
  { n: 6,  theory: "ring-buffer",        method: "ll-reverse",      lc: 2 },
  { n: 7,  theory: "hashing",            method: "dll-getitem",     lc: 232 },
  { n: 8,  theory: "collision",          method: "ll-insert",       lc: 2 },
  { n: 9,  theory: "hashset",            method: "dll-setitem",     lc: 21 },
  { n: 10, theory: "hashtable",          method: "deque-popright",  lc: 2073 },
  { n: 11, theory: "deque",              method: "hs-remove",       lc: 83 },
  { n: 12, theory: "ring-buffer",        method: "ll-setitem",      lc: 141 },
  { n: 13, theory: "hashing",            method: "deque-append",    lc: 234 },
  { n: 14, theory: "linked-list",        method: "deque-appendleft",lc: 290 },
  { n: 15, theory: "hashtable",          method: "ll-reverse",      lc: 225 }
];

// Формулировки теоретических вопросов — как в билетах
window.THEORY_Q = {
  "stack": "Структура данных стек. Принцип LIFO. Методы peek, add, remove",
  "queue": "Структура данных очередь. Принцип FIFO. Методы peek, add, remove",
  "linked-list": "Связанные списки",
  "doubly-linked-list": "Двухсвязные списки",
  "deque": "Deque. Плюсы и минусы реализации через кольцевой массив и двухсвязные списки",
  "ring-buffer": "Кольцевой массив",
  "hashing": "Хэширование. Особенности хэширования для криптографии и для хэшсетов",
  "collision": "Коллизия",
  "hashset": "Hashset",
  "hashtable": "Hashtable"
};

window.PROBLEMS = [
  { n: 1, slug: "two-sum", title: "Two Sum", ru: "Сумма двух", diff: "Easy", tags: ["хэш-таблица"], file: "leetcode/0001_two_sum.py",
    task: "Дан массив <code>nums</code> и число <code>target</code>. Найти индексы двух <b>разных</b> элементов, сумма которых равна <code>target</code>. Ответ гарантированно существует и единственный.",
    example: "nums = [2, 7, 11, 15], target = 9  →  [0, 1]",
    idea: "Перебор всех пар — O(n²). Быстрее: идём по массиву и для каждого числа <code>x</code> проверяем, встречали ли мы раньше «пару» <code>target - x</code>. Встреченные числа храним в словаре <code>число → индекс</code>; проверка <code>in</code> в хэш-таблице — O(1). Число кладём в словарь <i>после</i> проверки, чтобы не взять один элемент дважды.",
    time: "O(n)", mem: "O(n)" },
  { n: 2, slug: "add-two-numbers", title: "Add Two Numbers", ru: "Сложить два числа", diff: "Medium", tags: ["связанный список"], file: "leetcode/0002_add_two_numbers.py",
    task: "Два неотрицательных числа записаны в связанных списках цифрами <b>в обратном порядке</b> (первый узел — единицы). Вернуть их сумму в таком же виде.",
    example: "2→4→3 (342) + 5→6→4 (465)  →  7→0→8 (807)",
    idea: "Складываем «в столбик», как в школе: идём по обоим спискам одновременно, складываем цифры и перенос <code>carry</code>. Новая цифра — <code>total % 10</code>, перенос — <code>total // 10</code> (<code>divmod</code> даёт оба сразу). Цикл продолжается, пока есть хотя бы один список <b>или перенос</b> — иначе потеряем старшую единицу (99 + 1). Фиктивная голова <code>dummy</code> избавляет от отдельной обработки первого узла.",
    time: "O(max(m, n))", mem: "O(max(m, n)) — под ответ" },
  { n: 3, slug: "longest-substring-without-repeating-characters", title: "Longest Substring Without Repeating Characters", ru: "Самая длинная подстрока без повторов", diff: "Medium", tags: ["хэш-таблица", "скользящее окно"], file: "leetcode/0003_longest_substring.py",
    task: "Найти длину самой длинной подстроки строки <code>s</code>, в которой все символы различны.",
    example: "\"abcabcbb\" → 3 (\"abc\"),  \"bbbbb\" → 1,  \"pwwkew\" → 3 (\"wke\")",
    idea: "Скользящее окно <code>[left, right]</code> без повторов. Двигаем <code>right</code> по строке; в словаре храним, где каждый символ встречался последний раз. Если текущий символ уже был <b>внутри окна</b> (<code>last[ch] ≥ left</code>), переносим <code>left</code> сразу за его прошлое вхождение. Проверка <code>≥ left</code> важна: старое вхождение левее окна не мешает (пример \"abba\").",
    time: "O(n)", mem: "O(k), k — размер алфавита" },
  { n: 13, slug: "roman-to-integer", title: "Roman to Integer", ru: "Римские цифры в число", diff: "Easy", tags: ["хэш-таблица", "строки"], file: "leetcode/0013_roman_to_integer.py",
    task: "Перевести римское число (от 1 до 3999) в обычное целое.",
    example: "\"III\" → 3,  \"LVIII\" → 58,  \"MCMXCIV\" → 1994",
    idea: "Значения символов храним в словаре. Обычно цифры идут от больших к меньшим и просто складываются. Исключение — когда меньшая цифра стоит <b>перед</b> большей (IV = 4, IX = 9, CM = 900): тогда её надо <b>вычесть</b>. Значит, для каждого символа смотрим на следующий: если следующий больше — вычитаем текущий, иначе прибавляем.",
    time: "O(n)", mem: "O(1)" },
  { n: 20, slug: "valid-parentheses", title: "Valid Parentheses", ru: "Правильные скобки", diff: "Easy", tags: ["стек"], file: "leetcode/0020_valid_parentheses.py",
    task: "Строка из символов <code>()[]{}</code>. Проверить, что скобки расставлены правильно: каждая открытая закрыта скобкой того же типа и в правильном порядке.",
    example: "\"()[]{}\" → true,  \"(]\" → false,  \"([)]\" → false,  \"{[]}\" → true",
    idea: "Классическое применение <b>стека</b>. Открывающую скобку кладём в стек. Закрывающая должна соответствовать <b>последней</b> открытой (LIFO!) — сверяем с вершиной стека и снимаем её. Если стек пуст или тип не совпал — строка неправильная. В конце стек должен быть пустым — иначе остались незакрытые скобки.",
    time: "O(n)", mem: "O(n)" },
  { n: 21, slug: "merge-two-sorted-lists", title: "Merge Two Sorted Lists", ru: "Слияние двух отсортированных списков", diff: "Easy", tags: ["связанный список"], file: "leetcode/0021_merge_two_sorted_lists.py",
    task: "Даны головы двух отсортированных связанных списков. Слить их в один отсортированный список (переиспользуя узлы) и вернуть его голову.",
    example: "1→2→4 + 1→3→4  →  1→1→2→3→4→4",
    idea: "Фиктивный узел <code>dummy</code> и указатель <code>tail</code> на конец результата. Пока оба списка не пусты, сравниваем головы и прицепляем меньший узел к <code>tail</code>, сдвигая этот список. Когда один список закончился, остаток другого уже отсортирован — цепляем его целиком: <code>tail.next = list1 or list2</code>. Ответ — <code>dummy.next</code>.",
    time: "O(m + n)", mem: "O(1)" },
  { n: 83, slug: "remove-duplicates-from-sorted-list", title: "Remove Duplicates from Sorted List", ru: "Удалить дубликаты из отсортированного списка", diff: "Easy", tags: ["связанный список"], file: "leetcode/0083_remove_duplicates_sorted_list.py",
    task: "Дан отсортированный связанный список. Удалить повторы так, чтобы каждое значение встречалось один раз.",
    example: "1→1→2→3→3  →  1→2→3",
    idea: "Так как список отсортирован, одинаковые значения стоят рядом. Идём указателем <code>cur</code>: если <code>cur.next</code> равен <code>cur</code> — выкидываем его (<code>cur.next = cur.next.next</code>) и <b>не двигаемся</b> (дубликатов может быть несколько подряд). Иначе переходим к следующему узлу. Это тот же приём «перепрыгивания», что в методе <code>remove</code>.",
    time: "O(n)", mem: "O(1)" },
  { n: 141, slug: "linked-list-cycle", title: "Linked List Cycle", ru: "Цикл в связанном списке", diff: "Easy", tags: ["связанный список", "два указателя"], file: "leetcode/0141_linked_list_cycle.py",
    task: "Определить, есть ли в связанном списке цикл (какой-то узел ссылается на один из предыдущих).",
    example: "3→2→0→-4→(назад на 2)  →  true",
    idea: "Простое решение — запоминать посещённые узлы в <code>set</code> (O(n) памяти). Лучше — <b>алгоритм Флойда «черепаха и заяц»</b>: медленный указатель шагает на 1, быстрый на 2. Если цикла нет, заяц дойдёт до <code>None</code>. Если цикл есть, внутри цикла заяц догоняет черепаху на 1 узел за шаг и обязательно её встретит. Сравниваем узлы через <code>is</code>, а не значения.",
    time: "O(n)", mem: "O(1)" },
  { n: 155, slug: "min-stack", title: "Min Stack", ru: "Стек с минимумом", diff: "Medium", tags: ["стек"], file: "leetcode/0155_min_stack.py",
    task: "Реализовать стек с операциями <code>push</code>, <code>pop</code>, <code>top</code> и <code>getMin</code> (текущий минимум), каждая за O(1).",
    example: "push(-2), push(0), push(-3), getMin() → -3, pop(), top() → 0, getMin() → -2",
    idea: "Пересчитывать минимум при каждом <code>getMin</code> — O(n). Хитрость: храним второй стек <code>mins</code>, где на каждой высоте лежит минимум всех элементов <b>до этой высоты</b>. При <code>push</code> кладём <code>min(val, mins[-1])</code>, при <code>pop</code> снимаем из обоих стеков. Тогда минимум всегда на вершине <code>mins</code>.",
    time: "O(1) все операции", mem: "O(n)" },
  { n: 225, slug: "implement-stack-using-queues", title: "Implement Stack using Queues", ru: "Стек на очередях", diff: "Easy", tags: ["стек", "очередь"], file: "leetcode/0225_stack_using_queues.py",
    task: "Реализовать стек (LIFO), используя только операции очереди: добавить в конец, забрать из начала, посмотреть начало, размер, пустота.",
    example: "push(1), push(2), top() → 2, pop() → 2, empty() → false",
    idea: "Хватает <b>одной</b> очереди. После добавления элемента в конец «прокручиваем» очередь: <code>size - 1</code> раз забираем элемент из начала и ставим в конец. Новый элемент оказывается в начале, и порядок очереди совпадает с порядком стека. <code>pop</code> и <code>top</code> — просто начало очереди. Из <code>deque</code> используем только <code>append</code> и <code>popleft</code>.",
    time: "push O(n), остальное O(1)", mem: "O(n)" },
  { n: 232, slug: "implement-queue-using-stacks", title: "Implement Queue using Stacks", ru: "Очередь на стеках", diff: "Easy", tags: ["стек", "очередь"], file: "leetcode/0232_queue_using_stacks.py",
    task: "Реализовать очередь (FIFO), используя только два стека: <code>push</code>, <code>pop</code>, <code>peek</code>, <code>empty</code>.",
    example: "push(1), push(2), peek() → 1, pop() → 1, empty() → false",
    idea: "Два стека: <code>inbox</code> для добавления и <code>outbox</code> для извлечения. Если переложить элементы из одного стека в другой, их порядок развернётся — самый старый окажется сверху. Перекладываем <b>только когда outbox пуст</b>, иначе нарушим порядок. Каждый элемент перекладывается ровно один раз, поэтому в среднем все операции O(1).",
    time: "O(1) амортизированно", mem: "O(n)" },
  { n: 234, slug: "palindrome-linked-list", title: "Palindrome Linked List", ru: "Список-палиндром", diff: "Easy", tags: ["связанный список", "два указателя"], file: "leetcode/0234_palindrome_linked_list.py",
    task: "Проверить, читается ли связанный список одинаково в обе стороны.",
    example: "1→2→2→1 → true,  1→2 → false",
    idea: "Простой путь — скопировать значения в массив и сравнить с развёрнутым (O(n) памяти). Без доп. памяти: 1) находим середину — <code>slow</code> шагает на 1, <code>fast</code> на 2; когда <code>fast</code> дошёл до конца, <code>slow</code> в середине; 2) <b>разворачиваем</b> вторую половину (ровно метод <code>reverse</code> из билетов); 3) сравниваем первую половину с развёрнутой второй.",
    time: "O(n)", mem: "O(1)" },
  { n: 290, slug: "word-pattern", title: "Word Pattern", ru: "Шаблон слов", diff: "Easy", tags: ["хэш-таблица"], file: "leetcode/0290_word_pattern.py",
    task: "Дан шаблон <code>pattern</code> (буквы) и строка <code>s</code> (слова через пробел). Проверить, что между буквами и словами есть взаимно-однозначное соответствие (биекция).",
    example: "\"abba\", \"dog cat cat dog\" → true;  \"abba\", \"dog dog dog dog\" → false",
    idea: "Длины должны совпадать. Заводим <b>два</b> словаря: буква → слово и слово → буква. Одного мало: в примере \"abba\" / \"dog dog dog dog\" словарь буква→слово не заметит, что <code>a</code> и <code>b</code> обе стали <code>dog</code>. Для каждой пары проверяем, что она не противоречит уже записанному в обоих словарях.",
    time: "O(n)", mem: "O(n)" },
  { n: 2073, slug: "time-needed-to-buy-tickets", title: "Time Needed to Buy Tickets", ru: "Время на покупку билетов", diff: "Easy", tags: ["очередь"], file: "leetcode/2073_time_needed_to_buy_tickets.py",
    task: "В очереди <code>n</code> человек, i-й хочет купить <code>tickets[i]</code> билетов. За 1 секунду первый в очереди покупает 1 билет и, если ему нужно ещё, встаёт в конец. Сколько секунд пройдёт, пока человек <code>k</code> купит все свои билеты?",
    example: "tickets = [2, 3, 2], k = 2  →  6",
    idea: "Можно честно смоделировать <b>очередь</b> (FIFO) через <code>deque</code> — это второй метод в решении. Но есть формула за один проход: пока человек k покупает свои <code>tickets[k]</code> билетов, каждый, кто стоит <b>до него (включительно)</b>, успеет купить не больше <code>tickets[k]</code> билетов, а каждый, кто стоит <b>после</b>, — не больше <code>tickets[k] - 1</code> (в последнем круге k уходит раньше них). Суммируем <code>min</code>.",
    time: "O(n)", mem: "O(1)" }
];
