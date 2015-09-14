__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from modules.View import *
from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *
from modules.label.Label import *
from modules.Path import *
from modules.classifier.Recurrent import *

import os


class Main:
    def process_all(self):
        for entry in os.listdir(Path.RAW_PATH):
            if entry.find("e.csv") != -1:
                session_id = entry[:entry.find("_")]
                self.process(session_id)

    def process(self, session_id):
        data_path = Path.get_path(Path.RAW_PATH, session_id)
        output_path = Path.get_path(Path.FEATURE_PATH, session_id)

        view = None#View()

        label = Label(data_path)

        gyroscope = Gyroscope(data_path, view)
        gyroscope.segment_from_labels(label.timestamp, label.label, output_path)

        accelerometer = Accelerometer(data_path, view)

    def train(self):
        classifier = Recurrent()
        classifier.build_data_set(Path.FEATURE_PATH)
        classifier.train_model()

    def evaluate(self):
        classifier = Recurrent()
        classifier.evaluate("{}33916838_labelled.data".format(Path.FEATURE_PATH))
        classifier.evaluate("{}41991669_labelled.data".format(Path.FEATURE_PATH))
        classifier.evaluate("{}96390069_labelled.data".format(Path.FEATURE_PATH))
        classifier.evaluate("{}69141736_labelled.data".format(Path.FEATURE_PATH))

main = Main()
main.process_all()
main.train()
main.evaluate()