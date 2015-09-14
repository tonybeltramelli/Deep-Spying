__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 07/09/2015'

import numpy as np
import os

from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader


class Classifier:
    #LABELS = ["1", "3", "*", "#"]
    LABELS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#"]

    def __init__(self):
        self.classes = self.get_binary_classes(self.LABELS)
        self.data_set = None
        self.neural_net = None

    def build_data_set(self, data_path):
        for entry in os.listdir(data_path):
            if entry.find(".data") != -1:
                file_path = "{}{}".format(data_path, entry)
                self.consume(file_path)

    def consume(self, file_path):
        data = open(file_path, 'r')

        if not self.data_set:
            self.build(data)
            data.seek(0)

        self.parse(data)

    def train_model(self, iteration=10):
        trainer = self.get_trainer()

        for i in range(0, iteration):
            error = trainer.train()
            trainer.trainEpochs()
            print "Training {}/{} -> error: {}".format(i + 1, iteration, error)

        self.serialize("neural_net.xml")

    def evaluate(self, path):
        data = open(path, 'r')
        samples = self.get_samples(data)

        for key, value in samples.iteritems():
            prediction = self.neural_net.activate(value)
            predicted_label = self.get_label_from_binary_position(np.argmax(prediction))
            expected_label = key[key.find(":") + 1:]

            print "Predict: {}, expected: {} {}".format(predicted_label, expected_label, "OK" if predicted_label == expected_label else "")

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

    def serialize(self, path):
        NetworkWriter.writeToFile(self.neural_net, path)

    def deserialize(self, path):
        self.neural_net = NetworkReader.readFrom(path)