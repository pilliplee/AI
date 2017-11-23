from sga import genetic_algorithm, init_population, selection_chances, reproduce, mutate, weighted_sampler

def test_genetic_algorithm():
    # Graph coloring
    edges = {
        'A': [0, 1],
        'B': [0, 3],
        'C': [1, 2],
        'D': [2, 3]
    }

    def fitness(c):
        return sum(c[n1] != c[n2] for (n1, n2) in edges.values())

    solution_chars = GA_GraphColoringChars(edges, fitness)
    assert solution_chars == ['R', 'G', 'R', 'G'] or solution_chars == ['G', 'R', 'G', 'R']

    solution_bools = GA_GraphColoringBools(edges, fitness)
    assert solution_bools == [True, False, True, False] or solution_bools == [False, True, False, True]

    solution_ints = GA_GraphColoringInts(edges, fitness)
    assert solution_ints == [0, 1, 0, 1] or solution_ints == [1, 0, 1, 0]

    # Queens Problem
    gene_pool = range(8)
    population = init_population(100, gene_pool, 8)

    def fitness(q):
        non_attacking = 0
        for row1 in range(len(q)):
            for row2 in range(row1+1, len(q)):
                col1 = int(q[row1])
                col2 = int(q[row2])
                row_diff = row1 - row2
                col_diff = col1 - col2

                if col1 != col2 and row_diff != col_diff and row_diff != -col_diff:
                    non_attacking += 1

        return non_attacking


    solution = genetic_algorithm(population, fitness, gene_pool=gene_pool, f_thres=25)
    assert fitness(solution) >= 25


def GA_GraphColoringChars(edges, fitness):
    gene_pool = ['R', 'G']
    population = init_population(8, gene_pool, 4)

    return genetic_algorithm(population, fitness, gene_pool=gene_pool)


def GA_GraphColoringBools(edges, fitness):
    gene_pool = [True, False]
    population = init_population(8, gene_pool, 4)

    return genetic_algorithm(population, fitness, gene_pool=gene_pool)


def GA_GraphColoringInts(edges, fitness):
    population = init_population(8, [0, 1], 4)

    return genetic_algorithm(population, fitness)

if __name__ == '__main__':
   result = test_genetic_algorithm()
   print(result)