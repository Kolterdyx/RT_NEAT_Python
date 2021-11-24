from rtneat import *
from pprint import pprint
import pickle

from rtneat import Config


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
    random.seed(2)
    test_net()
    # evolve_xor()


def test_net():
    X = [-32, 1.7]

    inn = InnovationTracker()
    cfg = Config()

    nn1 = Network(2, 1, inn, cfg)
    nn1.add_link()

    nn2 = Network(2, 1, inn, cfg)
    nn2.add_link()
    nn2.add_link()


    nn1.add_node()
    nn2.add_node()



    # log.info(nn1.feed(X))
    # log.info(nn1.feed(X))
    # log.info(nn1.feed(X))
    # log.info(nn1.links)



    # log.info(nn2.feed(X))
    # log.info(nn2.feed(X))
    # log.info(nn2.feed(X))
    # log.info(nn2.links)

    nn1.export_json("nn1.json")
    nn2.export_json("nn2.json")


def evolve_xor():
    xor = [
        ((0.0, 0.0), 0.0),
        ((0.0, 1.0), 1.0),
        ((1.0, 0.0), 1.0),
        ((0.0, 0.0), 0.0)
    ]

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
