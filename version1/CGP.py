import copy
import random

from settings import COL, LEVEL_BACK
import operator as op


class Node:
    def __init__(self, arity):
        self.input = [0] * arity
        self.weight = [0.0] * arity
        self.func = None  # function in function set
        # function_set_order = [op.add, op.sub, op.mul, op.truediv]
        self.output = None
        self.active = False

    def calculate_output(self, input1, input2):
        if self.func == 0:
            self.output = input1 + input2
        if self.func == 1:
            self.output = input1 * input2
        if self.func == 2:
            self.output = input1 - input2
        if self.func == 3:
            self.output = op.truediv(input1, input2)


class Individual:
    function_set = []  # operator
    weight_range = [-1, 1]
    arity = 2
    n_inputs = 2
    n_outputs = 1
    col = COL
    level_back = LEVEL_BACK  # control depth

    def __init__(self):
        self.nodes = []
        self.score = 0

        for pos in range(COL):
            self.nodes.append(self._random_node(pos))

        # output node should be active
        self.nodes[len(self.nodes) - 1].active = True
        self._active_determined = False

    def _random_node(self, pos):
        node = Node(self.arity)
        node.func = random.randint(0, 3)  # len(self.function_set) - 1
        for i in range(self.arity):
            node.input[i] = random.randint(max(pos - self.level_back, -self.n_inputs), pos - 1)
            if node.input[i] == pos:
                node.input[i] = pos + 1
            node.weight[i] = random.uniform(self.weight_range[0], self.weight_range[1])
        node.output = pos
        return node

    def find_active_node(self):
        active_num = 0
        for node in reversed(self.nodes):
            if node.active:
                active_num += 1
                for i in range(self.arity):
                    if node.input[i] >= 0:
                        self.nodes[node.input[i]].active = True

        # print("active nodes: ", active_num)

    def eval(self, *args):
        if not self._active_determined:
            self.find_active_node()
            self._active_determined = True

        for node in self.nodes:
            if node.active:
                inputs = []
                for i in range(self.arity):
                    w = node.weight[i]
                    if node.input[i] < 0:
                        inputs.append(args[-node.input[i] - 1] * w)
                    else:
                        inputs.append(self.nodes[node.input[i]].output * w)
                node.calculate_output(inputs[0], inputs[1])
        return self.nodes[-1].output

    def mutate(self, mutate_rate=0.02):
        """
        Mutate this individual. Each gene is varied with probability *mut_rate*.
        :param mutate_rate: mutation probability
        :return a child after mutation
        """
        child = copy.deepcopy(self)
        for pos, node in enumerate(child.nodes):
            if random.random() < mutate_rate:
                node.func = random.randint(0, 3)
            for i in range(child.arity):
                if random.random() < mutate_rate:
                    node.input[i] = random.randint(max(pos - self.level_back, -self.n_inputs), pos - 1)
                    node.weight[i] = random.uniform(self.weight_range[0], self.weight_range[1])
            # initialize the active
            node.active = False
        self.nodes[len(self.nodes) - 1].active = True
        self._active_determined = False
        return child


def evolve(pop, mutate_rate, mu, lambda_):
    """
    :param pop: populations of the parents
    :param mutate_rate: default rate is 0.02 in function mutate
    :param mu: select the size of parents who behave better
    :param lambda_: size of the mutated children
    :return: a new populations
    """
    pop = sorted(pop, key=lambda individual: individual.score)
    parents = pop[-mu:]
    print(parents[-1].score)
    # generate lambda new children via mutation
    offspring = []
    for i in range(lambda_):
        parent = random.choice(parents)
        offspring.append(parent.mutate(mutate_rate))
    return parents + offspring


def create_pop(n):
    return [Individual() for _ in range(n)]
