import numpy as np
import time
import glob
"""
Postprocessing the graph evolved by CGP.
- Simplify the obtained math formula.
- Visualize the expression tree corresponding to the formula that is embedded in the CGP graph.
"""


def get_nodes_array(individual):
    # input1, input2, output, weight, func
    arr = []
    for pos, node in enumerate(individual.nodes):
        if node.active:
            arr.append([node.input[0], node.input[1], node.output, node.weight, node.func, pos])
    return np.array(arr)


def save(individual):
    arr = get_nodes_array(individual)

    num = len(glob.glob("../models/*.npy"))
    # a = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    # np.save("../models/" + a + ".npy", arr)
    np.save("../models/arr"+str(num)+".npy", arr)
    print("save successfully")


def load():
    arr = np.load("../models/arr1.npy")
    num = glob.glob("../models/*.npy")
    # print(arr)
    print(num)


load()