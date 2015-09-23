__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 23/09/2015'

from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules.svmunit import SVMUnit
from pybrain.supervised.trainers.svmtrainer import SVMTrainer
from Classifier import *


class SVM(Classifier):
    def name(self):
        return "Support Vector Machine"

    def build_neural_net(self):
        self.neural_net = SVMUnit()

    def get_new_data_set(self):
        input_number, output_number = self.meta_data

        return ClassificationDataSet(input_number, output_number)

    def get_new_trainer(self, data_set):
        if not self.neural_net:
            self.build_neural_net()

        return SVMTrainer(self.neural_net, data_set)

    def get_predictions(self, input_values):
        return self.neural_net.forwardPass(input_values[0])
