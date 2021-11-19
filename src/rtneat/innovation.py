class InnovationTracker():
    def __init__(self):

        self.innovation = 0

        self.nodes = []
        self.links = {}

    def node_exists_between(self, n1, n2):
        if n1 not in self.nodes or n2 not in self.nodes:
            return False

        linkmap = zip(self.links.keys(), self.links.values())
        for inn1, l1 in linkmap:
            for inn2, l2 in linkmap:
                if (l1[0] == n1 and l2[1] == n2 and l1[1] == l2[0]) and l1 != l2:
                    return [True, l1[1]]
        return [False]

    def link_exists_between(self, n1, n2):
        if n1 not in self.nodes or n2 not in self.nodes:
            return False
        linkmap = zip(self.links.keys(), self.links.values())
        for inn, link in linkmap:
            if link[0]==n1 and link[1]==n2:
                return [True, inn]

        return [False]


    def new_node(self):
        inn = self.new_innovation_number()
        self.nodes.append(self.innovation)
        return inn

    def new_link(self, n1, n2):
        inn = self.new_innovation_number()
        self.links[inn] = (n1, n2)
        return inn

    def new_innovation_number(self):
        self.innovation += 1
        return self.innovation

    def __str__(self):
        return str(self.innovation)+" | "+str(self.nodes)+" | "+str(self.links)

    def serialize(self):
        data = {
            "nodes": self.nodes,
            "links": self.links,
            "last_innovation": self.innovation
        }

        return data

    def deserialize(self, data: dict):
        self.nodes = data["nodes"]
        self.links = data["links"]
        self.innovation = data["last_innovation"]
