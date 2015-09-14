__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 14/09/2015'

from PeakAnalysis import *


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
        self.segment_sensor_from_labels(self.gyroscope, label_timestamps, labels, factor=100)
        self.segment_sensor_from_labels(self.accelerometer, label_timestamps, labels, factor=10)

    def segment_sensor_from_labels(self, sensor, label_timestamps, labels, factor, separator=","):
        if self.view is not None:
            self.view.plot_sensor_data_and_label("{} segmentation".format(sensor.name),
                                                 sensor.timestamp, sensor.x, sensor.y, sensor.z,
                                                 label_timestamps, labels)

        output_file = open("{}{}_labelled.data".format(self.output_path, sensor.name), 'w')

        for i in range(0, len(label_timestamps)):
            center_timestamp_index = (np.abs(sensor.timestamp - label_timestamps[i])).argmin()

            timestamp_sample = self.get_data_slice(sensor.timestamp, center_timestamp_index)
            x_sample = self.get_data_slice(sensor.x, center_timestamp_index)
            y_sample = self.get_data_slice(sensor.y, center_timestamp_index)
            z_sample = self.get_data_slice(sensor.z, center_timestamp_index)

            #if self.view is not None:
            #    self.view.plot_sensor_data("{} key {}".format(sensor.name, labels[i]), timestamp_sample, x_sample, y_sample, z_sample)

            output_file.write("label:{}\n".format(labels[i]))

            for j in range(0, len(x_sample)):
                x_value = '{0:.16f}'.format(x_sample[j] * factor)
                y_value = '{0:.16f}'.format(y_sample[j] * factor)
                z_value = '{0:.16f}'.format(z_sample[j] * factor)

                line = "{}{}{}{}{}\n".format(x_value, separator, y_value, separator, z_value)
                output_file.write(line)

            output_file.write("\n")
        output_file.close()

        print "Save features in {}".format(output_file.name)

        if self.view is not None:
            self.view.show()

    def get_data_slice(self, data, center_index, window_size=100):
        left_samples = data[center_index - (window_size / 2):center_index]
        right_samples = data[center_index:center_index + (window_size / 2)]

        return np.hstack((left_samples, right_samples))