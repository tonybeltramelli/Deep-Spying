#!/usr/bin/env python
__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

import sys

from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *
from modules.label.Label import *
from modules.feature.FeatureExtractor import *
from modules.classification.classifier.Recurrent import *


class Main:
    def __init__(self, run_name=""):
        self.run_name = "_" + run_name
        self.view = View(False, False, "paper")

    def process_all(self):
        for entry in os.listdir(Path.RAW_PATH):
            if entry.find("e.csv") != -1:
                session_id = entry[:entry.find("_")]
                self.process(session_id)

    def process(self, session_id):
        data_path = Path.get_path(Path.RAW_PATH, session_id)
        output_path = Path.get_path(Path.FEATURE_PATH, session_id)

        label = Label(data_path)
        gyroscope = Gyroscope(data_path, self.view)
        accelerometer = Accelerometer(data_path, self.view)
        accelerometer.fit(gyroscope.timestamp)

        feature_extractor = FeatureExtractor(output_path, self.view, use_statistical_features=False)

        if label.has_label:
            feature_extractor.segment_from_labels([gyroscope, accelerometer], label)
        else:
            feature_extractor.segment_heuristically(gyroscope.get_mean_signal(), [gyroscope, accelerometer])

    def get_classifier(self, iteration, neurons_per_layer):
        print "Train for {} iterations with {} neurons ({} layers)".format(iteration, neurons_per_layer, len(neurons_per_layer))

        classifier = Recurrent(neurons_per_layer)
        classifier.retrieve_samples(Path.FEATURE_PATH)

        return classifier

    def train(self, iteration=100, neurons_per_layer=[9]):
        classifier = self.get_classifier(iteration, neurons_per_layer)

        classifier.train_model(iteration)
        classifier.relevance.output_least_square_mean_errors("{}errors{}.png".format(Path.RESULT_PATH, self.run_name))

    def evaluate(self):
        classifier = Recurrent()
        classifier.retrieve_samples(Path.FEATURE_PATH)

        classifier.evaluate()
        classifier.relevance.output_confusion_matrix("{}confusion_matrix{}.png".format(Path.RESULT_PATH, self.run_name))
        classifier.relevance.output_statistics("{}statistics.md".format(Path.RESULT_PATH), self.run_name)

    def cross_validation(self, iteration=30, neurons_per_layer=[9]):
        classifier = self.get_classifier(iteration, neurons_per_layer)

        classifier.k_fold_cross_validate(10, iteration)
        classifier.relevance.output_confusion_matrix("{}confusion_matrix{}.png".format(Path.RESULT_PATH, self.run_name))
        classifier.relevance.output_statistics("{}statistics.md".format(Path.RESULT_PATH), self.run_name)
        classifier.relevance.output_compared_plot("{}progression{}.png".format(Path.RESULT_PATH, self.run_name))

if __name__ == "__main__":
    argv = sys.argv[1:]
    length = len(argv)

    if length < 1:
        print "Error: no argument supplied"
        print "Usage: "
        print "     main.py <mode> <run name> <args ...>"
    else:
        mode = argv[0]

        if mode == "process":
            main = Main()
            if length == 2:
                main.process(argv[1])
            else:
                main.process_all()
        else:
            main = Main(argv[1])

            if mode == "train":
                if length == 3:
                    main.train(int(argv[2]))
                elif length > 3:
                    main.train(int(argv[2]), [int(x) for x in argv[3:]])
                else:
                    main.train()
                main.evaluate()
            elif mode == "validate":
                if length == 3:
                    main.cross_validation(int(argv[2]))
                elif length > 3:
                    main.cross_validation(int(argv[2]), [int(x) for x in argv[3:]])
                else:
                    main.cross_validation()
