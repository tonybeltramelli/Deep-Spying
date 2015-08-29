__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from UPlot import *
from Data import *


def plot(session_id):
    accelerometer = Data("../../server/data/{}_accelerometer.csv".format(session_id))
    gyroscope = Data("../../server/data/{}_gyroscope.csv".format(session_id))

    #UPlot.plot_sensor_data("accelerometer", accelerometer.timestamp, accelerometer.x, accelerometer.y, accelerometer.z)
    #UPlot.plot_sensor_data("gyroscope", gyroscope.timestamp, gyroscope.x, gyroscope.y, gyroscope.z)
    UPlot.show()

plot("49896377")
