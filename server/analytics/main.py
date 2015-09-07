__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from modules.View import *
from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *
from modules.label.Label import *

def process(session_id):
    path = "../data/{}_".format(session_id)

    view = View()

    label = Label(path)

    gyroscope = Gyroscope(path, None)
    gyroscope.label_segmentation(session_id, label.timestamp, label.label)

    #accelerometer = Accelerometer(path, view)
    #accelerometer.segment()

    #view.plot_signal_and_label("data", gyroscope.timestamp, gyroscope.mean_signal, label.timestamp, label.label)
    #view.plot_sensor_data_and_label("data", gyroscope.timestamp, gyroscope.x, gyroscope.y, gyroscope.z, label.timestamp, label.label)
    #view.show()

#process("69141736")

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import *
from random import randint

net = buildNetwork(3, 2, 3, bias=True, hiddenclass=TanhLayer)
data_set = SupervisedDataSet(3, 3)
trainer = BackpropTrainer(net, data_set)

size_data_set = 100
iteration = 100

for i in range(0, size_data_set):
    a = [randint(0, 10) * -1, randint(0, 10) * 1, randint(0, 10) * 1]
    b = [randint(0, 10) * 1, randint(0, 10) * -1, randint(0, 10) * 1]
    c = [randint(0, 10) * 1, randint(0, 10) * 1, randint(0, 10) * -1]

    data_set.appendLinked(a, [1, 0, 0])
    data_set.appendLinked(b, [0, 1, 0])
    data_set.appendLinked(c, [0, 0, 1])

for i in range(0, iteration):
    error = trainer.train()
    print error

a = [-5, 5, 5]
b = [5, -5, 5]
c = [5, 5, -5]

result_a = net.activate(a)
result_b = net.activate(b)
result_c = net.activate(c)

print "a: {}, b: {}, c: {}".format(result_a, result_b, result_c)