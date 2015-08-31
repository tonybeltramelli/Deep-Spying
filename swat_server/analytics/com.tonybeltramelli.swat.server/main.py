__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from View import *
from Data import *


def preprocess(session_id, to_plot=False):
    gyroscope = Data("../../server/data/{}_gyroscope.csv".format(session_id))

    if to_plot:
        view = View()
        view.plot_sensor_data("raw gyroscope", gyroscope.timestamp, gyroscope.x, gyroscope.y, gyroscope.z)

    gyroscope.apply_median_filter(9)

    if to_plot:
        view.plot_sensor_data("median filter", gyroscope.timestamp, gyroscope.x, gyroscope.y, gyroscope.z)

    gyroscope.apply_lowpass_filter()

    if to_plot:
        view.plot_sensor_data("lowpass filter", gyroscope.timestamp, gyroscope.x, gyroscope.y, gyroscope.z)

    gyroscope.apply_kalman_filter()

    if to_plot:
        view.plot_sensor_data("kalman filter", gyroscope.timestamp, gyroscope.x, gyroscope.y, gyroscope.z)
        view.show()

preprocess("66181201")
