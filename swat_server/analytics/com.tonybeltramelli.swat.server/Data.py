__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 28/08/2015'

import numpy as np
from UPlot import *
import scipy.signal as signal

class Data:

    def __init__(self, file_path):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        self.timestamp = data['timestamp']

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

    def apply_median_filter(self):
        self.x = signal.medfilt(self.x, 5)
        self.y = signal.medfilt(self.y, 5)
        self.z = signal.medfilt(self.z, 5)

    def mean(self):
        xM = np.mean(self.x)
        yM = np.mean(self.y)
        zM = np.mean(self.z)

        self.target = (xM + yM + zM) / 3

        self.mean = xM
        self.x = map(self.center, self.x)

        self.mean = yM
        self.y = map(self.center, self.y)

        self.mean = zM
        self.z = map(self.center, self.z)

    def center(self, value):
        return (self.target * value) / self.mean


