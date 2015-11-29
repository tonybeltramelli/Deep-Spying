__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

from ..utils.UMath import *
from ..View import *


class PeakAnalysis:
    def __init__(self, view):
        self.view = view

    def get_peaks(self, signal):
        ratios = self.get_peak_to_average_ratios(signal)

        peak = (ratios > np.roll(ratios, 1))\
               &\
               (ratios > np.roll(ratios, -1))\
               &\
               (ratios > 4e-01)

        peak_indices = []

        for i in range(0, len(peak)):
            if peak[i]:
                peak_indices.append(i)

        return peak_indices

    def get_peak_to_average_ratios(self, signal):
        root_mean_square = UMath.get_root_mean_square(signal)

        ratios = np.array([pow(x / root_mean_square, 2) for x in signal])
        return ratios
