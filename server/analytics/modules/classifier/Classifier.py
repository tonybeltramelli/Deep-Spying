__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 07/09/2015'

import numpy as np

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import *

class Classifier:

    def __init__(self, path):
        data = open("{}samples.data".format(path), 'r')

        #self.labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#"]

        input_number, output_number, labels = self.get_dataset_metadata(data)

        self.classes = self.get_binary_class(labels)

        self.data_set = SupervisedDataSet(input_number, output_number)
        self.build_dataset(data, labels)

        self.neural_net = buildNetwork(input_number, 2, output_number, bias=True, hiddenclass=TanhLayer)
        self.train_model()

    def train_model(self, iteration=100):
        trainer = BackpropTrainer(self.neural_net, self.data_set)

        for i in range(0, iteration):
            error = trainer.train()
            print "Training {}/{} -> error: {}".format(i, iteration, error)

    def evaluate(self, path):
        data = open("{}samples.data".format(path), 'r')

        samples = {}
        values = []
        expected_label = ""

        for line in data:
            line = line.rstrip()

            if line.find(":") != -1:
                expected_label = line[line.find(":") + 1:]
            elif line.find(".") != -1:
                values.append(float(line))
            else:
                samples[expected_label] = values
                values = []

        for key, value in samples.iteritems():
            prediction = self.neural_net.activate(value)
            print "Predict: {}, expected: {}".format(prediction, self.classes[key])

    def build_dataset(self, data, labels):
        data.seek(0)

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

    def get_dataset_metadata(self, data):
        input_counter = 0
        output_counter = 0
        labels = []

        for line in data:
            line = line.rstrip()

            if line.find(":") != -1:
                output_counter += 1
                labels.append(line[line.find(":") + 1:])
            elif line.find(".") != -1:
                input_counter += 1

        labels = list(set(labels))

        return (input_counter / output_counter), len(labels), labels

    def get_binary_class(self, label_set):
        classes = {}
        length = len(label_set)

        for i in range(0, length):
            bin_classes = np.zeros(length, dtype=np.int8)
            bin_classes[i] = 1
            classes[label_set[i]] = bin_classes

        return classes
    