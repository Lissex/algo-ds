from collections import deque

def inorder(root):
    if not root:
        return []
    
    # Лево + Корень + Право
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):
    if not root:
        return []
    
    # Корень + Лево + Право
    return [root.val] + preorder(root.left) + preorder(root.right) 

def postorder(root):
    if not root:
        return []
    
    # Лево + Право + Корень
    return postorder(root.left) + postorder(root.right) + [root.val]

def bfs_binary_tree(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()  # Извлекаем узел из головы очереди
        result.append(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result
