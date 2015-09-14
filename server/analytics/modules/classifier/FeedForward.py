__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 13/09/2015'

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import *
from Classifier import *


class FeedForward(Classifier):
    def build(self, data):
        input_number, output_number = self.get_data_set_metadata(data)

        self.data_set = SupervisedDataSet(input_number, output_number)
        self.neural_net = buildNetwork(input_number, 3, output_number, bias=True, hiddenclass=TanhLayer)

    def parse(self, data):
        values = []
        label = ""

        for line in data:
            line = line.rstrip()

            if line.find(":") != -1:
                label = line[line.find(":") + 1:]
            elif line.find(".") != -1:
                values.append(float(line))
            else:
                self.data_set.appendLinked(values, self.classes[label])
                values = []

    def get_trainer(self):
        return BackpropTrainer(self.neural_net, self.data_set)

    def get_samples(self, data):
        samples = {}
        values = []
        expected_label = ""
        index = 0

        for line in data:
            line = line.rstrip()

            if line.find(":") != -1:
                index += 1
                expected_label = "{}:{}".format(index, line[line.find(":") + 1:])
            elif line.find(".") != -1:
                values.append(float(line))
            else:
                samples[expected_label] = values
                values = []

        return samples