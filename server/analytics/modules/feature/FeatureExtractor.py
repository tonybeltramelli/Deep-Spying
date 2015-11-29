__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 14/09/2015'

import scipy.stats as stats

from PeakAnalysis import *
from ..utils.UMath import *
from ..Path import Path


class FeatureExtractor:
    def __init__(self, output_path, view, use_statistical_features=False):
        self.output_path = output_path
        self.view = view
        self.use_statistical_features = use_statistical_features

    def segment_heuristically(self, sensors, reference_signal, label=None):
        p = PeakAnalysis(self.view)
        peaks = p.get_peaks(reference_signal)

        timestamps = []
        for peak_position in peaks:
            timestamps.append(sensors[0].timestamp[peak_position])

        if label:
            label_timestamps = label.timestamp
            labels = label.label
            closer_labels = []
            closer_timestamps = []

            for i in range(0, len(label_timestamps)):
                min_dist = label_timestamps[len(label_timestamps) - 1] - label_timestamps[0]
                closer_label = None
                closer_timestamp = None

                for heuristic_timestamp in timestamps:
                    dist = sqrt(np.square(label_timestamps[i] - heuristic_timestamp))

                    if dist < min_dist:
                        min_dist = dist
                        closer_label = labels[i]
                        closer_timestamp = heuristic_timestamp

                closer_labels.append(closer_label)
                closer_timestamps.append(closer_timestamp)

            self.segment(sensors, closer_timestamps, closer_labels)
        else:
            self.segment(sensors, timestamps)

    def segment_from_labels(self, sensors, label):
        label_timestamps = label.timestamp
        labels = label.label

        self.segment(sensors, label_timestamps, labels)

    def segment(self, sensors, timestamps, labels=None):
        output_file = open("{}.data".format(self.output_path), 'w')

        for i in range(0, len(timestamps)):
            features = self.get_features(sensors, timestamps[i])

            if labels is not None:
                output_file.write("label:{}\n".format(labels[i]))
            else:
                output_file.write(":\n")

            if not self.use_statistical_features:
                for j in range(0, len(features[0])):
                    line = self.get_line(features, j)

                    output_file.write(line)
            else:
                features = np.array(features).flatten()
                line = self.get_line(features)

                output_file.write(line)

            output_file.write("\n")
        output_file.close()

        print "Save features in {}".format(output_file.name)

        for sensor in sensors:
            self.plot_segmentation(sensor, timestamps, labels)

    def get_line(self, features, j=None, separator=","):
        length = len(features)
        line = ""

        for k in range(0, length):
            value = '{0:.16f}'.format(features[k] if j is None else features[k][j])
            line += "{}{}".format(value, separator if k < length - 1 else '\n')

        return line

    def plot_segmentation(self, sensor, label_timestamps, labels=None):
        title = "{} segmentation".format(sensor.name)
        self.view.plot_sensor_data_and_label(title.title(), sensor.timestamp, sensor.x, sensor.y, sensor.z, label_timestamps, labels)
        self.view.save("{}{}_{}.png".format(Path.RESULT_PATH, sensor.id, title.replace(" ", "_")))
        self.view.show()

    def get_features(self, sensors, timestamp_reference):
        sensor = sensors[0]
        center_timestamp_index = (np.abs(sensor.timestamp - timestamp_reference)).argmin()

        features = []

        for i in range(0, len(sensors)):
            sensor = sensors[i]
            sensor.normalize()

            if sensor.mean_signal is None:
                x_sample = self.get_data_slice(sensor.x, center_timestamp_index)
                y_sample = self.get_data_slice(sensor.y, center_timestamp_index)
                z_sample = self.get_data_slice(sensor.z, center_timestamp_index)

                features.append(x_sample if not self.use_statistical_features else self.get_statistical_features(x_sample))
                features.append(y_sample if not self.use_statistical_features else self.get_statistical_features(y_sample))
                features.append(z_sample if not self.use_statistical_features else self.get_statistical_features(z_sample))
            else:
                mean_sample = self.get_data_slice(sensor.mean_signal, center_timestamp_index)
                features.append(mean_sample if not self.use_statistical_features else self.get_statistical_features(mean_sample))

        return features

    def get_statistical_features(self, data):
        p = PeakAnalysis(self.view)

        min_value = np.amin(data)
        max_value = np.amax(data)
        root_mean_square = UMath.get_root_mean_square(data)
        peaks_number = np.mean(len(p.get_peaks(data)))
        crest_factor = np.median(p.get_peak_to_average_ratios(data))
        skewness = stats.skew(data, False)
        kurtosis = stats.kurtosis(data, False)
        variance = np.var(data)

        return [min_value, max_value, root_mean_square, peaks_number, crest_factor, skewness, kurtosis, variance]

    def get_data_slice(self, data, center_index, window_size=50):
        left_samples = data[center_index - (window_size / 2):center_index]
        right_samples = data[center_index:center_index + (window_size / 2)]

        return np.hstack((left_samples, right_samples))