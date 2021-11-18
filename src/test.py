from rtneat import *
# random.seed(0)

nn = Network(2, 1)

nn.add_node()
for i in range(5):
    nn.add_link()

print(nn.links)

X = [-16, 5]

for i in range(5):
    print(nn.feed(X))
