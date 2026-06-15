import random

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

FEATURES = [
    "return",
    "volatility",
    "sentiment",
    "ma5",
    "ma10",
    "ma20",
    "momentum",
    "volume_change",
    "ma_ratio",
    "price_vs_ma5",
    "rsi"
]


def random_chromosome():
    return [
        random.randint(0, 1)
        for _ in FEATURES
    ]


def decode(chromosome):
    selected = [
        FEATURES[i]
        for i, bit in enumerate(chromosome)
        if bit == 1
    ]

    # Ensure at least one feature
    if len(selected) == 0:
        selected = ["return"]

    return selected


def evaluate_chromosome(df, chromosome):
    selected_features = decode(chromosome)

    X = df[selected_features]
    y = df["target"]

    if len(df) < 50:
        return 0

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            shuffle=False
        )

        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        score = accuracy_score(
            y_test,
            predictions
        )

        return score

    except Exception:
        return 0


def tournament_selection(
    population,
    fitnesses
):
    i1 = random.randint(
        0,
        len(population) - 1
    )

    i2 = random.randint(
        0,
        len(population) - 1
    )

    if fitnesses[i1] > fitnesses[i2]:
        return population[i1]

    return population[i2]


def crossover(parent1, parent2):
    point = random.randint(
        1,
        len(parent1) - 1
    )

    child1 = (
        parent1[:point]
        + parent2[point:]
    )

    child2 = (
        parent2[:point]
        + parent1[point:]
    )

    return child1, child2


def mutate(
    chromosome,
    mutation_rate=0.10
):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = (
                1 - chromosome[i]
            )

    return chromosome


def ga_feature_selection(
    df,
    generations=20,
    population_size=20
):
    population = [
        random_chromosome()
        for _ in range(population_size)
    ]

    best_chromosome = None
    best_fitness = -1

    for _ in range(generations):

        fitnesses = [
            evaluate_chromosome(
                df,
                chromosome
            )
            for chromosome in population
        ]

        current_best = max(fitnesses)

        if current_best > best_fitness:
            best_fitness = current_best

            best_chromosome = population[
                fitnesses.index(
                    current_best
                )
            ]

        new_population = []

        while len(new_population) < population_size:

            parent1 = tournament_selection(
                population,
                fitnesses
            )

            parent2 = tournament_selection(
                population,
                fitnesses
            )

            child1, child2 = crossover(
                parent1,
                parent2
            )

            child1 = mutate(child1)
            child2 = mutate(child2)

            new_population.append(child1)
            new_population.append(child2)

        population = new_population[
            :population_size
        ]

    return decode(best_chromosome)
