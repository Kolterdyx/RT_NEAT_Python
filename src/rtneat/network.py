from .tags import *
from .node import *
from .link import *

innovation = 0

def get_innovation():
    global innovation
    innovation += 1
    return innovation

class Network:
    def __init__(self, ninputs, noutputs):
        self.nodes = []
        self.inodes = []
        self.onodes = []
        self.hnodes = []
        self.ninputs = ninputs
        self.noutputs = noutputs

        self.links = {}

        for i in range(ninputs):
            node = Node(INPUT, get_innovation())
            self.nodes.append(node)
            self.inodes.append(node)

        for i in range(noutputs):
            node = Node(OUTPUT, get_innovation())
            self.nodes.append(node)
            self.onodes.append(node)
            for n in self.inodes:
                link = self.new_link(n, node)
                self.links[link.innovation] = link




    def feed(self, X):
        if len(X) != self.ninputs:
            raise ValueError

        for i,node in enumerate(self.inodes):
            node.input_values.append(X[i])
            node.calculate()

        nodes_left = sum([node.activated for node in self.hnodes])

        while nodes_left > 0:
            for node in self.hnodes:
                for link in self.links.values():
                    if link.onode == node:
                        if link.inode.activated:
                            if link.recur:
                                node.input_values.append(link.inode.last_output_value*link.weight)
                            else:
                                node.input_values.append(link.inode.output_value*link.weight)
                node.calculate()
                nodes_left -= 1

        for node in self.onodes:
            for link in self.links.values():
                if link.onode == node:
                    node.input_values.append(link.inode.output_value*link.weight)
                    node.calculate()

        return [node.output_value for node in self.onodes]

    def recur_check(self, link):
        i, o = link.inode, link.onode
        if i == o:
            return True

        elif i.ntype == INPUT or o.ntype == OUTPUT:
            return False

        conList = []

        for c in self.links.values():
            conList.append((c.inode, c.onode))

        visited = {o}

        while True:
            n = 0
            for a, b in conList:
                if a in visited and b not in visited:
                    if b == i:
                        return True
                    visited.add(b)
                    n += 1

            if n == 0:
                return False

    def new_link(self, inode, onode):
        link = Link(inode, onode, get_innovation())
        if self.recur_check(link):
            link.recur = True
        return link


    def add_node(self):
        node = Node(HIDDEN, get_innovation())
        link1 = random.choice(list(self.links.values()))
        old_node = link1.onode
        link1.onode = node
        link2 = self.new_link(node, old_node)
        self.links[link2.innovation] = link2
        self.hnodes.append(node)

    def add_link(self):
        if self.hnodes:
            inode = random.choice(self.hnodes+self.inodes)
            onode = random.choice(self.hnodes+self.onodes)

            link = self.new_link(inode, onode)
            self.links[link.innovation] = link
