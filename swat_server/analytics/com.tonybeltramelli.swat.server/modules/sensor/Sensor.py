__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

import numpy as np
import scipy.signal as signal

from math import *
from ..utils.UMath import *
from posixpath import basename


class Sensor:
    def __init__(self, file_path, view=None):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        self.timestamp = data['timestamp']

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

        self.view = view

        file_name = basename(file_path)
        self.name = file_name[file_name.find("_") + 1:file_name.find(".")]

        self.sampling_rate = None
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

        if self.sampling_rate is not None and self.filter_type is not None:
            self.apply_filter(UMath.get_frequency(self.sampling_rate), self.filter_type)
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

    def segment(self):
        ratios = self.get_peak_to_average_ratios(self.mean_signal)

        uphill = (((ratios + np.roll(ratios, -1) + np.roll(ratios, 1)) / 3) <= 9e-02)\
                 &\
                 (((ratios + np.roll(ratios, -5)) / 2) > 0.1)

        peak = (ratios > np.roll(ratios, 1))\
               &\
               (ratios > np.roll(ratios, -1))\
               &\
               (ratios > 4e-01)

        #downhill = (((ratios + np.roll(ratios, -1) + np.roll(ratios, 1)) / 3) <= 9e-02)\
        #         &\
        #         (((ratios + np.roll(ratios, -5)) / 2) < 0.1)

        length = len(ratios)

        temp = []

        for i in range(0, length):
            if peak[i]:
                for j in xrange(i, 0, -1):
                    if uphill[j]:
                        temp.append(j)
                        break

        uphill = np.zeros(length, dtype=bool)

        for i in temp:
            uphill[i] = True

        result = self.filter_interval(0, 200, uphill).flatten()

        #print result

        #result = self.filter_interval(result)

        import pylab
        pylab.figure()

        pylab.plot(ratios, color='b', label='mean')
        pylab.plot(uphill.nonzero()[0], ratios[uphill], 'ro')
        pylab.plot(peak.nonzero()[0], ratios[peak], 'go')
        #pylab.plot(downhill.nonzero()[0], ratios[downhill], 'bo')

        for i in range(0, len(result)):
            pylab.axvline(result[i], color="r")

        pylab.legend()
        pylab.xlabel('Time')
        pylab.ylabel('Value')
        pylab.show()

    def filter_interval(self, index, limit, data):
        length = len(data)
        for i in range(index, len(data)):
            if data[i]:
                index = i + limit
                if index < length:
                    return np.vstack((i, self.filter_interval(index, limit, data)))
                else:
                    return

    def wait(self, window_size=21):
        ratios = self.get_peak_to_average_ratios(self.mean_signal)
        length = len(ratios)

        weights = []

        for i in range(0, length, window_size):
            weight = 0
            end = i + window_size
            end = length if end > length else end

            for j in range(i, end):
                weight += ratios[j]

            median_index = i + ((window_size - 1) / 2)
            median_index = length - 1 if median_index > length else median_index

            weights.append((median_index, weight))

        filtered_weights = self.filter_weight(weights)
        filtered_weights = self.filter_time(filtered_weights)

        #weights = sorted(weights, key=lambda ratio: ratio[1], reverse=True)

        import pylab
        pylab.figure()

        pylab.plot(self.timestamp, self.mean_signal, color='b', label='mean')

        for i in range(0, len(filtered_weights)):
            pylab.axvline(self.timestamp[filtered_weights[i][0]], color="k")

        pylab.legend()
        pylab.xlabel('Time')
        pylab.ylabel('Value')
        pylab.show()

    def filter_weight(self, weights):
        filtered_weights = []

        for i in range(0, len(weights)):
            weight = weights[i][1]

            if weight >= 17.0:
                filtered_weights.append(weights[i])

        return filtered_weights

    def filter_time(self, weights):
        filtered_weights = []
        last_time = 0

        for i in range(0, len(weights)):
            time = self.timestamp[weights[i][0]]

            diff = time - last_time

            if diff >= 1358000000:
                filtered_weights.append(weights[i])

            last_time = time

        return filtered_weights

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
