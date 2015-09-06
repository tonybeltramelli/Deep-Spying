__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from modules.View import *
from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *
from modules.label.Label import *


def process(session_id):
    path = "../../server/data/{}_".format(session_id)

    view = View()

    gyroscope = Gyroscope(path, None)
    gyroscope.segment()

    accelerometer = Accelerometer(path, None)

    label = Label(path)

    view.plot_signal_and_label("data", gyroscope.timestamp, gyroscope.mean_signal, label.timestamp, label.label)
    view.plot_sensor_data_and_label("data", gyroscope.timestamp, gyroscope.x, gyroscope.y, gyroscope.z, label.timestamp, label.label)
    view.show()

process("69141736")
