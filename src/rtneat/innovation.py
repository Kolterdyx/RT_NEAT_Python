class InnovationTracker():
    def __init__(self):

        self.innovation = -1

        self.nodes = []
        self.links = {}

    def node_splits_link(self, linkinn):
        if linkinn not in self.links.keys():
            return [False, None]

        linkmap = zip(self.links.keys(), self.links.values())

        for inn, l in linkmap:
            if linkinn == inn:
                # We've found the link we want to know if it's being split elsewhere by a node
                for inn1, l1 in linkmap:
                    for inn2, l2 in linkmap:
                        # We check combinations of links
                        if l1!=l and l1!=l2 and l2!=l:
                            # If we find two links that are different from each other and from the one we're inspecting
                            if (l1[0] == l[0] and l2[1] == l[1] and l1[1]==l2[0]) or (l2[0] == l[0] and l1[1] == l[1] and l2[1]==l1[0]):
                                # If the inode of link A is equal to the inode of the our link and the onode of link B
                                # is equal to the onode of our link, and the onode of link A is equal to the inode
                                # of link B, we've found a split link
                                #               our link
                                #   N1 -------------------------------> N2
                                #  l[0]                                l[1]
                                #
                                #       link A           link B
                                #   N1 -------------> N3 -------------> N2
                                # l1[0]             l1[1]
                                #                   l2[0]             l2[1]

                                return [True, l1[1]]
        return [False, None]

    def link_exists_between(self, n1, n2):
        if n1 not in self.nodes or n2 not in self.nodes:
            return [False, None]
        linkmap = zip(self.links.keys(), self.links.values())
        for inn, link in linkmap:
            if link[0] == n1 and link[1] == n2:
                return [True, inn]

        return [False, None]

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
        return str(self.innovation) + " | " + str(self.nodes) + " | " + str(self.links)

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
