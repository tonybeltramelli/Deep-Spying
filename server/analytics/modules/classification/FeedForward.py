__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 22/09/2015'

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from Classifier import *
from ..utils.NeuralNet import *


class FeedForward(Classifier):
    def __init__(self, neurons_per_layer=[9]):
        Classifier.__init__(self)

        self.neurons_per_layer = neurons_per_layer

    def build_neural_net(self):
        input_number, output_number = self.meta_data
        self.neural_net = NeuralNet.get_neural_net(input_number, output_number,
                                                   FeedForwardNetwork, TanhLayer, self.neurons_per_layer)

    def get_new_data_set(self):
        input_number, output_number = self.meta_data

        return SupervisedDataSet(input_number, output_number)

    def get_new_trainer(self, data_set):
        if not self.neural_net:
            self.build_neural_net()

        return BackpropTrainer(self.neural_net, data_set)

    def get_predictions(self, input_values):
        return self.neural_net.activate(input_values[0])

    def get_name(self):
        return "Feed forward network (Backpropagation training)"


