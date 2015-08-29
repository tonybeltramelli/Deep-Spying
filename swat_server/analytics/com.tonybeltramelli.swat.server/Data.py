__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 28/08/2015'

import numpy as np
import scipy.signal as signal

from utils.UMath import *


class Data:

    def __init__(self, file_path):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'x', 'y', 'z'])

        self.timestamp = data['timestamp']

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

    def apply_median_filter(self, window_size=3):
        self.x = signal.medfilt(self.x, window_size)
        self.y = signal.medfilt(self.y, window_size)
        self.z = signal.medfilt(self.z, window_size)

    def normalize(self):
        self.min = min(np.concatenate((self.x, self.y, self.z)))
        self.max = max(np.concatenate((self.x, self.y, self.z)))

        self.x = map(self.normalize_axis, self.x)
        self.y = map(self.normalize_axis, self.y)
        self.z = map(self.normalize_axis, self.z)

    def normalize_axis(self, value):
        return UMath.normalize(0, 1, value, self.min, self.max)

    def align(self):
        x_m = np.mean(self.x)
        y_m = np.mean(self.y)
        z_m = np.mean(self.z)

        self.target = (x_m + y_m + z_m) / 3

        self.mean = x_m
        self.x = map(self.align_axis, self.x)

        self.mean = y_m
        self.y = map(self.align_axis, self.y)

        self.mean = z_m
        self.z = map(self.align_axis, self.z)

    def align_axis(self, value):
        return value + (self.target - self.mean)



