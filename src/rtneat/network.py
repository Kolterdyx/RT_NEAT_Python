from .globals import *
from .innovation import InnovationTracker
from .link import Link
from .node import Node
from .config import Config


class Network:
    def __init__(self, ninputs: int, noutputs: int, innovationtracker: InnovationTracker, config: Config):
        self.nodes = {}
        self.inodes = []
        self.onodes = []
        self.hnodes = []
        self.ninputs = ninputs
        self.noutputs = noutputs
        self.inn = innovationtracker

        self.config = config

        self.links = {}

        self.initial_nodes_inn = -1-ninputs-noutputs

        for i in range(ninputs):
            node = Node(INPUT, self.new_initial_node())
            self.nodes[node.innovation] = node
            self.inodes.append(node)

        for i in range(noutputs):
            node = Node(OUTPUT, self.new_initial_node())
            self.nodes[node.innovation] = node
            self.onodes.append(node)

    def new_initial_node(self):
        self.initial_nodes_inn += 1
        self.inn.nodes.append(self.initial_nodes_inn) if self.initial_nodes_inn not in self.inn.nodes else None
        return self.initial_nodes_inn

    def feed(self, input_values: list):
        if len(input_values) != self.ninputs:
            raise ValueError

        for node in self.nodes.values():
            node.input_values = []
            node.activated = False

        # Calculate input nodes
        for i, node in enumerate(self.inodes):
            node.input_values.append(input_values[i])
            node.activate()

        # Calculate hidden nodes
        nodes_left = sum([not node.activated for node in self.hnodes])
        while nodes_left > 0:
            for node in self.hnodes:
                for link in self.links.values():
                    if link.enabled:
                        if link.onode == node:
                            if link.inode.activated:
                                node.input_values.append(link.inode.output_value * link.weight)
                            elif link.recur:
                                node.input_values.append(link.inode.last_output_value * link.weight)

                if not node.activated:
                    node.activate()
                    nodes_left -= 1

        # Calculate output nodes
        for node in self.onodes:
            for link in self.links.values():
                if link.onode == node:
                    node.input_values.append(link.inode.output_value * link.weight)

            node.activate()

        return [node.output_value for node in self.onodes]

    def recur_check(self, link: Link):
        """
        This method was mostly copied from the neat-python repo:
        https://github.com/CodeReclaimers/neat-python/blob/master/neat/graphs.py
        """
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

    def exists_link(self, inode: Node, onode: Node):
        for link in self.links.values():
            if link.inode == inode and link.onode == onode:
                return True, link
        return False, None

    def new_link(self, inode: Node, onode: Node):
        link_exists, link = self.exists_link(inode, onode)
        if link_exists:
            if not link.enabled:
                link.enabled = True
                return link

        link_check = self.inn.link_exists_between(inode.innovation, onode.innovation)
        if link_check[0]:
            link = Link(inode, onode, link_check[1])
        else:
            link = Link(inode, onode, self.inn.new_link(inode.innovation, onode.innovation))

        if self.recur_check(link):
            link.recur = True
        return link

    def add_link(self, link: Link = None):
        if not link:
            if self.hnodes:
                inode = random.choice(self.hnodes + self.inodes)
                onode = random.choice(self.hnodes + self.onodes)

                link_exists, existing_link = self.exists_link(inode, onode)
                while link_exists:
                    if not existing_link.enabled:
                        break
                    inode = random.choice(self.hnodes + self.inodes)
                    onode = random.choice(self.hnodes + self.onodes)
                    link_exists, existing_link = self.exists_link(inode, onode)

                link = self.new_link(inode, onode)
                self.links[link.innovation] = link
            else:
                inode = random.choice(self.inodes)
                onode = random.choice(self.onodes)

                link_exists, existing_link = self.exists_link(inode, onode)
                while link_exists:
                    if not existing_link.enabled:
                        break
                    inode = random.choice(self.inodes)
                    onode = random.choice(self.onodes)
                    link_exists, existing_link = self.exists_link(inode, onode)

                link = self.new_link(inode, onode)
                self.links[link.innovation] = link
        elif isinstance(link, Link):
            self.links[link.innovation] = link

    def add_node(self):

        old_link = random.choice(list(self.links.values()))
        while not old_link.enabled:
            old_link = random.choice(list(self.links.values()))
        old_link.enabled = False
        node_check = self.inn.node_splits_link(old_link.innovation)
        if node_check[0]:
            node = Node(HIDDEN, node_check[1])
        else:
            node = Node(HIDDEN, self.inn.new_node())
        old_node = old_link.onode
        new_link1 = self.new_link(old_link.inode, node)
        new_link2 = self.new_link(node, old_node)
        self.add_link(new_link1)
        self.add_link(new_link2)
        self.hnodes.append(node)
        self.nodes[node.innovation] = node
        return node

    def serialize(self):
        data = {
            "nodes": {},
            "links": {},
            "config": self.config.serialize(),
            "innovation_tracker": self.inn.serialize()
        }

        for node in self.nodes.values():
            inn, node_data = node.serialize()
            data["nodes"][inn] = node_data

        for link in self.links.values():
            inn, link_data = link.serialize()
            data["links"][inn] = link_data

        return data

    def deserialize(self, data: dict):
        log.warning("This will overwrite the current network data")
        self.nodes = {}
        self.inodes = []
        self.onodes = []
        self.hnodes = []
        self.links = {}

        node_dict = data["nodes"]
        link_dict = data["links"]
        self.config.deserialize(data["config"])
        self.inn.deserialize(data["innovation_tracker"])

        for inn, ntype in zip(node_dict.keys(), node_dict.values()):
            node = Node(ntype, int(inn))
            self.nodes[int(inn)] = node
            if ntype == INPUT:
                self.inodes.append(node)
            elif ntype == HIDDEN:
                self.hnodes.append(node)
            elif ntype == OUTPUT:
                self.onodes.append(node)

        for inn, link_data in zip(link_dict.keys(), link_dict.values()):
            con = link_data["connection"]
            self.links[int(inn)] = Link(self.nodes[con[0]], self.nodes[con[1]], int(inn))
            self.links[int(inn)].weight = link_data["weight"]
            self.links[int(inn)].recur = link_data["recurrent"]
            self.links[int(inn)].enabled = link_data["enabled"]

    def export_json(self, filename):
        import json
        with open(filename, 'w') as f:
            json.dump(self.serialize(), f, indent=2)

    def export_pickle(self, filename):
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.serialize(), f)

    def import_json(self, filename):
        import json
        with open(filename, 'r') as f:
            self.deserialize(json.load(f))

    def import_pickle(self, filename):
        import pickle
        with open(filename, 'rb') as f:
            self.deserialize(pickle.load(f))

    def __str__(self):
        return str(self.links) + "\n" + str(self.nodes)
