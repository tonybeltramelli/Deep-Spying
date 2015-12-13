__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

import numpy as np
import pylab

from posixpath import basename


class View:
    def __init__(self, to_show=True, to_save=True, screen_size=None):
        self.to_show = to_show
        self.to_save = to_save
        self.screen_size = screen_size

    def plot_sensor_data_from_file(self, file_path):
        if not self.to_save and not self.to_show:
            return

        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        file_name = basename(file_path)
        file_name = file_name[:file_name.find(".")]

        View.plot_sensor_data(basename(file_name), data['timestamp'], data['x'], data['y'], data['z'])

    def plot_sensor_data(self, title, timestamp, x, y, z):
        if not self.to_save and not self.to_show:
            return

        self.big_figure()
        pylab.grid("on")

        pylab.plot(timestamp, x, color='r', label='x')
        pylab.plot(timestamp, y, color='g', label='y')
        pylab.plot(timestamp, z, color='b', label='z')

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Amplitude')

    def plot_sensor_data_and_label(self, title, timestamp, x, y, z, label_timestamp, label=None):
        if not self.to_save and not self.to_show:
            return

        self.big_figure()

        pylab.plot(timestamp, x, color='r', label='x')
        pylab.plot(timestamp, y, color='g', label='y')
        pylab.plot(timestamp, z, color='b', label='z')

        for i in range(0, len(label_timestamp)):
            if label is not None:
                if i != 0:
                    pylab.axvline(label_timestamp[i], color="k", ls='dashed')
                else:
                    pylab.axvline(label_timestamp[i], color="k", label="keystroke", ls='dashed')
            else:
                pylab.axvline(label_timestamp[i], color="k", ls='dashed')

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Amplitude')
        if label:
            pylab.xticks(label_timestamp, label)

    def plot_signal(self, title, timestamp, signal):
        if not self.to_save and not self.to_show:
            return

        pylab.figure()

        pylab.plot(timestamp, signal, color='m', label="signal")

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Amplitude')

    def plot_data(self, title, data, xlabel, ylabel, colors=None, labels=None):
        if not self.to_save and not self.to_show:
            return

        self.big_figure()

        for i in range(0, len(data)):
            color = 'm' if colors is None else colors[i]

            if labels is None:
                pylab.plot(data[i], color=color)
            else:
                pylab.plot(data[i], color=color, label=labels[i])

        if labels is not None:
            pylab.legend()

        pylab.title(title)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)

    def plot_signal_and_label(self, title, timestamp, signal, label_timestamp, label):
        if not self.to_save and not self.to_show:
            return

        pylab.figure()

        pylab.plot(timestamp, signal, color='m', label='signal')

        for i in range(0, len(label_timestamp)):
            pylab.axvline(label_timestamp[i], color="k", label="{}: key {}".format(i, label[i]), ls='dashed')

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Amplitude')

    def plot_sensor_data_and_segment(self, title, timestamp, x, y, z, segment, label):
        if not self.to_save and not self.to_show:
            return

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
        pylab.ylabel('Amplitude')

    def plot_comparison(self, values, estimate):
        if not self.to_save and not self.to_show:
            return

        pylab.figure()

        pylab.plot(values, 'm', label='measurements')
        pylab.plot(estimate, 'c', label='estimate')

        pylab.legend()

        pylab.xlabel('Time')
        pylab.ylabel('Amplitude')

        pylab.show()

    def get_subplot_axes(self):
        if not self.to_save and not self.to_show:
            return

        f, axes = pylab.subplots(2, 4, sharex='col', sharey='row')
        return [axes[0, 0], axes[0, 1], axes[0, 2], axes[0, 3], axes[1, 0], axes[1, 1], axes[1, 2], axes[1, 3]]

    def subplot(self, axis, x, y, z, label):
        if not self.to_save and not self.to_show:
            return

        axis.plot(x, color='r', label='x')
        axis.plot(y, color='g', label='y')
        axis.plot(z, color='b', label='z')
        axis.set_title("key {}".format(label))

    def plot_confusion_matrix(self, matrix, labels):
        if not self.to_save and not self.to_show:
            return

        pylab.figure()
        pylab.imshow(matrix, interpolation='nearest', cmap=pylab.cm.jet)
        pylab.title("Confusion Matrix")

        for i, vi in enumerate(matrix):
            for j, vj in enumerate(vi):
                pylab.annotate("%.1f" % vj, xy=(j, i), horizontalalignment='center', verticalalignment='center', fontsize=9)

        pylab.colorbar()

        classes = np.arange(len(labels))
        pylab.xticks(classes, labels)
        pylab.yticks(classes, labels)

        pylab.ylabel('Expected label')
        pylab.xlabel('Predicted label')

    def plot_peaks(self, signal, uphill, peak, downhill):
        if not self.to_save and not self.to_show:
            return

        self.big_figure()
        pylab.grid("on")

        pylab.plot(signal, color='b')
        pylab.plot(uphill.nonzero()[0], signal[uphill], 'ro')
        pylab.plot(peak.nonzero()[0], signal[peak], 'go')
        pylab.plot(downhill.nonzero()[0], signal[downhill], 'bo')

        pylab.xlabel('Time')
        pylab.ylabel('Amplitude')

    def plot_fusion_sensor(self, title, timestamp, values, labels, colors):
        if not self.to_save and not self.to_show:
            return

        self.big_figure()
        pylab.grid("on")

        for i in range(0, len(values)):
            pylab.plot(timestamp, values[i], color=colors[i], label=labels[i])

        pylab.legend()

        pylab.title(title)
        pylab.xlabel('Time')
        pylab.ylabel('Amplitude')

    def plot_barchart(self, data, labels, colors, xlabel, ylabel, xticks, legendloc=1):
        self.big_figure()

        index = np.arange(len(data[0][0]))
        bar_width = 0.25

        pylab.grid("on", axis='y')
        pylab.ylim([0.5, 1.0])

        for i in range(0, len(data)):
            rects = pylab.bar(bar_width / 2 + index + (i * bar_width), data[i][0], bar_width,
                              alpha=0.5, color=colors[i],
                              yerr=data[i][1],
                              error_kw={'ecolor': '0.3'},
                              label=labels[i])

        pylab.legend(loc=legendloc, prop={'size': 12})

        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.xticks(bar_width / 2 + index + ((bar_width * (len(data[0]) + 1)) / len(data[0])), xticks)

    def big_figure(self):
        if self.screen_size == "fullscreen":
            pylab.figure(figsize=(18, 9.5))
        elif self.screen_size == "paper":
            pylab.figure(figsize=(11, 4))
        elif self.screen_size == "medium":
            pylab.figure(figsize=(12, 6))
        elif self.screen_size == "square":
            pylab.figure(figsize=(5, 5))
        else:
            pylab.figure()

    def show(self):
        if self.to_show:
            pylab.show()

    def save(self, name):
        if self.to_save:
            pylab.savefig(name, bbox_inches='tight')
