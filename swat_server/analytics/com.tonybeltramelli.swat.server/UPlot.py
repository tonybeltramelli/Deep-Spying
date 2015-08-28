__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

import numpy as np
import matplotlib.pyplot as plot
from posixpath import basename


class UPlot:

    @staticmethod
    def plot(session_id):
        UPlot.plot_sensor_data_from_file("../../server/data/{}_accelerometer.csv".format(session_id))
        UPlot.plot_sensor_data_from_file("../../server/data/{}_gyroscope.csv".format(session_id))
        UPlot.show()

    @staticmethod
    def plot_sensor_data_from_file(file_path):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        file_name = basename(file_path)
        file_name = file_name[:file_name.find(".")]

        UPlot.plot_sensor_data(basename(file_name), data['timestamp'], data['x'], data['y'], data['z'])

    @staticmethod
    def plot_sensor_data(name, timestamp, x, y, z):
        fig = plot.figure()

        ax1 = fig.add_subplot(111)

        ax1.set_title(name)
        ax1.set_xlabel('time')
        ax1.set_ylabel('value')

        ax1.plot(timestamp, x, color='r', label='x')
        ax1.plot(timestamp, y, color='g', label='y')
        ax1.plot(timestamp, z, color='b', label='z')

        ax1.legend()

    @staticmethod
    def show():
        plot.show()
