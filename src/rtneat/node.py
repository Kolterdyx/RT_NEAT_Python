from .tags import *
import numpy as np

class Node:
    def __init__(self, node_type, inn):
        self.ntype = node_type
        self.input_values = []
        self.output_value = 0
        self.last_output_value = 0
        self.activated = False
        self.innovation = inn

    def calculate(self):
        self.last_output_value = self.output_value
        self.output_value = sigmoid(sum(self.input_values))

    def __str__(self):
        return "N"+str(self.innovation)


def sigmoid(x):
    return round(1/(1+np.exp(-x)), 6)
