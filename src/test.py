from rtneat import *


# log.setLevel(DEBUG)


# random.seed(1)

nn = Network(2, 1)

nn.add_link(nn.new_link(nn.inodes[0], nn.onodes[0]))

node = nn.add_node()

nn.add_link(nn.new_link(nn.inodes[1], node))

nn.add_link(nn.new_link(node, node))

log.debug(nn.links)

X = [-13, 5]
