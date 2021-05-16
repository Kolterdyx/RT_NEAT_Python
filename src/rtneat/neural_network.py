from .genome import Genome
from .node_gene import Type
import numpy as np


class NeuralNetwork:
    def __init__(self, genome: Genome):
        self.inputs = []
        self.outputs = []
        self.neurons = {}
        self.unprocessed = []

        self.genome = genome

        for node in genome.nodes.values():
            neuron = Neuron()

            if node.TYPE == Type.INPUT:
                neuron.addInputConnection()
                self.inputs.append(node.ID)
            elif node.TYPE == Type.OUTPUT:
                self.outputs.append(node.ID)

            self.neurons[node.ID] = neuron


        for con in genome.connections.values():
            if con.expressed:
                inputNode = self.neurons[con.inNode]
                inputNode.addOutputConnection(con.outNode, con.weight)
                outputReceiver = self.neurons[con.outNode]
                outputReceiver.addInputConnection()

    def feed(self, X):
        if len(X) != len(self.inputs):
            raise ValueError(f"Input fed to the network ({len(X)}) does not match input size ({len(self.inputs)})")

        for neuron in self.neurons.values():
            neuron.reset()

        self.unprocessed = list(self.neurons.values())

        for i, x in enumerate(X):
            inputNeuron = self.neurons[self.inputs[i]]

            inputNeuron.feed(x)
            inputNeuron.calculate()

            for k, w in zip(inputNeuron.outputIDs, inputNeuron.outputWeights):
                receiver = self.neurons[k]
                receiver.feed(inputNeuron.output * w)

            self.unprocessed.remove(inputNeuron)

        loops = 0
        while len(self.unprocessed) > 0:
            loops += 1
            if loops > 10 ** (len(self.inputs) + 2):
                # raise TimeoutError("Too many iterations to calculate network.py")
                print(self)
                return [0] * len(self.outputs)

            for n in self.unprocessed:
                if n.isReady():
                    n.calculate()
                    for i, j in zip(n.outputIDs, n.outputWeights):
                        value = n.output * j
                        self.neurons[i].feed(value)
                    self.unprocessed.remove(n)

        outputs = []
        for n in self.outputs:
            outputs.append(round(self.neurons[n].output, 8))
        return outputs

    def __str__(self):
        return f"""
Network:
 - Neurons: {len(self.neurons.keys())} {self.neurons}
{self.genome}
"""

    def __repr__(self):
        return self.__str__()


class Neuron:

    def __init__(self):
        self.output = 0.0
        self.inputs = []
        self.nInputs = 0
        self.outputIDs = []
        self.outputWeights = []
        self.calculated = False

    def addInputConnection(self):
        self.nInputs += 1

    def addOutputConnection(self, outputID, weight):
        self.outputIDs.append(outputID)
        self.outputWeights.append(weight)

    def calculate(self):
        if not self.calculated:
            self.output = self.sigmoid(sum(self.inputs))
            self.calculated = True

    def isReady(self):
        if len(self.inputs) != self.nInputs:
            return False
        return True

    def feed(self, data):
        self.inputs.append(data)

    def reset(self):
        self.inputs = []
        self.output = 0.0
        self.calculated = False

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def __str__(self):
        return f"Inputs: {self.inputs}, Output: {self.output}"

    def __repr__(self):
        return self.__str__()
