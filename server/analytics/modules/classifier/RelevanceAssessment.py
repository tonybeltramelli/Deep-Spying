__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 16/09/2015'

from ..utils.UMath import *

import collections


class RelevanceAssessment:
    def __init__(self, labels):
        self.collection_size = 0
        self.positives = None
        self.negatives = None
        self.reliabilities = None

        self.total_f1_score = []
        self.total_precision = []
        self.total_recall = []
        self.total_reliability = []

        self.confusion_matrix = self.build_confusion_matrix(labels)

    def new_assessment(self, collection_size):
        self.collection_size = collection_size
        self.positives = []
        self.negatives = []
        self.reliabilities = []

    def update(self, predicted_label, expected_label, predictions):
        self.confusion_matrix[expected_label][predicted_label] += 1

        if predicted_label == expected_label:
            self.positives.append(expected_label)
        else:
            self.negatives.append(expected_label)

        self.reliabilities.append(UMath.reliability([x / sum(predictions) for x in predictions]))

        print "predict: {}, expect: {} {}".format(predicted_label, expected_label, "OK" if predicted_label == expected_label else "")

    def compute(self):
        true_positives = float(len(self.positives))
        false_negatives = self.get_false_positives(self.negatives, self.positives)

        precision = true_positives / self.collection_size
        recall = true_positives / UMath.get_denominator(true_positives + false_negatives)
        f1_score = 2 * (precision * recall) / UMath.get_denominator(precision + recall)
        reliability = np.mean(self.reliabilities)

        print "f1_score: {} (precision: {}, recall: {}), reliability: {}".format(f1_score, precision, recall, reliability)

        self.total_f1_score.append(f1_score)
        self.total_precision.append(precision)
        self.total_recall.append(recall)
        self.total_reliability.append(reliability)

    def output_statistics(self, title, path):
        output_file = open(path, 'a')
        output_file.write("#{} \n".format(title))

        output_file.write("* F1 score: {}\n".format(self.get_statistics(self.total_f1_score)))
        output_file.write("* Precision: {}\n".format(self.get_statistics(self.total_precision)))
        output_file.write("* Recall: {}\n".format(self.get_statistics(self.total_recall)))
        output_file.write("* Reliability: {}\n".format(self.get_statistics(self.total_reliability)))

        output_file.write("\n")
        output_file.close()

    def get_statistics(self, data):
        min = np.amin(data)
        max = np.amax(data)
        mean = np.mean(data)
        stddev = np.std(data)

        return "min: {}, max: {}, mean: {}, stddev: {}".format(min, max, mean, stddev)

    def get_false_positives(self, negatives, true_positives):
        unique_false_negatives = set(true_positives) & set(negatives)
        false_negatives = 0

        for x in unique_false_negatives:
            for y in negatives:
                if x == y:
                    false_negatives += 1

        return float(false_negatives)

    def get_confusion_matrix(self):
        matrix = self.convert_to_matrix(self.confusion_matrix)
        return UMath.normalize_array(matrix)

    def build_confusion_matrix(self, label_set):
        expected_labels = collections.OrderedDict()

        for expected_label in label_set:
            expected_labels[expected_label] = collections.OrderedDict()

            for predicted_label in label_set:
                expected_labels[expected_label][predicted_label] = 0.0

        return expected_labels

    def convert_to_matrix(self, dictionary):
        length = len(dictionary)
        confusion_matrix = np.zeros((length, length))

        i = 0
        for row in dictionary:
            j = 0
            for column in dictionary:
                confusion_matrix[i][j] = dictionary[row][column]
                j += 1
            i += 1

        return confusion_matrix