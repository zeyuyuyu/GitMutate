import random

class Mutator:
    def __init__(self, mutation_rate=0.1):
        self.mutation_rate = mutation_rate

    def mutate(self, input_str):
        """Mutate the input string with a given probability."""
        output_chars = []
        for char in input_str:
            if random.random() < self.mutation_rate:
                output_chars.append(chr(random.randint(32, 126)))
            else:
                output_chars.append(char)
        return ''.join(output_chars)

if __name__ == '__main__':
    mutator = Mutator(mutation_rate=0.2)
    original_text = "The quick brown fox jumps over the lazy dog."
    mutated_text = mutator.mutate(original_text)
    print(f"Original text: {original_text}")
    print(f"Mutated text: {mutated_text}")
