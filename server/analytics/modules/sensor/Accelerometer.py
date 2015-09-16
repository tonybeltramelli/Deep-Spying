__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

from Sensor import *


class Accelerometer(Sensor):
    def __init__(self, path, view):
        Sensor.__init__(self, file_path="{}accelerometer.csv".format(path), view=view)

        self.sampling_bias = 10000
        self.median_filter_window_size = 5
        self.filter_type = "highpass"
        self.process_variance_q = 1e-02
        self.measurement_variance_estimate = 1e-01
        self.scaling_factor = 10
        self.use_for_feature_extraction = True

        Sensor.process(self, merge_axis=False)