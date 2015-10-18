#!/usr/bin/env python
__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

import sys

from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *
from modules.label.Label import *
from modules.feature.FeatureExtractor import *
from modules.classification.Recurrent import *


class Main:
    def __init__(self, run_name=""):
        self.run_name = "_" + run_name
        self.view = View(False, False, "paper")

    def process_all(self, sensors="ga", merge_axes={"g": False, "a": False}):
        for entry in os.listdir(Path.RAW_PATH):
            if entry.find("e.csv") != -1:
                session_id = entry[:entry.find("_")]
                self.process(session_id, sensors, merge_axes)

    def process(self, session_id, sensors="ga", merge_axes={"g": False, "a": False}):
        data_path = Path.get_path(Path.RAW_PATH, session_id) + "_"
        output_path = Path.get_path(Path.FEATURE_PATH, session_id)

        label = Label(data_path)
        gyroscope = Gyroscope(data_path, self.view, merge_axes["g"])
        accelerometer = Accelerometer(data_path, self.view, merge_axes["a"])
        accelerometer.fit(gyroscope.timestamp)

        feature_extractor = FeatureExtractor(output_path, self.view, use_statistical_features=False)

        fusion = []
        for sensor in sensors:
            if sensor == 'g':
                fusion.append(gyroscope)
            if sensor == 'a':
                fusion.append(accelerometer)

        if label.has_label:
            feature_extractor.segment_from_labels(fusion, label)
        else:
            feature_extractor.segment_heuristically(fusion, gyroscope.get_mean_signal())

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

    def predict(self, session_id):
        self.process(session_id)

        classifier = Recurrent()
        classifier.retrieve_sample("{}{}.data".format(Path.FEATURE_PATH, session_id), is_labelled=False)
        classifier.evaluate(is_labelled=False)

if __name__ == "__main__":
    argv = sys.argv[1:]
    length = len(argv)

    v = View(True, True, "paper")

    v.plot_barchart(
        [([0.373025666578, 0.367080893497, 0.431190242506, 0.412785756485, 0.402505703031, 0.418872610971, 0.427297289822],
          [0.110226019592, 0.0969236576547, 0.0887581320032, 0.12242333994, 0.123381943808, 0.0534291379761, 0.0509361148712]),
         ([0.647812579514, 0.541792534155, 0.607798120908, 0.617981202941, 0.725041371656, 0.676142714071, 0.66495872617],
          [0.147544293302, 0.142810668947, 0.125222338836, 0.120056562871, 0.121752907104, 0.107792865971, 0.131764392002]),
         ([0.0378858368801, 0.0404751739562, 0.0403674696271, 0.0391558492471, 0.0384106392517, 0.0409793233211, 0.0384642877895],
          [0.0018363574503, 0.00759169087034, 0.00879365417906, 0.00654630997189, 0.00378130836884, 0.00968919533633, 0.00427866459814])],
        ["F1 score", "Reliability", "Least square mean error"],
        ['g', 'b', 'r'],
        'Number of neurons',
        'Score',
        ('6', '7', '8', '9', '10', '11', '12')
    )

    v.show()

    exit()

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
