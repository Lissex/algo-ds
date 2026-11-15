class Node:
    def __init__(self, val):
        self.val = val
        self.right = None
        self.left = None

class BinaryTree:
    def __init__(self, root):
        self.root = Node(root)
        self.size = 1

    def add_node(self, val):
        new_node = Node(val)
        cur = self.root
        while cur:
            parent = cur
            if cur.val == val:
                raise ValueError(f'node {val} already in tree')
            if cur.val > val:
                cur = cur.left
            else:
                cur = cur.right
        if parent.val > val:
            parent.left = new_node
        else:
            parent.right = new_node
        self.size += 1
        return

    def find(self, val):
        cur = self.root
        while cur:
            if cur.val == val:
                return True
            elif cur.val > val:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def remove(self, val):
        self.root = self._remove(self.root, val)


    def _remove(self, node, val):
        if node is None:
            return None

        if val < node.val:
            node.left = self._remove(node.left, val)
            return node

        if val > node.val:
            node.right = self._remove(node.right, val)
            return node
        
        
        if not node.left and not node.right:
            return None

        if not node.left:
            return node.right
        if not node.right:
            return node.left


        min_node = self._min_node(node.right)
        node.val = min_node.val  
        node.right = self._remove(node.right, min_node.val)  

        return node

    def _min_node(self, node):
        while node.left:
            node = node.left
        return node

    def count_nodes(self):
        return self.size


    def bfs(self):
        res = []
        cur = [self.root]
        while cur:
            tmp = []
            for node in cur:
                res.append(node.val)
                if node.left:
                    tmp.append(node.left)
                if node.right:
                    tmp.append(node.right)
            cur = tmp
        return res

    def dfs(self):
        res = []

        def dfs_rec(node):
            if not node:
                return
            dfs_rec(node.left)
            res.append(node.val)
            dfs_rec(node.right)

        dfs_rec(self.root)
        return res

    def get_max(self):
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.val

    def get_min(self):
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.val