__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

import scipy.signal as signal

from ..utils.UMath import *
from pandas import Series
from ..Path import Path


class Sensor:
    def __init__(self, file_path, view=None, preprocess_signal=True):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1,
                             names=['timestamp', 'x', 'y', 'z'],
                             dtype=[('timestamp', long), ('x', float), ('y', float), ('z', float)])

        print "Processing {}".format(file_path)

        self.timestamp = data['timestamp']

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

        self.view = view

        self.name = Path.get_sensor_name(file_path)
        self.id = Path.get_id(file_path)

        self.maximum_delay = None
        self.filter_type = None
        self.median_filter_window_size = None
        self.process_variance_q = None
        self.measurement_variance_estimate = None
        self.mean_signal = None

        self.preprocess_signal = preprocess_signal

    def process(self, merge_axes=False):
        self.plot("raw")

        self.calibrate()
        self.plot("calibration")

        if merge_axes:
            self.mean_signal = self.get_mean_signal()

        if self.preprocess_signal:
            if self.median_filter_window_size is not None:
                self.apply_median_filter(self.median_filter_window_size)
                self.plot("median filter")

            if self.maximum_delay is not None and self.filter_type is not None:
                self.apply_filter(UMath.get_frequency(self.maximum_delay), self.filter_type)
                self.plot("{} filter".format(self.filter_type))

            self.apply_kalman_filter()
            self.plot("kalman filter")

        self.to_constant_rate()

        self.view.show()

    def plot(self, title):
        title = "{} {}".format(self.name, title)

        if self.mean_signal is None:
            self.view.plot_sensor_data(title.title(), self.timestamp, self.x, self.y, self.z)
        else:
            self.view.plot_signal(title.title(), self.timestamp, self.mean_signal)

        self.view.save("{}{}_{}.png".format(Path.RESULT_PATH, self.id, title.replace(" ", "_")))

    def apply_median_filter(self, window_size=3):
        if self.mean_signal is None:
            self.x = signal.medfilt(self.x, window_size)
            self.y = signal.medfilt(self.y, window_size)
            self.z = signal.medfilt(self.z, window_size)
        else:
            self.mean_signal = signal.medfilt(self.mean_signal, window_size)

    def apply_filter(self, sampling_frequency, filter_type):
        if self.mean_signal is None:
            self.x = self.apply_butterworth_filter(self.x, sampling_frequency, filter_type)
            self.y = self.apply_butterworth_filter(self.y, sampling_frequency, filter_type)
            self.z = self.apply_butterworth_filter(self.z, sampling_frequency, filter_type)
        else:
            self.mean_signal = self.apply_butterworth_filter(self.mean_signal, sampling_frequency, filter_type)

    def apply_butterworth_filter(self, data, frequency, type, order=6):
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
        if self.mean_signal is None:
            self.x = UMath.normalize_array(self.x, -1.0, 1.0)
            self.y = UMath.normalize_array(self.y, -1.0, 1.0)
            self.z = UMath.normalize_array(self.z, -1.0, 1.0)
        else:
            self.mean_signal = UMath.normalize_array(self.mean_signal, -1.0, 1.0)

        self.calibrate()

    def calibrate(self):
        if self.mean_signal is None:
            self.x = self.calibrate_axis(self.x)
            self.y = self.calibrate_axis(self.y)
            self.z = self.calibrate_axis(self.z)
        else:
            self.mean_signal = self.calibrate_axis(self.mean_signal)

    def calibrate_axis(self, data):
        mean = np.mean(data)
        return [x - mean for x in data]

    def get_mean_signal(self):
        length = len(self.x)
        mean = np.zeros(length)

        for i in range(0, length):
            mean[i] = (self.x[i] + self.y[i] + self.z[i]) / 3

        return mean

    def to_constant_rate(self, rate=2):
        diff = []
        for i in range(1, len(self.timestamp)):
            diff.append(self.timestamp[i] - self.timestamp[i - 1])

        mintime = np.amin(self.timestamp)
        maxtime = np.amax(self.timestamp)

        target_timestamps = np.arange(mintime, maxtime + rate, rate)

        self.fit(target_timestamps)

    def fit(self, target_timestamps):
        merged_timestamps = sorted(set(np.concatenate((target_timestamps, self.timestamp))))

        if self.mean_signal is None:
            self.x = self.adapt_values(self.x, target_timestamps, merged_timestamps)
            self.y = self.adapt_values(self.y, target_timestamps, merged_timestamps)
            self.z = self.adapt_values(self.z, target_timestamps, merged_timestamps)
        else:
            self.mean_signal = self.adapt_values(self.mean_signal, target_timestamps, merged_timestamps)

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

