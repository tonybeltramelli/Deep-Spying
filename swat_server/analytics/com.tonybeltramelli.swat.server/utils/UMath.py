__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 29/08/2015'


class UMath:

    @staticmethod
    def normalize(range_min, range_max, x, x_min, x_max):
        return range_min + (((x - x_min) * (range_max - range_min)) / (x_max - x_min))

    @staticmethod
    def get_frequency(sampling_rate_ms):
        return 1 / (sampling_rate_ms * 1e-06)