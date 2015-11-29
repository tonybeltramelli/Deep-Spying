__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 16/09/2015'

from ..utils.UMath import *
from ..View import *

import collections


class RelevanceAssessment:
    def __init__(self, labels):
        self.labels = labels
        self.view = View(False, True)

        self.positives = []
        self.negatives = []
        self.reliabilities = []

        self.errors = []

        self.all_f1_score = []
        self.all_precision = []
        self.all_recall = []
        self.all_reliability = []

        self.confusion_matrix = self.build_confusion_matrix(labels)

    def update_training(self, error):
        self.errors.append(error)

    def update_evaluation(self, predicted_label, expected_label, predictions):
        self.confusion_matrix[expected_label][predicted_label] += 1

        if predicted_label == expected_label:
            self.positives.append(expected_label)
        else:
            self.negatives.append(expected_label)

        self.reliabilities.append(UMath.reliability([x / sum(predictions) for x in predictions]))

        print "predict: {}, expect: {} {}".format(predicted_label, expected_label, "OK" if predicted_label == expected_label else "")

    def compute(self, collection_size):
        true_positives = float(len(self.positives))
        false_negatives = self.get_false_positives(self.negatives, self.positives)

        precision = true_positives / collection_size
        recall = true_positives / UMath.get_denominator(true_positives + false_negatives)
        f1_score = 2 * (precision * recall) / UMath.get_denominator(precision + recall)
        reliability = np.mean(self.reliabilities)

        print "f1_score: {} (precision: {}, recall: {}), reliability: {}".format(f1_score, precision, recall, reliability)

        self.all_f1_score.append(f1_score)
        self.all_precision.append(precision)
        self.all_recall.append(recall)
        self.all_reliability.append(reliability)

        self.positives = []
        self.negatives = []
        self.reliabilities = []

    def get_statistics(self, data):
        amin = np.amin(data)
        mean = np.mean(data)
        amax = np.amax(data)
        stddev = np.std(data)

        return "min: {}, mean: {}, max: {}, stddev: {}".format(amin, mean, amax, stddev)

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

    def output_compared_plot(self, path):
        length = len(self.all_f1_score)
        elength = len(self.errors)

        if elength > length:
            ratio = elength / length
            self.all_f1_score = UMath.interpolate(self.all_f1_score, length * ratio)
            self.all_precision = UMath.interpolate(self.all_precision, length * ratio)
            self.all_recall = UMath.interpolate(self.all_recall, length * ratio)
            self.all_reliability = UMath.interpolate(self.all_reliability, length * ratio)

        data = [self.errors, self.all_f1_score, self.all_precision, self.all_recall, self.all_reliability]
        colors = ['m', 'c', 'g', 'b', 'r']
        labels = ["Mean square error", "F1 score", "Precision", "Recall", "Reliability"]

        self.view.plot_data("K-fold cross-validation", data, "Epoch", "Amplitude", colors, labels)
        self.view.show()
        self.view.save(path)

    def output_statistics(self, path, run_name):
        output_file = open(path, 'a')
        output_file.write("#Statistics {}\n".format(run_name))

        output_file.write("* F1 score: {}\n".format(self.get_statistics(self.all_f1_score)))
        output_file.write("* Precision: {}\n".format(self.get_statistics(self.all_precision)))
        output_file.write("* Recall: {}\n".format(self.get_statistics(self.all_recall)))
        output_file.write("* Reliability: {}\n".format(self.get_statistics(self.all_reliability)))
        if len(self.errors) > 0:
            output_file.write("* Mean square error: {}\n".format(self.get_statistics(self.errors)))

        output_file.write("\n")
        output_file.close()

    def output_mean_square_mean_error(self, path, k=1):
        if k > 1:
            step = len(self.errors) / k
            errors = np.zeros(step)

            for i in xrange(0, len(self.errors), step):
                error_run = []

                for j in range(i, i + step):
                    error_run.append(self.errors[j])

                errors = [sum(x) for x in zip(errors, error_run)]

            errors = [x / k for x in errors]
        else:
            errors = self.errors

        self.view.plot_data("Training", [errors], "Epoch", "Mean square error")
        self.view.show()
        self.view.save(path)

    def output_confusion_matrix(self, path):
        matrix = self.get_confusion_matrix()

        self.view.plot_confusion_matrix(matrix, self.labels)
        self.view.show()
        self.view.save(path)