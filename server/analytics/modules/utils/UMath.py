__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 29/08/2015'

from math import *

import numpy as np


class UMath:

    @staticmethod
    def normalize(range_min, range_max, x, x_min, x_max):
        return range_min + (((x - x_min) * (range_max - range_min)) / (x_max - x_min))

    @staticmethod
    def normalize_array(a):
        dimension = len(np.array(a).shape)

        if dimension == 1:
            return [UMath.normalize(0, 1, x, min(a), max(a)) for x in a]
        elif dimension == 2:
            return [[UMath.normalize(0, 1, y, np.amin(a), np.amax(a)) for y in x] for x in a]

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