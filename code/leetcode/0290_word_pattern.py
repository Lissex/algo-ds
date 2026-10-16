# Время O(n): split и один проход по парам.
# Память O(n): список слов и два словаря.

class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()
        if len(pattern) != len(words):
            return False
        char_to_word = {}
        word_to_char = {}                  # нужна биекция — проверяем в обе стороны
        for ch, word in zip(pattern, words):
            if char_to_word.get(ch, word) != word:
                return False
            if word_to_char.get(word, ch) != ch:
                return False
            char_to_word[ch] = word
            word_to_char[word] = ch
        return True
