__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 07/09/2015'

import numpy as np
import os

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import *


class Classifier:
    LABELS = ["1", "3", "*", "#"]
    #["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#"]

    def __init__(self):
        self.classes = self.get_binary_classes(self.LABELS)
        self.data_set = None
        self.input_number = None
        self.output_number = None
        self.neural_net = None

    def build_data_set(self, data_path):
        for entry in os.listdir(data_path):
            if entry.find(".data") != -1:
                file_path = "{}{}".format(data_path, entry)
                self.consume(file_path)

    def consume(self, file_path):
        data = open(file_path, 'r')

        if not self.data_set:
            self.input_number, self.output_number = self.get_data_set_metadata(data)
            self.data_set = SupervisedDataSet(self.input_number, self.output_number)
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

    def train_model(self, iteration=100):
        self.neural_net = buildNetwork(self.input_number, 3, self.output_number, bias=True, hiddenclass=TanhLayer)
        trainer = BackpropTrainer(self.neural_net, self.data_set)

        for i in range(0, iteration):
            error = trainer.train()
            print "Training {}/{} -> error: {}".format(i + 1, iteration, error)

    def evaluate(self, path):
        data = open(path, 'r')

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

        for key, value in samples.iteritems():
            prediction = self.neural_net.activate(value)
            predicted_label = self.get_label_from_binary_position(np.argmax(prediction))
            expected_label = key[key.find(":") + 1:]

            print "Predict: {}, expected: {}".format(predicted_label, expected_label)

    def get_data_set_metadata(self, data):
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

        return (input_counter / output_counter), len(labels)

    def get_binary_classes(self, label_set):
        classes = {}
        length = len(label_set)

        for i in range(0, length):
            bin_classes = np.zeros(length, dtype=np.int8)
            bin_classes[i] = 1
            classes[label_set[i]] = bin_classes

        return classes

    def get_label_from_binary_position(self, index):
        for key, value in self.classes.iteritems():
            if value[index]:
                return key
