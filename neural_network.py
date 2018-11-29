import numpy as np


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1.0 - x)


class NeuralNetwork:
    def __init__(self, num_input, num_output):
        self.num_input = num_input
        self.num_output = num_output

    def feedforward(self, input_array, weights):
        weights1 = weights[:self.num_input *
                           self.num_input].reshape(self.num_input, self.num_input)
        weights2 = weights[self.num_input *
                           self.num_input:].reshape(self.num_input, self.num_output)

        self.layer1 = sigmoid(np.dot(input_array, weights1))
        self.output = sigmoid(np.dot(self.layer1, weights2))
        return self.output
