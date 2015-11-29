__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 07/09/2015'

import os
import random
import collections

from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from RelevanceAssessment import *
from ..utils.UMath import *


class Classifier:
    LABELS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#"]

    def __init__(self):
        self.classes = self.get_binary_classes(self.LABELS)
        self.neural_net = None
        self.errors = None
        self.relevance = RelevanceAssessment(self.LABELS)
        self.collection = []
        self.meta_data = None

    def retrieve_samples(self, data_path):
        for entry in os.listdir(data_path):
            if entry.find(".data") != -1:
                self.retrieve_sample("{}{}".format(data_path, entry))

    def retrieve_sample(self, file_path, is_labelled=True):
        data = open(file_path, 'r')

        label = ""
        data_points = None

        for line in data:
            line = line.rstrip()

            if line.find(":") != -1:
                if is_labelled:
                    label = line[line.find(":") + 1:]
                        
                if data_points:
                    self.collection.append(data_points)
                data_points = []
            elif line.find(".") != -1:
                values = line.split(",")

                if is_labelled:
                    data_points.append({"values": values, "label": label})
                else:
                    data_points.append({"values": values})

                if self.meta_data is None:
                    input_number = len(values)
                    self.meta_data = (input_number, len(self.LABELS))

        if data_points and len(data_points) > 0:
            self.collection.append(data_points)

    def get_samples(self, collection, k=1):
        if k != 1:
            random.shuffle(collection)

        last_sample = None
        length = len(collection)
        m = length % k
        if m != 0:
            last_sample = collection[length - m:]
            samples = collection[:length - m]
        else:
            samples = collection

        sub_samples = np.split(np.array(samples), k)

        if last_sample is not None:
            sub_samples.append(np.array(last_sample))

        return sub_samples

    def get_training_set(self, samples):
        training_set = self.get_new_data_set()

        for sample in samples:
            for data_points in sample:
                for data_point in data_points:
                    training_set.addSample(data_point["values"], self.classes[data_point["label"]])

        return training_set

    def get_evaluation_set(self, sample, is_labelled=True):
        evaluation_set = collections.OrderedDict()
        index = 0

        for data_points in sample:
            index += 1
            if is_labelled:
                expected_label = "{}:{}".format(index, data_points[0]["label"])
            else:
                expected_label = "{}".format(index)

            evaluation_set[expected_label] = []

            for data_point in data_points:
                evaluation_set[expected_label].append(data_point["values"])

        return evaluation_set

    def train_model(self, iteration=100, training_set=None):
        training_set = self.get_samples(self.collection) if training_set is None else training_set
        data_set = self.get_training_set(training_set)
        trainer = self.get_new_trainer(data_set)

        print "Train for {} iterations".format(iteration)

        min_loss = 1.0

        for i in range(0, iteration):
            error = trainer.train()
            print "Training {}/{} -> error: {}".format(i + 1, iteration, error)

            self.relevance.update_training(error)

            if error < min_loss:
                min_loss = error
                self.serialize("neural_net.xml")

        print "Minimum loss: {}".format(min_loss)

    def evaluate(self, evaluation_set=None, is_labelled=True):
        evaluation_set = self.collection if evaluation_set is None else evaluation_set
        data_set = self.get_evaluation_set(evaluation_set, is_labelled)

        for key, sample in data_set.iteritems():
            self.deserialize("neural_net.xml")

            predictions = self.get_predictions(sample)
            predicted_label = self.get_label_from_binary_position(np.argmax(predictions))
            
            if is_labelled:
                expected_label = key[key.find(":") + 1:]
                self.relevance.update_evaluation(predicted_label, expected_label, predictions)
            else:
                print "predict: {}".format(predicted_label)

        if is_labelled:
            self.relevance.compute(len(data_set))

    def k_fold_cross_validate(self, k=5, iteration=1):
        samples = self.get_samples(self.collection, k)

        for i in range(0, k):
            print "Cross-validation {}/{}".format(i + 1, k)

            evaluation_set = samples[i]
            training_set = samples[:i] + samples[i + 1:]

            self.neural_net = None
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
