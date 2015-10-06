__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

from ..utils.UMath import *
from ..View import *


class PeakAnalysis:
    def __init__(self, view):
        self.view = view

    def detect_peaks(self, timestamp, signal, labels):
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

        self.view.plot_peaks(timestamp, ratios, uphill, peak, downhill, labels)
        self.view.show()

        return {"uphill": np.count_nonzero(uphill), "peak": np.count_nonzero(peak), "downhill": np.count_nonzero(downhill)}

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

    def filter_interval(self, index, limit, data):
        length = len(data)

        for i in xrange(index, 0 if limit < 0.0 else length, -1 if limit < 0.0 else 1):
            if data[i]:
                index = i + limit

                if index < length:
                    return np.vstack((i, self.filter_interval(index, limit, data)))
                else:
                    return

    def get_peak_to_average_ratios(self, data):
        root_mean_square = UMath.get_root_mean_square(data)

        length = len(data)
        ratios = np.zeros(length)

        for i in range(0, length):
            crest_factor = data[i] / root_mean_square
            peak_to_average_ratio = pow(crest_factor, 2)

            ratios[i] = peak_to_average_ratio

        return ratios
