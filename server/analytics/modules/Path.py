__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 08/09/2015'

from posixpath import basename


class Path:
    BASE_PATH = "../data/"
    RAW_PATH = "{}raw/".format(BASE_PATH)
    FEATURE_PATH = "{}feature/".format(BASE_PATH)
    RESULT_PATH = "{}result/".format(BASE_PATH)

    @staticmethod
    def get_path(root, variable):
        path = "{}{}".format(root, variable)
        return path

    @staticmethod
    def get_sensor_name(file_path):
        file_name = basename(file_path)
        return file_name[file_name.find("_") + 1:file_name.find(".")]

    @staticmethod
    def get_id(file_path):
        file_name = basename(file_path)
        return file_name[:file_name.find("_")]

