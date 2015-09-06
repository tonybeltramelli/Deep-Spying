__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 06/09/2015'

import numpy as np


class Label:
    def __init__(self, file_path):
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1, names=['timestamp', 'label'])

        self.timestamp = data['timestamp']
        self.label = data['label']