__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 13/09/2015'

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SequentialDataSet
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.structure import *
from Classifier import *


class Recurrent(Classifier):
    def build_neural_net(self, multi_hidden_layers=False):
        input_number, output_number = self.meta_data

        if not multi_hidden_layers:
            self.neural_net = buildNetwork(input_number, 9, len(self.LABELS), hiddenclass=LSTMLayer, recurrent=True, outputbias=False)
        else:
            input = LinearLayer(input_number)
            output = LinearLayer(len(self.LABELS))
            lstm1 = LSTMLayer(5)
            lstm2 = LSTMLayer(9)

            self.neural_net = RecurrentNetwork()
            self.neural_net.addInputModule(input)
            self.neural_net.addModule(lstm1)
            self.neural_net.addModule(lstm2)
            self.neural_net.addOutputModule(output)

            self.neural_net.addConnection(FullConnection(input, lstm1))
            self.neural_net.addConnection(FullConnection(lstm1, lstm2))
            self.neural_net.addConnection(FullConnection(lstm2, output))
            self.neural_net.sortModules()

    def get_new_data_set(self):
        input_number, output_number = self.meta_data

        return SequentialDataSet(input_number, len(self.LABELS))

    def get_new_trainer(self, data_set):
        if not self.neural_net:
            self.build_neural_net()

        return RPropMinusTrainer(self.neural_net, dataset=data_set)
