__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 13/09/2015'

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SequentialDataSet
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.structure.modules import *
from Classifier import *
from ..utils.UMath import *


class Recurrent(Classifier):
    def build(self, data):
        input_number, output_number = self.get_data_set_metadata(data)

        self.data_set = SequentialDataSet(3, len(self.LABELS))
        self.neural_net = buildNetwork(3, 5, len(self.LABELS), hiddenclass=LSTMLayer, recurrent=True, outputbias=False)

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

        positives = []
        negatives = []
        reliabilities = []

        predicted_labels = []
        expected_labels = []

        for key, sample in samples.iteritems():
            self.deserialize("neural_net.xml")

            predictions = np.zeros(len(self.LABELS))
            for values in sample:
                prediction = self.neural_net.activate(values)
                predictions = [sum(x) for x in zip(predictions, prediction)]

            predictions = [UMath.normalize(0, 1, x, min(predictions), max(predictions)) for x in predictions]

            predicted_label = self.get_label_from_binary_position(np.argmax(predictions))
            expected_label = key[key.find(":") + 1:]

            predicted_labels.append(predicted_label)
            expected_labels.append(expected_label)

            if predicted_label == expected_label:
                positives.append(expected_label)
            else:
                negatives.append(expected_label)

            reliabilities.append(UMath.get_reliability([x / sum(predictions) for x in predictions]))

            print "predict: {}, expect: {} {}".format(predicted_label, expected_label, "OK" if predicted_label == expected_label else "")

        true_positives = float(len(positives))
        false_negatives = float(len(set(positives) & set(negatives)))

        precision = true_positives / len(samples)
        recall = true_positives / (true_positives + false_negatives)
        f1_score = 2 * (precision * recall) / UMath.get_denominator(precision + recall)
        reliability = sum(reliabilities) / len(reliabilities)

        print "f1_score: {} (precision: {}, recall: {}), reliability: {}".format(f1_score, precision, recall, reliability)

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
