import os
import random

class GitMutator:
    def __init__(self):
        self.mutation_rate = 0.1

    def mutate_file(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if random.random() < self.mutation_rate:
                lines[i] = self._mutate_line(lines[i])

        with open(filepath, 'w') as f:
            f.writelines(lines)

    def _mutate_line(self, line):
        words = line.split()
        for i in range(len(words)):
            if random.random() < self.mutation_rate:
                words[i] = self._mutate_word(words[i])
        return ' '.join(words) + '\n'

    def _mutate_word(self, word):
        mutation = random.choice(['replace', 'insert', 'delete'])
        if mutation == 'replace':
            return self._replace_char(word)
        elif mutation == 'insert':
            return self._insert_char(word)
        else:
            return self._delete_char(word)

    def _replace_char(self, word):
        idx = random.randint(0, len(word) - 1)
        return word[:idx] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[idx+1:]

    def _insert_char(self, word):
        idx = random.randint(0, len(word))
        return word[:idx] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[idx:]

    def _delete_char(self, word):
        if len(word) == 1:
            return ''
        idx = random.randint(0, len(word) - 1)
        return word[:idx] + word[idx+1:]

if __name__ == '__main__':
    mutator = GitMutator()
    mutator.mutate_file('./src/main.py')
