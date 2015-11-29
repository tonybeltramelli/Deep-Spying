#!/usr/bin/env python
__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

import sys

from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *
from modules.label.Label import *
from modules.feature.FeatureExtractor import *
from modules.classification.Recurrent import *


class Main:
    def __init__(self, run_name="", use_statistical_features=False, preprocess_signal=True, use_heuristic_segmentation=False):
        self.run_name = "_" + run_name
        self.view = View(False, False, "paper")
        self.use_statistical_features = use_statistical_features
        self.preprocess_signal = preprocess_signal
        self.use_heuristic_segmentation =  use_heuristic_segmentation

    def process_all(self, sensors="ga", merge_axes={"g": False, "a": False}):
        for entry in os.listdir(Path.RAW_PATH):
            if entry.find("e.csv") != -1:
                session_id = entry[:entry.find("_")]
                self.process(session_id, sensors, merge_axes)

    def process(self, session_id, sensors="ga", merge_axes={"g": False, "a": False}):
        data_path = Path.get_path(Path.RAW_PATH, session_id) + "_"
        output_path = Path.get_path(Path.FEATURE_PATH, session_id)

        label = Label(data_path)

        gyroscope = Gyroscope(data_path, self.view, merge_axes["g"], preprocess_signal=self.preprocess_signal)
        accelerometer = Accelerometer(data_path, self.view, merge_axes["a"], preprocess_signal=self.preprocess_signal)
        accelerometer.fit(gyroscope.timestamp)

        feature_extractor = FeatureExtractor(output_path, self.view, use_statistical_features=self.use_statistical_features)

        fusion = []
        for sensor in sensors:
            if sensor == 'g':
                fusion.append(gyroscope)
            if sensor == 'a':
                fusion.append(accelerometer)

        if not self.use_heuristic_segmentation:
            if label.has_label:
                feature_extractor.segment_from_labels(fusion, label)
            else:
                feature_extractor.segment_heuristically(fusion, gyroscope.get_mean_signal())
        else:
            feature_extractor.segment_heuristically(fusion, gyroscope.get_mean_signal(), label)

    def get_classifier(self, neurons_per_layer):
        classifier = Recurrent(neurons_per_layer)
        classifier.retrieve_samples(Path.FEATURE_PATH)

        return classifier

    def train(self, iteration=100, neurons_per_layer=[128, 128]):
        classifier = self.get_classifier(neurons_per_layer)

        classifier.train_model(iteration)
        classifier.relevance.output_mean_square_mean_error("{}errors{}.png".format(Path.RESULT_PATH, self.run_name))

    def evaluate(self):
        classifier = Recurrent()
        classifier.retrieve_samples(Path.FEATURE_PATH)

        classifier.evaluate()
        classifier.relevance.output_confusion_matrix("{}confusion_matrix{}.png".format(Path.RESULT_PATH, self.run_name))
        classifier.relevance.output_statistics("{}statistics.md".format(Path.RESULT_PATH), self.run_name)

    def cross_validation(self, iteration=100, neurons_per_layer=[128, 128], k=5):
        classifier = self.get_classifier(neurons_per_layer)

        classifier.k_fold_cross_validate(k, iteration)
        classifier.relevance.output_confusion_matrix("{}confusion_matrix{}.png".format(Path.RESULT_PATH, self.run_name))
        classifier.relevance.output_statistics("{}statistics.md".format(Path.RESULT_PATH), self.run_name)
        classifier.relevance.output_mean_square_mean_error("{}error{}.png".format(Path.RESULT_PATH, self.run_name), k)

    def predict(self, session_id):
        self.process(session_id)

        classifier = Recurrent()
        classifier.retrieve_sample("{}{}.data".format(Path.FEATURE_PATH, session_id), is_labelled=False)
        classifier.evaluate(is_labelled=False)

if __name__ == "__main__":
    argv = sys.argv[1:]
    length = len(argv)

    if length < 1:
        print "Error: no argument supplied"
        print "Usage: "
        print "     main.py <mode> <run name> <args ...>"
        print "Examples: "
        print "     main.py process 69141736"
        print "     main.py process ga gyan"
        print "     main.py train dev 10 9"
        print "     main.py validate session1 10 5 9"
        print "     main.py predict 69141736"
        print "     main.py extract y n"
    else:
        mode = argv[0]

        if mode == "process":
            main = Main()
            if length == 2:
                main.process(argv[1])
            elif length > 2:
                s = argv[1]
                m = argv[2]

                a = {"g": False, "a": False}
                for i in xrange(0, len(m), 2):
                    c = m[i] + m[i + 1]
                    sensor = c[0]
                    strategy = c[1]

                    a[sensor] = True if strategy == 'y' else False

                main.process_all(s, a)
            else:
                main.process_all()
        elif mode == "extract":
            statistical = argv[1]
            preprocessing = argv[2]
            heuristic = argv[3]

            use_statistical_features = False
            preprocess_signal = True
            use_heuristic_segmentation = False

            if statistical == 'y':
                use_statistical_features = True

            if preprocessing == 'n':
                preprocess_signal = False

            if heuristic == 'y':
                use_heuristic_segmentation = True

            main = Main(use_statistical_features=use_statistical_features, preprocess_signal=preprocess_signal, use_heuristic_segmentation=use_heuristic_segmentation)
            main.process_all()
        elif mode == "predict" and length == 2:
            main = Main()
            main.predict(argv[1])
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
            elif mode == "evaluate":
                main.evaluate()
