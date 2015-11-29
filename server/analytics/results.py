#!/usr/bin/env python
__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 16/11/2015'

import sys

from modules.classification.RelevanceAssessment import *
from modules.Path import *

LABELS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#"]
relevance = RelevanceAssessment(LABELS)

def parse_training_results():
    data = open('./advanced/report_training', 'r')

    losses = []
    loss = None

    for line in data:
        line = line.rstrip()

        if line.find("--") == -1:
            if not loss:
                loss = []
            loss.append(float(line))
        else:
            losses.append(loss)
            loss = None

    averageLoss = np.zeros(len(losses[0]))
    for l in losses:
        averageLoss = [sum(x) for x in zip(averageLoss, l)]

    for l in losses[0]:
        relevance.update_training(l)

    relevance.output_mean_square_mean_error("{}errors{}.png".format(Path.RESULT_PATH, run_name))

def parse_evaluation_results():
    data = open('./advanced/report_evaluation', 'r')

    for line in data:
        line = line.rstrip()

        if line.find("--") == -1:
            results = line.split("|")
            expected_label = results[0]
            predicted_label = results[1]
            predictions = results[2].split(",")

            relevance.update_evaluation(predicted_label, expected_label, [float(x) for x in predictions])
        else:
            datasetSize = float(line[2:])
            relevance.compute(datasetSize)

    relevance.output_confusion_matrix("{}confusion_matrix{}.png".format(Path.RESULT_PATH, run_name))
    relevance.output_statistics("{}statistics.md".format(Path.RESULT_PATH), run_name)
    relevance.output_compared_plot("{}progression{}.png".format(Path.RESULT_PATH, run_name))

if __name__ == "__main__":
    argv = sys.argv[1:]
    length = len(argv)

    if length < 1:
        print "Error: no argument supplied"
        print "Usage: "
        print "     results.py <run name>"
    else:
        run_name = argv[0]

        parse_training_results()
        parse_evaluation_results()
