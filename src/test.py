from rtneat import *
from pprint import pprint
import pickle


class Entity:
    def __init__(self, inn, config):
        self.brain = Network(2, 1, inn, config)
        self.brain.add_link()
        self.brain.add_link()
        self.brain.add_node()
        self.fitness = 4.0

    def input(self, X):
        for xi, xo in X:
            result = self.brain.feed(xi)[0]
            self.fitness -= (result - xo) ** 2

    def __gt__(self, other):
        if isinstance(other, Entity):
            return self.fitness > other.fitness

    def __lt__(self, other):
        if isinstance(other, Entity):
            return self.fitness < other.fitness

    def __ge__(self, other):
        if isinstance(other, Entity):
            return self.fitness >= other.fitness

    def __le__(self, other):
        if isinstance(other, Entity):
            return self.fitness <= other.fitness

    def __str__(self):
        return str(self.fitness)

    def __repr__(self):
        return str(self)


def main():
    # log.setLevel(DEBUG)
    # random.seed(1)

    xor = [
        ((0.0, 0.0), 0.0),
        ((0.0, 1.0), 1.0),
        ((1.0, 0.0), 1.0),
        ((0.0, 0.0), 0.0)
    ]

    X = [-32, 1.7]

    inn = InnovationTracker()
    config = Config()

    nn = Network(2, 1, inn, config)
    nn.add_link()
    nn.add_link()
    nn.add_link()
    nn.add_link()
    nn.add_link()
    nn.add_node()

    log.info(nn.feed(X))
    #
    # nn.export_json("model.json")
    # nn.export_pickle("model.pickle")
    #
    # nn.import_pickle("model.pickle")
    #
    # print(nn.feed(X))
    #
    # nn.import_json("model.json")
    #
    # print(nn.feed(X))

    max_pop = 25

    pop = []
    for i in range(max_pop):
        pop.append(Entity(inn, config))

    for e in pop:
        e.input(xor)
        # log.info(e.fitness)

    pop = sorted(pop)
    pop.reverse()

    survivors = pop[:int(max_pop / 2)]

    print(survivors)


if __name__ == '__main__':
    main()
