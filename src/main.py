import random

class Mutator:
    def __init__(self, genome):
        self.genome = genome

    def mutate(self, mutation_rate=0.01):
        """Mutate the genome with the given mutation rate."""
        mutated_genome = []
        for gene in self.genome:
            if random.random() < mutation_rate:
                mutated_gene = self.mutate_gene(gene)
                mutated_genome.append(mutated_gene)
            else:
                mutated_genome.append(gene)
        return mutated_genome

    def mutate_gene(self, gene):
        """Mutate a single gene using a variety of techniques."""
        mutation_type = random.randint(1, 5)
        if mutation_type == 1:
            return self.point_mutation(gene)
        elif mutation_type == 2:
            return self.insertion_mutation(gene)
        elif mutation_type == 3:
            return self.deletion_mutation(gene)
        elif mutation_type == 4:
            return self.duplication_mutation(gene)
        else:
            return self.inversion_mutation(gene)

    def point_mutation(self, gene):
        """Replace a random character in the gene with a new random character."""
        gene_list = list(gene)
        index = random.randint(0, len(gene_list) - 1)
        gene_list[index] = chr(random.randint(ord('a'), ord('z')))
        return ''.join(gene_list)

    def insertion_mutation(self, gene):
        """Insert a new random character at a random position in the gene."""
        gene_list = list(gene)
        index = random.randint(0, len(gene_list))
        gene_list.insert(index, chr(random.randint(ord('a'), ord('z'))))
        return ''.join(gene_list)

    def deletion_mutation(self, gene):
        """Remove a random character from the gene."""
        gene_list = list(gene)
        if len(gene_list) > 0:
            index = random.randint(0, len(gene_list) - 1)
            del gene_list[index]
        return ''.join(gene_list)

    def duplication_mutation(self, gene):
        """Duplicate a random substring of the gene."""
        gene_list = list(gene)
        start = random.randint(0, len(gene_list) - 1)
        end = random.randint(start, len(gene_list) - 1)
        duplicate = ''.join(gene_list[start:end+1])
        gene_list.insert(random.randint(0, len(gene_list)), duplicate)
        return ''.join(gene_list)

    def inversion_mutation(self, gene):
        """Reverse a random substring of the gene."""
        gene_list = list(gene)
        start = random.randint(0, len(gene_list) - 1)
        end = random.randint(start, len(gene_list) - 1)
        gene_list[start:end+1] = reversed(gene_list[start:end+1])
        return ''.join(gene_list)
