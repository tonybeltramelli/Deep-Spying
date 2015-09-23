__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 22/09/2015'

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import *
from Classifier import *


class FeedForward(Classifier):
    def build_neural_net(self):
        input_number, output_number = self.meta_data

        self.neural_net = buildNetwork(input_number, 5, output_number, bias=True, hiddenclass=TanhLayer)

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


