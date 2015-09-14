__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 29/08/2015'

from math import *


class UMath:

    @staticmethod
    def normalize(range_min, range_max, x, x_min, x_max):
        return range_min + (((x - x_min) * (range_max - range_min)) / (x_max - x_min))

    @staticmethod
    def get_frequency(sampling_rate_micro_sec):
        return 1 / (sampling_rate_micro_sec * 1e-06)

    @staticmethod
    def get_entropy(values):
        h = 0
        for x in values:
            h += x * log(x) if x > 0 else 0
        return h * -1

    @staticmethod
    def get_reliability(values):
        return 1 - ((1 / log(len(values))) * UMath.get_entropy(values))

    @staticmethod
    def get_denominator(d):
        return 1.0 if d == 0.0 else d