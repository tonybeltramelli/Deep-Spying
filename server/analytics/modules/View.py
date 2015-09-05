__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

import numpy as np
import pylab
from posixpath import basename


class View:

    def plot(self, session_id):
        View.plot_sensor_data_from_file("../../server/data/{}_accelerometer.csv".format(session_id))
        View.plot_sensor_data_from_file("../../server/data/{}_gyroscope.csv".format(session_id))
        View.show()

    def plot_sensor_data_from_file(self, file_path):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        file_name = basename(file_path)
        file_name = file_name[:file_name.find(".")]

        View.plot_sensor_data(basename(file_name), data['timestamp'], data['x'], data['y'], data['z'])

    def plot_sensor_data(self, title, timestamp, x, y, z):
        pylab.figure()

        pylab.plot(timestamp, x, color='r', label='x')
        pylab.plot(timestamp, y, color='g', label='y')
        pylab.plot(timestamp, z, color='b', label='z')

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

    def plot_comparison(self, values, estimate):
        pylab.figure()

        pylab.plot(values, 'm', label='measurements')
        pylab.plot(estimate, 'c', label='estimate')

        pylab.legend()

        pylab.xlabel('Time')
        pylab.ylabel('Value')

        pylab.show()

    def show(self):
        pylab.show()
