__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from View import *
from Data import *


def preprocess(session_id):
    view = View()

    #gyroscope = Data(file_path="../../server/data/{}_gyroscope.csv".format(session_id),
    #                 sampling_rate=62500,
    #                 filter_type="lowpass",
    #                 normalize=False,
    #                 median_filter_window_size=9,
    #                 apply_kalman_filter=True,
    #                 view=view)

    #gyroscope.find_peaks()

    accelerometer = Data(file_path="../../server/data/{}_accelerometer.csv".format(session_id),
                         sampling_rate=10000,
                         merge_axis=True,
                         filter_type="highpass",
                         normalize=True,
                         median_filter_window_size=5,
                         apply_kalman_filter=True,
                         view=view)

    accelerometer.find_peaks()


preprocess("30809189")


