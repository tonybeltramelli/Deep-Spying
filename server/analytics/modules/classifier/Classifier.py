__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 07/09/2015'

import numpy as np
import os
import random

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
        self.neural_net = None
        self.errors = None
        self.relevance = RelevanceAssessment(self.LABELS)
        self.collection = []
        self.meta_data = None

    def retrieve_samples(self, data_path):
        self.collection = []
        input_number = 0
        labels = []

        for entry in os.listdir(data_path):
            if entry.find(".data") != -1:
                file_path = "{}{}".format(data_path, entry)
                data = open(file_path, 'r')

                label = ""
                data_points = None

                for line in data:
                    line = line.rstrip()

                    if line.find(":") != -1:
                        label = line[line.find(":") + 1:]
                        labels.append(label)

                        if data_points:
                            self.collection.append(data_points)
                        data_points = []
                    elif line.find(".") != -1:
                        values = line.split(",")
                        data_points.append({"values": values, "label": label})

                        if input_number == 0:
                            input_number = len(values)

                if data_points and len(data_points) > 0:
                    self.collection.append(data_points)

        output_number = len(list(set(labels)))

        self.meta_data = (input_number, output_number)

    def get_data_sets(self, collection, k=1):
        if k != 1:
            random.shuffle(collection)

        data_set = [k]
        sub_samples = np.split(np.array(collection), k)

        for i in range(0, k):
            sample = sub_samples[i]
            training_set = self.get_training_set()

            for data_points in sample:
                for data_point in data_points:
                    training_set.addSample(data_point["values"], self.classes[data_point["label"]])

            data_set[i] = training_set

        return data_set

    def get_evaluation_set(self, sample):
        evaluation_set = {}
        index = 0

        for data_points in sample:
            index += 1
            expected_label = "{}:{}".format(index, data_points[0]["label"])
            evaluation_set[expected_label] = []

            for data_point in data_points:
                evaluation_set[expected_label].append(data_point["values"])

        return evaluation_set

    def train_model(self, iteration=2):
        training_set = self.get_training_set()

        for data_points in self.collection:
            for data_point in data_points:
                training_set.addSample(data_point["values"], self.classes[data_point["label"]])

        trainer = self.get_trainer(training_set)
        self.errors = np.zeros(iteration)

        for i in range(0, iteration):
            error = trainer.train()
            print "Training {}/{} -> error: {}".format(i + 1, iteration, error)
            self.errors[i] = error

        self.serialize("neural_net.xml")

    def evaluate(self):
        data_set = self.get_evaluation_set(self.collection)

        self.relevance.new_assessment(len(data_set))

        for key, sample in data_set.iteritems():
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

    def train_and_evaluate_k_fold_cross_validate(self, k=10):
        data_sets = self.get_data_sets(k)

        for i in range(0, k):
            print i

    def output_least_square_mean_errors(self, path):
        self.view.plot_data("Training", self.errors, "Iteration", "Least square mean error")
        self.view.show()
        self.view.save(path)

    def output_confusion_matrix(self, path):
        matrix = self.relevance.get_confusion_matrix()

        self.view.plot_confusion_matrix(matrix, self.LABELS)
        self.view.show()
        self.view.save(path)

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