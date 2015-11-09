__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

from ..utils.UMath import *
from ..View import *


class PeakAnalysis:
    def __init__(self, view):
        self.view = view

    def get_peaks(self, signal):
        ratios = self.get_peak_to_average_ratios(signal)

        uphill = (((ratios + np.roll(ratios, -1) + np.roll(ratios, 1)) / 3) <= 9e-02)\
                 &\
                 (((ratios + np.roll(ratios, -5)) / 2) > 0.1)

        peak = (ratios > np.roll(ratios, 1))\
               &\
               (ratios > np.roll(ratios, -1))\
               &\
               (ratios > 4e-01)

        downhill = (((ratios + np.roll(ratios, -1) + np.roll(ratios, 1)) / 3) <= 9e-02)\
                 &\
                 (((ratios + np.roll(ratios, -5)) / 2) < 0.1)

        uphill = self.filter_from_peak_position(peak, uphill, -1)
        downhill = self.filter_from_peak_position(peak, downhill, 1)

        self.view = View(True, True)
        self.view.plot_peaks(ratios, uphill, peak, downhill)
        self.view.show()

        peak_indices = []

        for i in range(0, len(peak)):
            if peak[i]:
                peak_indices.append(i)

        return peak_indices

    def filter_from_peak_position(self, peak, hill, direction):
        length = len(peak)
        temp = []

        for i in range(0, length):
            if peak[i]:
                for j in xrange(i, 0 if direction < 0.0 else length, direction):
                    if hill[j]:
                        temp.append(j)
                        break

        hill = np.zeros(length, dtype=bool)

        for i in temp:
            hill[i] = True

        return hill

    def get_peak_to_average_ratios(self, signal):
        root_mean_square = UMath.get_root_mean_square(signal)

        ratios = np.array([pow(x / root_mean_square, 2) for x in signal])
        return ratios
