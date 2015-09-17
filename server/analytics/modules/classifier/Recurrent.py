__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 13/09/2015'

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SequentialDataSet
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.structure.modules import *
from Classifier import *


class Recurrent(Classifier):
    def build(self, data):
        input_number, output_number = self.get_data_set_metadata(data)

        self.data_set = SequentialDataSet(input_number, len(self.LABELS))
        self.neural_net = buildNetwork(input_number, 9, len(self.LABELS), hiddenclass=LSTMLayer, recurrent=True, outputbias=False)

    def parse(self, data):
        label = ""

        for line in data:
            line = line.rstrip()

            if line.find(":") != -1:
                label = line[line.find(":") + 1:]
            elif line.find(".") != -1:
                values = line.split(",")
                self.data_set.addSample(values, self.classes[label])

    def get_trainer(self):
        return RPropMinusTrainer(self.neural_net, dataset=self.data_set)

    def evaluate(self, path):
        data = open(path, 'r')
        samples = self.get_samples(data)

        self.relevance.new_assessment(len(samples))

        for key, sample in samples.iteritems():
            self.deserialize("neural_net.xml")

            predictions = np.zeros(len(self.LABELS))
            for values in sample:
                prediction = self.neural_net.activate(values)
                predictions = [sum(x) for x in zip(predictions, prediction)]

            predictions = UMath.normalize_array(predictions)

            predicted_label = self.get_label_from_binary_position(np.argmax(predictions))
            expected_label = key[key.find(":") + 1:]

            self.relevance.update(predicted_label, expected_label, predictions)

        self.relevance.compute()

    def get_samples(self, data):
        samples = {}
        expected_label = ""
        index = 0

        for line in data:
            line = line.rstrip()

            if line.find(":") != -1:
                index += 1
                expected_label = "{}:{}".format(index, line[line.find(":") + 1:])
                samples[expected_label] = []
            elif line.find(".") != -1:
                values = line.split(",")
                samples[expected_label].append(values)

        return samples
