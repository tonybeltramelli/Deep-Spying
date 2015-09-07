__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 04/09/2015'

import numpy as np
import pylab

from math import *


class PeakAnalysis:

    def segment(self, signal, to_show=False):
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
        #uphill_filtered = self.filter_interval(0, 190, uphill).flatten()

        downhill = self.filter_from_peak_position(peak, downhill, 1)
        downhill_filtered = self.filter_interval(len(ratios) - 1, -170, downhill).flatten()

        if to_show:
            pylab.figure()

            pylab.plot(ratios, color='b')
            pylab.plot(uphill.nonzero()[0], ratios[uphill], 'ro')
            pylab.plot(peak.nonzero()[0], ratios[peak], 'go')
            pylab.plot(downhill.nonzero()[0], ratios[downhill], 'bo')

            #for i in range(0, len(uphill_filtered)):
            #    pylab.axvline(uphill_filtered[i], color="r")

            #for i in range(0, len(downhill_filtered)):
            #    pylab.axvline(downhill_filtered[i], color="b")

            pylab.xlabel('Time')
            pylab.ylabel('Value')
            pylab.show()

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
        root_mean_square = self.get_root_mean_square(data)

        length = len(data)
        ratios = np.zeros(length)

        for i in range(0, length):
            crest_factor = data[i] / root_mean_square
            peak_to_average_ratio = pow(crest_factor, 2)

            ratios[i] = peak_to_average_ratio

        return ratios

    def get_root_mean_square(self, data):
        return sqrt(np.sum(np.square(data) / len(data)))
