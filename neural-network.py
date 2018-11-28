import numpy as np


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1.0 - x)


class NeuralNetwork:
    def __init__(self, input_size, output_size):
        self.weights1 = np.random.uniform(
            low=-4.0, high=4.0, size=(input_size, input_size))

        self.weights2 = np.random.uniform(
            low=-4.0, high=4.0, size=(input_size, output_size))
        # print(self.weights2)
        self.output = np.zeros(output_size)

    def feedforward(self, input_array):
        self.layer1 = sigmoid(np.dot(input_array, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))
        # print(self.layer1)
        return self.output


if __name__ == "__main__":
    for i in range(200):
        nn = NeuralNetwork(12, 2)
        print(nn.feedforward([0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]).round())
