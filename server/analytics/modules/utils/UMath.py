__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 29/08/2015'

from math import *
from pandas import Series

import numpy as np


class UMath:

    @staticmethod
    def normalize(range_min, range_max, x, x_min, x_max):
        return range_min + (((x - x_min) * (range_max - range_min)) * (1 / (x_max - x_min)))

    @staticmethod
    def normalize_array(a, range_min=0, range_max=1):
        dimension = len(np.array(a).shape)

        if dimension == 1:
            amin = min(a)
            amax = max(a)
            return [UMath.normalize(range_min, range_max, x, amin, amax) for x in a]
        elif dimension == 2:
            amin = np.amin(a)
            amax = np.amax(a)
            return [[UMath.normalize(range_min, range_max, y, amin, amax) for y in x] for x in a]

    @staticmethod
    def get_frequency(sampling_rate_micro_sec):
        return 1 / (sampling_rate_micro_sec * 1e-06)

    @staticmethod
    def entropy(values):
        h = 0
        for x in values:
            h += x * log(x) if x > 0 else 0
        return h * -1

    @staticmethod
    def reliability(values):
        return 1 - ((1 / log(len(values))) * UMath.entropy(values))

    @staticmethod
    def get_denominator(d):
        return 1.0 if d == 0.0 else d

    @staticmethod
    def scale(vector, scalar):
        return [x * scalar for x in vector]

    @staticmethod
    def interpolate(a, target_size):
        length = len(a)
        values = np.zeros(target_size)
        values[:] = np.NaN

        step = target_size / length

        for i in range(0, length):
            values[i * step] = a[i]

        s = Series(data=values)
        s = s.interpolate()

        return s.values

    @staticmethod
    def get_root_mean_square(data):
        return sqrt(np.sum(np.square(data) / len(data)))