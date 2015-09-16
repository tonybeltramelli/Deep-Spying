__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 07/09/2015'

import numpy as np
import os

from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from ..View import *
from RelevanceAssessment import *
from ..utils.UMath import *


class Classifier:
    #LABELS = ["1", "3", "*", "#"]
    LABELS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#"]

    def __init__(self):
        self.view = View(False, True)
        self.classes = self.get_binary_classes(self.LABELS)
        self.data_set = None
        self.neural_net = None
        self.errors = None
        self.relevance = RelevanceAssessment()

    def build_data_set(self, data_path):
        for entry in os.listdir(data_path):
            if entry.find(".data") != -1:
                file_path = "{}{}".format(data_path, entry)
                data = open(file_path, 'r')

                if not self.data_set:
                    self.build(data)
                    data.seek(0)

                self.parse(data)

    def train_model(self, iteration=50):
        trainer = self.get_trainer()
        self.errors = np.zeros(iteration)

        for i in range(0, iteration):
            error = trainer.train()
            trainer.trainEpochs()
            print "Training {}/{} -> error: {}".format(i + 1, iteration, error)
            self.errors[i] = error

        self.serialize("neural_net.xml")

    def output_weighted_mean_errors(self, path):
        self.view.plot_data("Training", self.errors, "Iteration", "Weighted mean error")
        self.view.show()
        self.view.save(path)

    def output_confusion_matrix(self, path):
        matrix = self.relevance.get_confusion_matrix()

        self.view.plot_confusion_matrix(matrix, self.LABELS)
        self.view.show()
        self.view.save(path)

    def get_data_set_metadata(self, data):
        input_number = 0
        labels = []

        for line in data:
            line = line.rstrip()

            if line.find(":") != -1:
                labels.append(line[line.find(":") + 1:])
            elif line.find(",") != -1 and input_number == 0:
                input_number = line.count(",") + 1

        output_number = len(list(set(labels)))

        return input_number, output_number

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