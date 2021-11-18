import random
from .globals import *

class Link:
    def __init__(self, inode, onode, inn):
        self.inode = inode
        self.onode = onode
        self.recur = False
        self.weight = round(random.uniform(-4,4), 2)
        self.innovation = inn

    def __str__(self):
        return "R:"+str(self.recur)+"|"+str(self.innovation)+"="+str(self.inode)+"->"+str(self.onode)+":"+str(self.weight)

    def __repr__(self):
        return self.__str__()
