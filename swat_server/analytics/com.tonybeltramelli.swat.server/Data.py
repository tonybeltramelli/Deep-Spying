__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 28/08/2015'

import numpy as np
import scipy.signal as signal

from math import *
from utils.UMath import *


class Data:

    def __init__(self, file_path, sampling_rate, filter_type, normalize=False, median_filter_window_size=None, apply_kalman_filter=False, view=None):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        self.timestamp = data['timestamp']

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

        self.view = view
        self.plot("raw")

        if normalize:
            self.normalize()
            self.plot("normalize")

        if median_filter_window_size is not None:
            self.apply_median_filter(median_filter_window_size)
            self.plot("median filter")

        if sampling_rate is not None and filter_type is not None:
            self.apply_filter(UMath.get_frequency(sampling_rate), filter_type)
            self.plot("{} filter".format(filter_type))

        if apply_kalman_filter:
            self.apply_kalman_filter()
            self.plot("kalman filter")

        if self.view is not None:
            self.view.show()

    def plot(self, title):
        if self.view is not None:
            self.view.plot_sensor_data(title, self.timestamp, self.x, self.y, self.z)

    def apply_median_filter(self, window_size=3):
        self.x = signal.medfilt(self.x, window_size)
        self.y = signal.medfilt(self.y, window_size)
        self.z = signal.medfilt(self.z, window_size)

    def apply_filter(self, sampling_frequency, filter_type):
        self.x = self.apply_butter_filter(self.x, sampling_frequency, filter_type)
        self.y = self.apply_butter_filter(self.y, sampling_frequency, filter_type)
        self.z = self.apply_butter_filter(self.z, sampling_frequency, filter_type)

    def apply_butter_filter(self, data, frequency, type, order=6):
        CUTOFF_FREQUENCY = 0.5

        critical = 0.5 * frequency
        normal_cutoff = CUTOFF_FREQUENCY / critical

        b, a = signal.butter(order, normal_cutoff, btype=type, analog=False)

        result = signal.lfilter(b, a, data)
        return result

    def apply_kalman_filter(self):
        self.x = self.get_kalman_filter_estimate(self.x)
        self.y = self.get_kalman_filter_estimate(self.y)
        self.z = self.get_kalman_filter_estimate(self.z)

    def get_kalman_filter_estimate(self, data):
        length = len(data)

        PROCESS_VARIANCE_Q = 1e-5
        MEASUREMENT_VARIANCE_ESTIMATE = 1e-02

        a_posteriori_estimate = np.zeros(length)
        a_posteriori_error_estimate = np.zeros(length)
        a_priori_estimate = np.zeros(length)
        a_priori_error_estimate = np.zeros(length)
        blending_factor_gain = np.zeros(length)

        a_posteriori_estimate[0] = 0.0
        a_posteriori_error_estimate[0] = 1.0

        for i in range(1, length):
            a_priori_estimate[i] = a_posteriori_estimate[i - 1]
            a_priori_error_estimate[i] = a_posteriori_error_estimate[i - 1] + PROCESS_VARIANCE_Q

            blending_factor_gain[i] = a_priori_error_estimate[i] / (a_priori_error_estimate[i] + MEASUREMENT_VARIANCE_ESTIMATE)

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

    def find_peaks(self):
        ratios_x = self.get_peak_to_average_ratios(self.x)
        ratios_y = self.get_peak_to_average_ratios(self.y)
        ratios_z = self.get_peak_to_average_ratios(self.z)

        ratios = []

        for i in range(0, len(ratios_x)):
            ratios.append((i, (ratios_x[i] + ratios_y[i] + ratios_z[i]) / 3))

        print len(ratios)
        ratios = ratios[0::50]
        print len(ratios)
        ratios = sorted(ratios, key=lambda ratio: ratio[1], reverse=True)

        import pylab
        pylab.figure()

        pylab.plot(self.timestamp, self.x, color='r', label='x')
        pylab.plot(self.timestamp, self.y, color='g', label='y')
        pylab.plot(self.timestamp, self.z, color='b', label='z')

        for i in range(0, 20):
            pylab.axvline(self.timestamp[ratios[i][0]], color="k")

        pylab.legend()
        pylab.xlabel('Time')
        pylab.ylabel('Value')
        print "here"
        pylab.show()


    def get_peak_to_average_ratios(self, data):
        root_mean_square = self.get_root_mean_square(data)

        length = len(data)
        ratios = np.zeros(length)

        for i in range(0, length):
            crest_factor = data[i] / root_mean_square
            peak_to_average_ratio = pow(crest_factor, 2)

            ratios[i] = peak_to_average_ratio

        return ratios

    def get_root_mean_square(self, data):
        return sqrt(np.sum(np.square(data) / len(data)))




