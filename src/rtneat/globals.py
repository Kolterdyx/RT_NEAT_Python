import logging
import random
import numpy as np
from .tags import *

FORMAT = '%(levelname)s [%(asctime)s] %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.setLevel(INFO)


def genetic_comparison(net1, net2):
    net1_data = net1.serialize()
    net2_data = net2.serialize()
    nodes1 = list(net1_data["nodes"].values())
    nodes2 = list(net2_data["nodes"].values())
    links1 = net1_data["links"]
    links2 = net2_data["links"]

    links1inns = sorted(list(links1.keys()))
    links2inns = sorted(list(links2.keys()))

    matching = {}
    disjoint = {}
    excess = {}

    print(links1inns)
    print(links2inns)

    for a,b in zip(links1inns, links2inns):
        if a==b:
            matching[a] = links1[a]
            links1inns.remove(a)
            links2inns.remove(b)

    print(links1inns)
    print(links2inns)




def crossover(net1, net2):
    pass
