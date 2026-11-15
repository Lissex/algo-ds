"""Префиксное дерево с добавлением, поиском, префиксом и удалением."""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, text):
        node = self.root
        for char in text:
            node = node.children.get(char)
            if node is None:
                return None
        return node

    def delete(self, word):
        if not self.search(word):
            return False
        def prune(node, depth):
            if depth == len(word):
                node.is_end = False
            else:
                char = word[depth]
                if prune(node.children[char], depth + 1):
                    del node.children[char]
            return not node.is_end and not node.children
        prune(self.root, 0)
        return True
