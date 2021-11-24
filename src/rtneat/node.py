from .globals import *


class Node:
    def __init__(self, node_type, inn):
        self.ntype = node_type
        self.input_values = []
        self.output_value = 0
        self.last_output_value = 0
        self.activated = False
        self.innovation = inn

    def activate(self):
        self.output_value = sigmoid(sum(self.input_values))  # if self.ntype != INPUT else sum(self.input_values)
        self.last_output_value = self.output_value
        self.activated = True
        log.debug(self.debug())

    def debug(self):
        return str(self) + "|" + str(self.input_values) + "|" + str(self.output_value) + "|" + str(
            self.last_output_value)

    def __str__(self):
        return "N" + str(self.innovation) + "." + str(self.ntype)

    def __repr__(self):
        return str(self)

    def serialize(self):
        return self.innovation, self.ntype


def sigmoid(x):
    return round(1 / (1 + np.exp(-x)), 6)
