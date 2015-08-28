__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 28/08/2015'

import numpy as np
from UPlot import *

class Data:
    def __init__(self, file_path):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        self.timestamp = data['timestamp']

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

        xM = (np.max(self.x) - np.min(self.x)) / 2
        yM = (np.max(self.y) - np.min(self.y)) / 2
        zM = (np.max(self.z) - np.min(self.z)) / 2

        self.target = (xM + yM + zM) / 3

        self.mean = np.mean(self.x)
        self.x = map(self.center, self.x)

        self.mean = np.mean(self.y)
        self.y = map(self.center, self.y)

        self.mean = np.mean(self.z)
        self.z = map(self.center, self.z)

        UPlot.plot_sensor_data(file_path, self.timestamp, self.x, self.y, self.z)

    def center(self, value):
        return (self.target * value) / self.mean


