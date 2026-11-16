class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        # Высота листа равна 0
        self.height = 0


class AVLTree:
    def __init__(self):
        self.root = None

    # ---------- Высота и баланс ----------

    def get_height(self, node):
        # Высота отсутствующего узла
        if node is None:
            return -1
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return (
            self.get_height(node.left)
            - self.get_height(node.right)
        )

    def update_height(self, node):
        node.height = 1 + max(
            self.get_height(node.left),
            self.get_height(node.right)
        )

    # ---------- Повороты ----------

    def rotate_right(self, A):
        B = A.left
        T = B.right

        B.right = A
        A.left = T

        # Сначала высота опустившейся вершины
        self.update_height(A)
        self.update_height(B)

        return B

    def rotate_left(self, A):
        B = A.right
        T = B.left

        B.left = A
        A.right = T

        self.update_height(A)
        self.update_height(B)

        return B

    # ---------- Балансировка ----------

    def rebalance(self, node):
        self.update_height(node)
        balance = self.get_balance(node)

        # Левое поддерево слишком высокое
        if balance > 1:
            # LR: сначала поворачиваем левого ребёнка
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)

            # LL или уже преобразованный LR
            return self.rotate_right(node)

        # Правое поддерево слишком высокое
        if balance < -1:
            # RL: сначала поворачиваем правого ребёнка
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)

            # RR или уже преобразованный RL
            return self.rotate_left(node)

        return node

    # ---------- Вставка ----------

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Дубликаты игнорируем
            return node

        return self.rebalance(node)

    # ---------- Поиск ----------

    def search(self, key):
        current = self.root

        while current is not None:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return None

    # ---------- Удаление ----------

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Нет левого ребёнка
            if node.left is None:
                return node.right

            # Нет правого ребёнка
            if node.right is None:
                return node.left

            # Два ребёнка:
            # заменяем ключ на минимальный ключ справа
            successor = self._min_node(node.right)
            node.key = successor.key
            node.right = self._delete(
                node.right,
                successor.key
            )

        # После удаления балансируем каждый предок
        return self.rebalance(node)

    def _min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # ---------- Обходы ----------

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.key)
        self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node is None:
            return
        result.append(node.key)
        self._preorder(node.left, result)
        self._preorder(node.right, result)