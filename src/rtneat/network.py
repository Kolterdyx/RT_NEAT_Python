from .genome import *
from .neural_network import *
from .counter import *
import random


class Network:
    def __init__(self, inputs, outputs):
        self.genome = Genome()
        self.nCounter = Counter()
        self.iCounter = Counter()

        self.mutate_weight_chance = 1
        self.weight_mutation_strength = 1
        self.mutate_add_connection_chance = 0.01
        self.mutate_add_node_chance = 0.01
        self.mutate_rem_node_chance = 0.01
        self.mutate_rem_connection_chance = 0.01

        for i in range(inputs):
            self.genome.addInput(self.nCounter)

        for i in range(outputs):
            self.genome.addOutput(self.nCounter)

        self.network = NeuralNetwork(self.genome)

    def mutate(self):
        mutation = random.randint(0, 2)
        chance = random.uniform(0, 1)

        if mutation == 0:
            if self.mutate_add_node_chance > chance:
                self.genome.addNodeMutation(self.nCounter, self.iCounter)
        elif mutation == 1:
            if self.mutate_weight_chance > chance:
                self.genome.addWeightMutation(self.weight_mutation_strength)
        elif mutation == 2:
            if self.mutate_add_connection_chance > chance:
                self.genome.addConnectionMutation(self.iCounter)
        elif mutation == 3:
            if self.mutate_rem_node_chance > chance:
                self.genome.remNodeMutation()
        elif mutation == 4:
            if self.mutate_rem_connection_chance > chance:
                self.genome.remConnectionMutation()


        self.update_network()

    def feed(self, X):
        return self.network.feed(X)

    def update_network(self):
        self.network = NeuralNetwork(self.genome)

    def __str__(self):
        return str(self.network)

