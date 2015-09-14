__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

import numpy as np
import scipy.signal as signal

from ..utils.UMath import *
from posixpath import basename
from pandas import Series


class Sensor:
    def __init__(self, file_path, view=None):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1,
                             names=['timestamp', 'x', 'y', 'z'],
                             dtype=[('timestamp', long), ('x', float), ('y', float), ('z', float)])

        print "Processing {}".format(file_path)

        self.timestamp = data['timestamp']

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

        self.view = view

        file_name = basename(file_path)
        self.name = file_name[file_name.find("_") + 1:file_name.find(".")]

        self.sampling_bias = None
        self.filter_type = None
        self.median_filter_window_size = None
        self.process_variance_q = None
        self.measurement_variance_estimate = None
        self.mean_signal = None

    def process(self, merge_axis=False):
        self.plot("raw")

        self.normalize()
        self.plot("normalize")

        if merge_axis:
            self.mean_signal = self.get_mean_signal()

        if self.median_filter_window_size is not None:
            self.apply_median_filter(self.median_filter_window_size)
            self.plot("median filter")

        if self.sampling_bias is not None and self.filter_type is not None:
            self.apply_filter(UMath.get_frequency(self.sampling_bias), self.filter_type)
            self.plot("{} filter".format(self.filter_type))

        self.apply_kalman_filter()
        self.plot("kalman filter")

        if self.view is not None:
            self.view.show()

    def plot(self, title):
        title = "{} {}".format(self.name, title)

        if self.view is not None:
            if self.mean_signal is None:
                self.view.plot_sensor_data(title, self.timestamp, self.x, self.y, self.z)
            else:
                self.view.plot_signal(title, self.timestamp, self.mean_signal)

    def apply_median_filter(self, window_size=3):
        if self.mean_signal is None:
            self.x = signal.medfilt(self.x, window_size)
            self.y = signal.medfilt(self.y, window_size)
            self.z = signal.medfilt(self.z, window_size)
        else:
            self.mean_signal = signal.medfilt(self.mean_signal, window_size)

    def apply_filter(self, sampling_frequency, filter_type):
        if self.mean_signal is None:
            self.x = self.apply_butter_filter(self.x, sampling_frequency, filter_type)
            self.y = self.apply_butter_filter(self.y, sampling_frequency, filter_type)
            self.z = self.apply_butter_filter(self.z, sampling_frequency, filter_type)
        else:
            self.mean_signal = self.apply_butter_filter(self.mean_signal, sampling_frequency, filter_type)

    def apply_butter_filter(self, data, frequency, type, order=6):
        CUTOFF_FREQUENCY = 0.5

        critical = 0.5 * frequency
        normal_cutoff = CUTOFF_FREQUENCY / critical

        b, a = signal.butter(order, normal_cutoff, btype=type, analog=False)

        result = signal.lfilter(b, a, data)
        return result

    def apply_kalman_filter(self):
        if self.mean_signal is None:
            self.x = self.get_kalman_filter_estimate(self.x)
            self.y = self.get_kalman_filter_estimate(self.y)
            self.z = self.get_kalman_filter_estimate(self.z)
        else:
            self.mean_signal = self.get_kalman_filter_estimate(self.mean_signal)

    def get_kalman_filter_estimate(self, data):
        length = len(data)

        a_posteriori_estimate = np.zeros(length)
        a_posteriori_error_estimate = np.zeros(length)
        a_priori_estimate = np.zeros(length)
        a_priori_error_estimate = np.zeros(length)
        blending_factor_gain = np.zeros(length)

        a_posteriori_estimate[0] = 0.0
        a_posteriori_error_estimate[0] = 1.0

        for i in range(1, length):
            a_priori_estimate[i] = a_posteriori_estimate[i - 1]
            a_priori_error_estimate[i] = a_posteriori_error_estimate[i - 1] + self.process_variance_q

            blending_factor_gain[i] = a_priori_error_estimate[i] / (a_priori_error_estimate[i] + self.measurement_variance_estimate)

            a_posteriori_estimate[i] = a_priori_estimate[i] + blending_factor_gain[i] * (data[i] - a_priori_estimate[i])
            a_posteriori_error_estimate[i] = (1 - blending_factor_gain[i]) * a_priori_error_estimate[i]

        return a_posteriori_estimate

    def normalize(self):
        self.mean = np.mean(self.x)
        self.x = map(self.normalize_axis, self.x)

        self.mean = np.mean(self.y)
        self.y = map(self.normalize_axis, self.y)

        self.mean = np.mean(self.z)
        self.z = map(self.normalize_axis, self.z)

    def normalize_axis(self, value):
        return value - self.mean

    def get_mean_signal(self):
        length = len(self.x)
        mean = np.zeros(length)

        for i in range(0, length):
            mean[i] = (self.x[i] + self.y[i] + self.z[i]) / 3

        return mean

    def fit(self, target_timestamps):
        merged_timestamps = sorted(set(np.concatenate((target_timestamps, self.timestamp))))

        self.x = self.adapt_values(self.x, target_timestamps, merged_timestamps)
        self.y = self.adapt_values(self.y, target_timestamps, merged_timestamps)
        self.z = self.adapt_values(self.z, target_timestamps, merged_timestamps)
        self.timestamp = target_timestamps

    def adapt_values(self, data, target_timestamps, merged_timestamps):
        timelink = {}
        for i in range(0, len(self.timestamp)):
            timelink[self.timestamp[i]] = data[i]

        length = len(merged_timestamps)
        values = np.zeros(length)
        values[:] = np.NaN

        for i in range(0, length):
            timekey = merged_timestamps[i]

            if timekey in timelink:
                values[i] = timelink[timekey]

        s = Series(data=values)
        s = s.interpolate()

        values = []
        for i in range(0, length):
            timekey = merged_timestamps[i]

            if timekey in target_timestamps:
                values.append(s[i])

        return values

