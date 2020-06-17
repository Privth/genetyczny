import sys
from abc import abstractmethod, ABC
from random import randint, choice
from random import random, choice


def elite_selection_model(generation):
    max_selected = int(len(generation) / 10)
    sorted_by_assess = sorted(generation, key=lambda x: x.fitness)
    return sorted_by_assess[:max_selected]


class Element(ABC):

    @abstractmethod
    def __init__(self):
        self.fitness = self.evaluate_function()

    def mutation(self):
        self._perform_mutation()
        self.fitness = self.evaluate_function()

    @abstractmethod
    def _perform_mutation(self):
        pass

    @abstractmethod
    def crossover(self, element2: 'Element') -> 'Element':
        pass

    @abstractmethod
    def evaluate_function(self):
        pass


class GeneticAlgorithm:

    def __init__(self, first_population_generator: callable,
                 selection_model: callable, stop_condition: callable, mutation_probability: float = 0.1):
        self.first_generation_func = first_population_generator
        self.selection_model = selection_model
        self.stop_condition = stop_condition
        self.mutation_probability = mutation_probability

    def run(self):
        population = self.first_generation_func()
        population.sort(key=lambda x: x.fitness)
        population_len = len(population)
        i = 0
        while True:
            selected = self.selection_model(population)
            new_population = selected.copy()
            while len(new_population) != population_len:
                child = choice(population).crossover(choice(population))
                if random() <= self.mutation_probability:
                    child.mutation()
                new_population.append(child)

            population = new_population
            the_best_match = min(population, key=lambda x: x.fitness)
            print("Generation: {} S: {} fitness: {}".format(i, the_best_match, the_best_match.fitness))

            i += 1
            if self.stop_condition(the_best_match, the_best_match.fitness, i):
                break


TARGET = "Tutaj wpisac tekst do testu"


class Text(Element):
    POSSIBILITIES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

    def __init__(self, text):
        self.text = text
        super().__init__()

    def _perform_mutation(self):
        random_index = randint(0, len(self.text) - 1)
        text_as_list = list(self.text)
        text_as_list[random_index] = choice(self.POSSIBILITIES)
        self.text = "".join(text_as_list)

    def crossover(self, element2: 'Element') -> 'Element':
        length = int(randint(0, len(self.text) - 1))
        new_text = self.text[:length] + element2.text[length:]

        return Text(new_text)

    def evaluate_function(self):
        diff = 0
        for letter1, letter2 in zip(self.text, TARGET):
            if letter1 != letter2:
                diff += 1
        return diff

    def __repr__(self):
        return self.text


def first_population_generator():
    return [Text(''.join(choice(Text.POSSIBILITIES) for _ in range(len(TARGET)))) for _ in range(100)]


def stop_condition(string, current_fitness, i):
    return current_fitness == 0


ga = GeneticAlgorithm(first_population_generator, elite_selection_model, stop_condition)
ga.run()
