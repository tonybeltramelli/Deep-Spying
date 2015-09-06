__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 25/08/2015'

from modules.View import *
from modules.sensor.Gyroscope import *
from modules.sensor.Accelerometer import *


def preprocess(session_id):
    view = View()

    gyroscope = Gyroscope(session_id, view)
    #gyroscope.segment()

    accelerometer = Accelerometer(session_id, view)

preprocess("55687865")

