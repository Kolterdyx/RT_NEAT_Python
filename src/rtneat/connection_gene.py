class ConnectionGene:
    inNode = None
    outNode = None
    weight = int()
    expressed = bool()
    innovation = int()

    def __init__(self, inNode: int, outNode: int, weight: float, expressed: bool, innovation: int):
        self.inNode = inNode
        self.outNode = outNode
        self.weight = weight
        self.expressed = expressed
        self.innovation = innovation

    def disable(self):
        self.expressed = False

    def enable(self):
        self.expressed = True

    def __str__(self):
        return f"""Connection:
 + Input:      {self.inNode}
 + Output:     {self.outNode}
 + Weight:     {self.weight}
 + Enabled:    {self.expressed}
 + Innovation: {self.innovation}
"""

    def __repr__(self): return self.__str__()


def copy(self):
    return ConnectionGene(self.inNode, self.outNode, self.weight, self.expressed, self.innovation)


setattr(ConnectionGene, 'copy', copy)
