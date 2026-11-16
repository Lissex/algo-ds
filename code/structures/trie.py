class TrieNode:

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):  # добавляет слово
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):  # ищет слово
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def start_width(self, prefix):  # определяет есть ли слово с таким префиксом
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    def delete(self, word):
        if not self.search(word):
            return False

        def dfs_del(node, word, depth):
            if depth == len(word):
                node.is_end = False
                return len(node.children) == 0
            ch = word[depth]
            child = node.children.get(ch)          
            if child is None:                      
                return False
            delete_child = dfs_del(child, word, depth + 1)
            if delete_child:
                del node.children[ch]              # было: node.chldren[ch]
                return (not node.is_end) and (len(node.children) == 0)
            return False

        dfs_del(self.root, word, 0)
        return True