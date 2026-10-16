class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {')': '(', ']': '[', '}': '{'}
        stack = []
        for ch in s:
            if ch in pairs:                            # закрывающая скобка
                if not stack or stack[-1] != pairs[ch]:
                    return False
                stack.pop()
            else:                                      # открывающая — кладём в стек
                stack.append(ch)
        return not stack                               # все скобки должны закрыться
