from enum import Enum
class Type(Enum):
    INPUT = 0
    HIDDEN = 1
    OUTPUT = 2

class NodeGene:
    TYPE = None
    ID = int()

    def __init__(self, t, i: int()):
        self.TYPE = t
        self.ID = i

    def __str__(self):
        return f"ID: {self.ID}, TYPE = {self.TYPE}"

    def __repr__(self):return self.__str__()

def copy(self):
    return NodeGene(self.TYPE, self.ID)

setattr(NodeGene, "copy", copy)
