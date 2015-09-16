__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 14/09/2015'

from PeakAnalysis import *
from ..utils.UMath import *
from ..Path import Path


class FeatureExtractor:
    def __init__(self, gyroscope, accelerometer, output_path, view):
        self.gyroscope = gyroscope
        self.accelerometer = accelerometer
        self.output_path = output_path
        self.view = view

    def segment_heuristically(self, signal):
        p = PeakAnalysis()
        p.segment(signal, True)

    def segment_from_labels(self, label_timestamps, labels):
        self.accelerometer.fit(self.gyroscope.timestamp)

        self.segment_sensor_from_labels(label_timestamps, labels)

    def segment_sensor_from_labels(self, label_timestamps, labels, separator=","):
        output_file = open("{}labelled.data".format(self.output_path), 'w')

        for i in range(0, len(label_timestamps)):
            features = self.get_features((self.gyroscope, self.accelerometer), label_timestamps[i])

            output_file.write("label:{}\n".format(labels[i]))

            for j in range(0, len(features[0])):
                length = len(features)
                line = ""

                for k in range(0, length):
                    value = '{0:.16f}'.format(features[k][j])
                    line += "{}{}".format(value, separator if k < length - 1 else '\n')

                output_file.write(line)

            output_file.write("\n")
        output_file.close()

        print "Save features in {}".format(output_file.name)

        self.plot_segmentation(self.gyroscope, label_timestamps, labels)
        #self.plot_segmentation(self.accelerometer, label_timestamps, labels)

    def plot_segmentation(self, sensor, label_timestamps, labels):
        title = "{} segmentation".format(sensor.name)
        self.view.plot_sensor_data_and_label(title.title(), sensor.timestamp, sensor.x, sensor.y, sensor.z, label_timestamps, labels)

        self.view.save("{}{}_{}.png".format(Path.FIGURE_PATH, sensor.id, title.replace(" ", "_")))

        self.view.show()

    def get_features(self, sensors, timestamp_reference):
        sensor = sensors[0]
        center_timestamp_index = (np.abs(sensor.timestamp - timestamp_reference)).argmin()

        features = []

        for i in range(0, len(sensors)):
            sensor = sensors[i]
            if not sensor.use_for_feature_extraction:
                continue

            x_sample = self.get_data_slice(sensor.x, center_timestamp_index)
            y_sample = self.get_data_slice(sensor.y, center_timestamp_index)
            z_sample = self.get_data_slice(sensor.z, center_timestamp_index)

            features.append(UMath.scale(x_sample, sensor.scaling_factor))
            features.append(UMath.scale(y_sample, sensor.scaling_factor))
            features.append(UMath.scale(z_sample, sensor.scaling_factor))

        return features

    def get_data_slice(self, data, center_index, window_size=100):
        left_samples = data[center_index - (window_size / 2):center_index]
        right_samples = data[center_index:center_index + (window_size / 2)]

        return np.hstack((left_samples, right_samples))