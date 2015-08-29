__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from View import *
from Data import *


def plot(session_id):
    accelerometer = Data("../../server/data/{}_accelerometer.csv".format(session_id))
    gyroscope = Data("../../server/data/{}_gyroscope.csv".format(session_id))

    accelerometer.apply_median_filter(3)
    accelerometer.align()
    accelerometer.normalize()

    gyroscope.apply_median_filter(5)
    gyroscope.normalize()

    view = View()
    view.plot_sensor_data("accelerometer", accelerometer.timestamp, accelerometer.x, accelerometer.y, accelerometer.z)
    view.plot_sensor_data("gyroscope", gyroscope.timestamp, gyroscope.x, gyroscope.y, gyroscope.z)
    view.show()

plot("49896377")
