__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 07/09/2015'

import os
import random

from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from RelevanceAssessment import *
from ..utils.UMath import *


class Classifier:
    #LABELS = ["1", "3", "*", "#"]
    LABELS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#"]

    def __init__(self):
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

    def get_samples(self, collection, k=1):
        if k != 1:
            random.shuffle(collection)

        sub_samples = np.split(np.array(collection), k)
        return sub_samples

    def get_training_set(self, samples):
        training_set = self.get_new_data_set()

        for sample in samples:
            for data_points in sample:
                for data_point in data_points:
                    training_set.addSample(data_point["values"], self.classes[data_point["label"]])

        return training_set

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

    def train_model(self, iteration=100, training_set=None):
        training_set = self.get_samples(self.collection) if training_set is None else training_set
        data_set = self.get_training_set(training_set)
        trainer = self.get_new_trainer(data_set)

        for i in range(0, iteration):
            error = trainer.train()
            print "Training {}/{} -> error: {}".format(i + 1, iteration, error)

            self.relevance.update_training(error)

        self.serialize("neural_net.xml")

    def evaluate(self, evaluation_set=None):
        evaluation_set = self.collection if evaluation_set is None else evaluation_set
        data_set = self.get_evaluation_set(evaluation_set)

        for key, sample in data_set.iteritems():
            self.deserialize("neural_net.xml")

            predictions = self.get_predictions(sample)

            predicted_label = self.get_label_from_binary_position(np.argmax(predictions))
            expected_label = key[key.find(":") + 1:]

            self.relevance.update_evaluation(predicted_label, expected_label, predictions)

        self.relevance.compute(len(data_set))

    def k_fold_cross_validate(self, k=10, iteration=1):
        samples = self.get_samples(self.collection, k)

        for i in range(0, k):
            print "Cross-validation {}/{}".format(i + 1, k)

            evaluation_set = samples[i]
            training_set = samples[:i] + samples[i + 1:]

            self.train_model(iteration, training_set)
            self.evaluate(evaluation_set)

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