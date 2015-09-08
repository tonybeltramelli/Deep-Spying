__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

import numpy as np
import scipy.signal as signal

from ..PeakAnalysis import *
from ..utils.UMath import *
from posixpath import basename


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

    def segment_heuristically(self):
        self.mean_signal = self.get_mean_signal()

        p = PeakAnalysis()
        p.segment(self.mean_signal, True)

    def segment_from_labels(self, label_timestamps, labels, output_path, factor=100):
        output_file = open("{}labelled.data".format(output_path), 'w')

        if self.view is not None:
            self.view.plot_sensor_data_and_label("{} segmentation".format(self.name), self.timestamp, self.x, self.y, self.z, label_timestamps, labels)

        for i in range(0, len(label_timestamps)):
            center_timestamp_index = (np.abs(self.timestamp - label_timestamps[i])).argmin()

            timestamp_sample = self.get_data_slice(self.timestamp, center_timestamp_index)
            x_sample = self.get_data_slice(self.x, center_timestamp_index)
            y_sample = self.get_data_slice(self.y, center_timestamp_index)
            z_sample = self.get_data_slice(self.z, center_timestamp_index)

            #if self.view is not None:
            #    self.view.plot_sensor_data("{} key {}".format(self.name, labels[i]), timestamp_sample, x_sample, y_sample, z_sample)

            output_file.write("label:{}\n".format(labels[i]))

            for j in range(0, len(x_sample)):
                x_value = '{0:.16f}'.format(x_sample[j] * factor)
                y_value = '{0:.16f}'.format(y_sample[j] * factor)
                z_value = '{0:.16f}'.format(z_sample[j] * factor)

                line = "{}\n{}\n{}\n".format(x_value, y_value, z_value)
                output_file.write(line)

            output_file.write("\n")
        output_file.close()

        if self.view is not None:
            self.view.show()

    def get_data_slice(self, data, center_index, window_size=100):
        left_samples = data[center_index - (window_size / 2):center_index]
        right_samples = data[center_index:center_index + (window_size / 2)]

        return np.hstack((left_samples, right_samples))
