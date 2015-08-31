__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 28/08/2015'

import numpy as np
import scipy.signal as signal

from utils.UMath import *


class Data:

    def __init__(self, file_path):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        self.timestamp = data['timestamp']

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

    def apply_median_filter(self, window_size=3):
        self.x = signal.medfilt(self.x, window_size)
        self.y = signal.medfilt(self.y, window_size)
        self.z = signal.medfilt(self.z, window_size)

    def apply_lowpass_filter(self):
        SAMPLING_FREQUENCY = 16.0
        CUTOFF_FREQUENCY = 0.5

        self.x = self.get_butter_lowpass_filter_result(self.x, CUTOFF_FREQUENCY, SAMPLING_FREQUENCY)
        self.y = self.get_butter_lowpass_filter_result(self.y, CUTOFF_FREQUENCY, SAMPLING_FREQUENCY)
        self.z = self.get_butter_lowpass_filter_result(self.z, CUTOFF_FREQUENCY, SAMPLING_FREQUENCY)

    def get_butter_lowpass_filter_result(self, data, cutoff_frequency, frequency, order=6):
        critical = 0.5 * frequency
        normal_cutoff = cutoff_frequency / critical
        b, a = signal.butter(order, normal_cutoff, btype='lowpass', analog=False)

        result = signal.lfilter(b, a, data)
        return result

    def apply_kalman_filter(self):
        self.x = self.get_kalman_filter_estimate(self.x)
        self.y = self.get_kalman_filter_estimate(self.y)
        self.z = self.get_kalman_filter_estimate(self.z)

    def get_kalman_filter_estimate(self, values):
        LENGTH = len(values)

        PROCESS_VARIANCE_Q = 1e-5
        MEASUREMENT_VARIANCE_ESTIMATE = 0.1 ** 2

        a_posteriori_estimate = np.zeros(LENGTH)
        a_posteriori_error_estimate = np.zeros(LENGTH)
        a_priori_estimate = np.zeros(LENGTH)
        a_priori_error_estimate = np.zeros(LENGTH)
        blending_factor_gain = np.zeros(LENGTH)

        a_posteriori_estimate[0] = 0.0
        a_posteriori_error_estimate[0] = 1.0

        for i in range(1, LENGTH):
            a_priori_estimate[i] = a_posteriori_estimate[i - 1]
            a_priori_error_estimate[i] = a_posteriori_error_estimate[i - 1] + PROCESS_VARIANCE_Q

            blending_factor_gain[i] = a_priori_error_estimate[i] / (a_priori_error_estimate[i] + MEASUREMENT_VARIANCE_ESTIMATE)

            a_posteriori_estimate[i] = a_priori_estimate[i] + blending_factor_gain[i] * (values[i] - a_priori_estimate[i])
            a_posteriori_error_estimate[i] = (1 - blending_factor_gain[i]) * a_priori_error_estimate[i]

        return a_posteriori_estimate

    def normalize(self):
        self.min = min(np.concatenate((self.x, self.y, self.z)))
        self.max = max(np.concatenate((self.x, self.y, self.z)))

        self.x = map(self.normalize_axis, self.x)
        self.y = map(self.normalize_axis, self.y)
        self.z = map(self.normalize_axis, self.z)

    def normalize_axis(self, value):
        return UMath.normalize(0, 1, value, self.min, self.max)

    def align(self):
        x_m = np.mean(self.x)
        y_m = np.mean(self.y)
        z_m = np.mean(self.z)

        self.target = (x_m + y_m + z_m) / 3

        self.mean = x_m
        self.x = map(self.align_axis, self.x)

        self.mean = y_m
        self.y = map(self.align_axis, self.y)

        self.mean = z_m
        self.z = map(self.align_axis, self.z)

    def align_axis(self, value):
        return value + (self.target - self.mean)


