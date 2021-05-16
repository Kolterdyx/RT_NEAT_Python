import random
from .connection_gene import ConnectionGene
from .node_gene import NodeGene, Type
from .counter import Counter


def random_bool():
    return random.choice((True, False))


class Genome:
    nodes = {}
    connections = {}
    hidden_nodes = []

    def addNode(self, node: NodeGene):
        self.nodes[node.ID] = node

    def remNode(self, node: NodeGene):
        del self.nodes[node.ID]
        for con in self.connections.keys():
            connection = self.connections[con]
            if node.ID == connection.inNode or node.ID == connection.outNode:
                self.connections[con].disable()

    def addConnection(self, connection: ConnectionGene):
        if connection in self.connections.values():
            self.connections[connection.innovation].enable()
        if not creates_loop(self.connections, connection):
            self.connections[connection.innovation] = connection

    def remConnection(self, connection: ConnectionGene):
        self.connections[connection.innovation].disable()

    def addInput(self, counter):
        self.addNode(NodeGene(Type.INPUT, counter.getNumber()))

    def addHidden(self, counter):
        node = NodeGene(Type.HIDDEN, counter.getNumber())
        self.addNode(node)
        self.hidden_nodes.append(node)

    def addOutput(self, counter):
        self.addNode(NodeGene(Type.OUTPUT, counter.getNumber()))

    def addConnectionMutation(self, innovation: Counter):
        node1 = random.choice(list(self.nodes.values()))
        node2 = random.choice(list(self.nodes.values()))
        while node2 == node1:
            node2 = random.choice(list(self.nodes.values()))

        reverse = False
        if node1.TYPE == Type.HIDDEN and node2.TYPE == Type.INPUT:
            reverse = True
        elif node1.TYPE == Type.OUTPUT and node2.TYPE == Type.HIDDEN:
            reverse = True
        elif node1.TYPE == Type.OUTPUT and node2.TYPE == Type.INPUT:
            reverse = True

        connectionExists = False
        for con in self.connections.values():
            if con.inNode == node1.ID and con.outNode == node2.ID:
                connectionExists = True
                break
            elif con.inNode == node2.ID and con.outNode == node1.ID:
                connectionExists = True
                break

        if connectionExists:
            return

        new_con = ConnectionGene(node2.ID if reverse else node1.ID, node1.ID if reverse else node2.ID,
                                 random.uniform(-1, 1), True, innovation.getNumber())

        self.addConnection(new_con)

    def remConnectionMutation(self):
        self.remConnection(random.choice(list(self.connections.keys()))) if self.connections != {} else None

    def addNodeMutation(self, nCounter: Counter, iCounter: Counter):
        if self.connections != {}:
            con = random.choice(list(self.connections.values()))

            inNode = self.nodes[con.inNode]
            outNode = self.nodes[con.outNode]

            con.disable()

            newNode = NodeGene(Type.HIDDEN, nCounter.getNumber())
            inToNew = ConnectionGene(inNode.ID, newNode.ID, 1.0, True, iCounter.getNumber())
            newToOut = ConnectionGene(newNode.ID, outNode.ID, con.weight, True, iCounter.getNumber())

            self.addNode(newNode)
            self.addConnection(inToNew)
            self.addConnection(newToOut)

    def remNodeMutation(self):
        if self.nodes != {}:
            node = random.choice(self.hidden_nodes)
            self.remNode(node)

    def addWeightMutation(self, strength: float):
        if len(list(self.connections.keys())) > 0:
            con = random.choice(list(self.connections.values()))
            con.weight += random.uniform(-1, 1)*strength

    @staticmethod
    def countMatchingGenes(self, genome1, genome2):
        matchingGenes = 0

        nodeKeys1 = sorted(list(genome1.nodes.keys()))
        nodeKeys2 = sorted(list(genome2.nodes.keys()))

        highestInnovation1 = nodeKeys1[-1]
        highestInnovation2 = nodeKeys2[-1]

        indices = max(highestInnovation1, highestInnovation2)

        for i in range(indices):
            node1 = i in genome1.nodes.keys()
            node2 = i in genome2.nodes.keys()

            if node1 and node2:
                matchingGenes += 1

        conKeys1 = sorted(list(genome1.connections.keys()))
        conKeys2 = sorted(list(genome2.connections.keys()))

        highestInnovation1 = conKeys1[-1]
        highestInnovation2 = conKeys2[-1]

        indices = max(highestInnovation1, highestInnovation2)

        for i in range(indices):
            con1 = i in genome1.connections.keys()
            con2 = i in genome2.connections.keys()

            if con1 and con2:
                matchingGenes += 1

        return matchingGenes

    @staticmethod
    def countDisjointGenes(self, genome1, genome2):
        disjointGenes = 0

        nodeKeys1 = sorted(list(genome1.nodes.keys()))
        nodeKeys2 = sorted(list(genome2.nodes.keys()))

        highestInnovation1 = nodeKeys1[-1]
        highestInnovation2 = nodeKeys2[-1]

        indices = max(highestInnovation1, highestInnovation2)

        for i in range(indices):
            node1 = i in genome1.nodes.keys()
            node2 = i in genome2.nodes.keys()

            if (not node1 and node2 and highestInnovation1 > i) or (node1 and not node2 and highestInnovation2 > i):
                disjointGenes += 1

        return disjointGenes

    @staticmethod
    def countExcessGenes(self, genome1, genome2):
        excessGenes = 0

        nodeKeys1 = sorted(list(genome1.nodes.keys()))
        nodeKeys2 = sorted(list(genome2.nodes.keys()))

        highestInnovation1 = nodeKeys1[-1]
        highestInnovation2 = nodeKeys2[-1]

        indices = max(highestInnovation1, highestInnovation2)

        for i in range(indices):
            node1 = i in genome1.nodes.keys()
            node2 = i in genome2.nodes.keys()

            if (not node1 and node2 and highestInnovation1 < i) or (node1 and not node2 and highestInnovation2 < i):
                excessGenes += 1

        conKeys1 = sorted(list(genome1.connections.keys()))
        conKeys2 = sorted(list(genome2.connections.keys()))

        highestInnovation1 = conKeys1[-1]
        highestInnovation2 = conKeys2[-1]

        indices = max(highestInnovation1, highestInnovation2)

        for i in range(indices):
            con1 = i in genome1.connections.keys()
            con2 = i in genome2.connections.keys()

            if (not con1 and con2 and highestInnovation1 < i) or (con1 and not con2 and highestInnovation2 < i):
                excessGenes += 1

        return excessGenes

    @staticmethod
    def averageWeightDiff(self, genome1, genome2):
        matchingGenes = 0
        weightDiff = 0

        conKeys1 = sorted(list(genome1.connections.keys()))
        conKeys2 = sorted(list(genome2.connections.keys()))

        highestInnovation1 = conKeys1[-1]
        highestInnovation2 = conKeys2[-1]

        indices = max(highestInnovation1, highestInnovation2)

        for i in range(indices):
            con1 = i in genome1.connections.keys()
            con2 = i in genome2.connections.keys()
            connection1 = genome1.connections[con1]
            connection2 = genome2.connections[con2]

            if con1 and con2:
                matchingGenes += 1
                weightDiff += abs(connection1.weight - connection2.weight)

        return weightDiff / matchingGenes

    @staticmethod
    def compatibilityDistance(self, genome1, genome2, c1: int, c2: int, c3: int):
        E = self.countExcessGenes(genome1, genome2)
        D = self.countDisjointGenes(genome1, genome2)
        W = self.averageWeightDiff(genome1, genome2)

        N = 1

        o = c1 * E / N + c2 * D / N + c3 * W

        return o

    def __str__(self):
        a = str(self.nodes)
        b = str(self.connections)

        return f"""Genome:
 - Nodes:       {len(self.nodes.keys())} {a}
 - Connections: {len(self.connections.keys())} {b}
"""




@staticmethod
def crossover(self, parent1: Genome, parent2: Genome):
    child = Genome()

    for p1node in parent1.nodes.values():
        child.addNode(p1node.copy())

    for p1con in parent1.connections.values():
        if p1con.innovation in parent2.connections.keys():  # matching gene
            childConnection = p1con.copy() if random_bool else parent2.connections[p1con.innovation].copy()
            child.addConnection(childConnection)
        else:  # disjoint / excess
            child.addConnection(p1con.copy())

    return child


def creates_loop(connections: dict, con):
    i, o = con.inNode, con.outNode
    if i == o:
        return True

    conList = []

    for c in connections.values():
        conList.append((c.inNode, c.outNode))

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


setattr(Genome, 'crossover', crossover)
