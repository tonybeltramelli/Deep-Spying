__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

import numpy as np
import pylab

from posixpath import basename


class View:
    def plot_sensor_data_from_file(self, file_path):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        file_name = basename(file_path)
        file_name = file_name[:file_name.find(".")]

        View.plot_sensor_data(basename(file_name), data['timestamp'], data['x'], data['y'], data['z'])

    def plot_sensor_data(self, title, timestamp, x, y, z):
        self.big_figure()

        pylab.plot(timestamp, x, color='r', label='x')
        pylab.plot(timestamp, y, color='g', label='y')
        pylab.plot(timestamp, z, color='b', label='z')

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Value')

    def plot_sensor_data_and_label(self, title, timestamp, x, y, z, label_timestamp, label):
        self.big_figure()

        pylab.plot(timestamp, x, color='r', label='x')
        pylab.plot(timestamp, y, color='g', label='y')
        pylab.plot(timestamp, z, color='b', label='z')

        for i in range(0, len(label_timestamp)):
            pylab.axvline(label_timestamp[i], color="k", label="{}: key {}".format(i, label[i]), ls='dashed')

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Value')

    def plot_signal(self, title, timestamp, signal):
        pylab.figure()

        pylab.plot(timestamp, signal, color='m', label="signal")

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Value')

    def plot_data(self, title, data, xlabel, ylabel):
        self.big_figure()

        pylab.plot(data, color='m')

        pylab.title(title)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)

    def plot_signal_and_label(self, title, timestamp, signal, label_timestamp, label):
        pylab.figure()

        pylab.plot(timestamp, signal, color='m', label='signal')

        for i in range(0, len(label_timestamp)):
            pylab.axvline(label_timestamp[i], color="k", label="{}: key {}".format(i, label[i]), ls='dashed')

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Value')

    def plot_sensor_data_and_segment(self, title, timestamp, x, y, z, segment, label):
        self.big_figure()

        pylab.plot(timestamp, x, color='r', label='x')
        pylab.plot(timestamp, y, color='g', label='y')
        pylab.plot(timestamp, z, color='b', label='z')

        for i in range(0, len(segment)):
            pylab.axvline(segment[i][0], color="c", ls='dashed')
            pylab.axvline(segment[i][1], color="k", label="{}: key {}".format(i, label[i]), ls='dashed')
            pylab.axvline(segment[i][2], color="m", ls='dashed')

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Value')

    def plot_comparison(self, values, estimate):
        pylab.figure()

        pylab.plot(values, 'm', label='measurements')
        pylab.plot(estimate, 'c', label='estimate')

        pylab.legend()

        pylab.xlabel('Time')
        pylab.ylabel('Value')

        pylab.show()

    def get_subplot_axes(self):
        f, axes = pylab.subplots(2, 4, sharex='col', sharey='row')
        return [axes[0, 0], axes[0, 1], axes[0, 2], axes[0, 3], axes[1, 0], axes[1, 1], axes[1, 2], axes[1, 3]]

    def subplot(self, axis, x, y, z, label):
        axis.plot(x, color='r', label='x')
        axis.plot(y, color='g', label='y')
        axis.plot(z, color='b', label='z')
        axis.set_title("{} key {}".format(self.name, label))

    def plot_confusion_matrix(self, matrix, labels):
        pylab.figure()
        pylab.imshow(matrix, interpolation='nearest', cmap=pylab.cm.jet)
        pylab.title("Confusion Matrix")

        for i, vi in enumerate(matrix):
            for j, vj in enumerate(vi):
                pylab.text(j-.1, i+.1, "%.2f" % vj, fontsize=14)

        pylab.colorbar()

        classes = np.arange(len(labels))
        pylab.xticks(classes, labels)
        pylab.yticks(classes, labels)

        pylab.ylabel('Expected label')
        pylab.xlabel('Predicted label')

    def big_figure(self):
        pylab.figure(figsize=(18, 9.5))

    def show(self):
        pylab.show()

    def save(self, name):
        pylab.savefig(name, bbox_inches='tight')
