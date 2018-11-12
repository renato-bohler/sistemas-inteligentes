import random
from math import exp
from prettytable import PrettyTable

def sigmoid(input):
	try:
		return 1.0 / (1.0 + exp(-input))
	except OverflowError:
		return 0.0

def dsigmoid(input):
	return input * (1.0 - input)

class Node(object):
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias
        self.output = 0
        self.delta = 1

    def __str__(self):
        return f" (weights: {self.weights}, bias: {self.bias}, output: {self.output}, delta: {self.delta}) "

class Network(object):
    def __init__(self, input_nodes, nodes):
        self.input_nodes = input_nodes
        
        last_layer_nodes = input_nodes

        self.layers = list()
        for nodes_qty in nodes:
            layer = list()
            for i in range(nodes_qty):
                layer.append(Node([random.random() for i in range(last_layer_nodes)], random.random()))
            self.layers.append(layer)
            last_layer_nodes = nodes_qty

        self.layers.append([Node([random.random() for i in range(last_layer_nodes)], random.random())])

    def __str__(self):
        output = f"Input layer: {self.input_nodes} nodes"

        for layer in self.layers:
            output += "\n\n"
            output += f"Layer {self.layers.index(layer) + 1}: "
            for node in layer:
                output += Node.__str__(node)

        return output

    def predict(self, inputs):
        if (type(inputs) is not list):
            raise ValueError("Input should be a list")
        if (len(inputs) != self.input_nodes):
            raise ValueError(f"Input should have {self.input_nodes} numbers")

        layer_input = inputs

        for layer in self.layers:
            next_layer_input = list()
            node_output = 0
            for node in layer:
                node_output = node.bias
                for i in range(len(layer_input)):
                    node_output += node.weights[i] * layer_input[i]
                node.output = sigmoid(node_output)
                next_layer_input.append(node.output)
            layer_input = next_layer_input.copy()

        return next_layer_input[0]

    def backpropagate_error(self, expected):
        n_layers = len(self.layers)

        for i in reversed(range(n_layers)):
            layer = self.layers[i]
            n_nodes = len(layer)
            errors = list()

            if i != n_layers - 1:
                for j in range(n_nodes):
                    error = 0.0
                    for node in self.layers[i + 1]:
                        error += (node.weights[j] * node.delta)
                    errors.append(error)
            else:
                for j in range(n_nodes):
                    node = layer[j]
                    errors.append(expected - node.output)
            for j in range(n_nodes):
                node = layer[j]
                node.delta = errors[j] * dsigmoid(node.output)

    def update_weights(self, train_row, learning_rate):
	    for i in range(len(self.layers)):
	    	inputs = train_row['input']
	    	if i != 0:
	    		inputs = [node.output for node in self.layers[i - 1]]
	    	for node in self.layers[i]:
	    		for j in range(len(inputs)):
	    			node.weights[j] += learning_rate * node.delta * inputs[j]
	    		node.weights[-1] += learning_rate * node.delta

    def train(self, train_data, iterations = 1000, learning_rate = 0.5):
        if (type(train_data) is not list):
            raise ValueError("Input should be a list")

        for i in range(iterations):
            for train_row in train_data:
                provided_inputs = train_row['input']
                expected_output = train_row['output']

                if (type(provided_inputs) is not list):
                    raise ValueError("Input should be a list")
                if (len(provided_inputs) != self.input_nodes):
                    raise ValueError(f"Input should have {self.input_nodes} numbers")

                self.predict(provided_inputs)

                self.backpropagate_error(expected_output)
                self.update_weights(train_row, learning_rate)

n_inputs = 2
hidden_layers = [5, 5]

network = Network(n_inputs, hidden_layers)

# XOR
train_data = [
    {
        'input': [0, 0],
        'output': 0
    },
    {
        'input': [0, 1],
        'output': 1
    },
    {
        'input': [1, 0],
        'output': 1
    },
    {
        'input': [1, 1],
        'output': 0
    },
]

network.train(train_data, 10000, 0.75)

t = PrettyTable()
for i in range(n_inputs):
    t.add_column(f"I{i}", [])
t.add_column("Expected", [])
t.add_column("Predicted", [])
for data in train_data:
    row = list()
    for input in data['input']:
        row.append(input)
    row.append(data['output'])
    row.append(network.predict(data['input']))
    t.add_row(row)

print(t)