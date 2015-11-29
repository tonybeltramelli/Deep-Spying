__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

from Sensor import *


class Accelerometer(Sensor):
    def __init__(self, path, view, merge_axes=False, preprocess_signal=True):
        Sensor.__init__(self, file_path="{}accelerometer.csv".format(path), view=view, preprocess_signal=preprocess_signal)

        self.maximum_delay = 10000
        self.median_filter_window_size = 5
        self.filter_type = "highpass"
        self.process_variance_q = 1e-02
        self.measurement_variance_estimate = 1e-01

        Sensor.process(self, merge_axes)