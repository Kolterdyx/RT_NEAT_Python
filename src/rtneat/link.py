from .globals import *


class Link:
    def __init__(self, inode, onode, inn):
        self.inode = inode
        self.onode = onode
        self.recur = False
        self.weight = round(random.uniform(-4, 4), 6)
        self.innovation = inn
        self.enabled = True

    def __str__(self):
        return "E:" + str(self.enabled) + "|R:" + str(self.recur) + "|" + str(self.innovation) + "=" + str(
            self.inode) + "->" + str(self.onode) + ":" + str(self.weight)

    def __repr__(self):
        return self.__str__()

    def serialize(self):
        return self.innovation, {"connection": [self.inode.innovation, self.onode.innovation], "enabled": self.enabled,
                                 "recurrent": self.recur, "weight": self.weight}
