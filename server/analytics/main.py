__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from modules.View import *
from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *
from modules.label.Label import *
from modules.classifier.Classifier import *

def process(session_id):
    path = "../data/{}_".format(session_id)

    view = View()

    label = Label(path)

    gyroscope = Gyroscope(path, None)
    gyroscope.segment_from_labels(label.timestamp, label.label)

    #accelerometer = Accelerometer(path, view)
    #accelerometer.segment()

def train(session_id):
    path = "../data/{}_".format(session_id)

    classifer = Classifier(path)
    classifer.evaluate(path)

#process("69141736")
train("69141736")
