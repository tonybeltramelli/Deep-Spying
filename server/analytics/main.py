__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *
from modules.label.Label import *
from modules.feature.FeatureExtractor import *
from modules.classification.classifier.Recurrent import *


class Main:
    def __init__(self):
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

    def train(self):
        classifier = Recurrent()
        classifier.retrieve_samples(Path.FEATURE_PATH)

        classifier.train_model(50)
        classifier.relevance.output_least_square_mean_errors("{}errors.png".format(Path.RESULT_PATH))

    def evaluate(self):
        classifier = Recurrent()
        classifier.retrieve_samples(Path.FEATURE_PATH)

        classifier.evaluate()
        classifier.relevance.output_confusion_matrix("{}confusion_matrix.png".format(Path.RESULT_PATH))
        classifier.relevance.output_statistics("{}statistics.md".format(Path.RESULT_PATH))

    def cross_validation(self):
        classifier = Recurrent()
        classifier.retrieve_samples(Path.FEATURE_PATH)

        classifier.k_fold_cross_validate(10, 50)
        classifier.compute()
        classifier.relevance.output_confusion_matrix("{}confusion_matrix.png".format(Path.RESULT_PATH))
        classifier.relevance.output_statistics("{}statistics.md".format(Path.RESULT_PATH))
        classifier.relevance.output_compared_plot("{}progression.png".format(Path.RESULT_PATH))

    def benchmark(self, classifiers):
        for classifier in classifiers:
            classifier.retrieve_samples(Path.FEATURE_PATH)
            classifier.k_fold_cross_validate(10, 50)

            classifier.relevance.output_confusion_matrix("{}{}_confusion_matrix.png".format(Path.RESULT_PATH, classifier.get_name()))
            classifier.relevance.output_statistics("{}{}_statistics.md".format(Path.RESULT_PATH, classifier.get_name()))
            classifier.relevance.output_compared_plot("{}{}_progression.png".format(Path.RESULT_PATH, classifier.get_name()))

main = Main()
main.process_all()
#main.process("23213605")
main.train()
main.evaluate()
#main.cross_validation()
#main.benchmark([Recurrent(), FeedForward()])




