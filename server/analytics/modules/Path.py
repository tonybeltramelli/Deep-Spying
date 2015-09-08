__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 08/09/2015'


class Path:
    BASE_PATH = "../data/"
    RAW_PATH = "{}raw/".format(BASE_PATH)
    FEATURE_PATH = "{}feature/".format(BASE_PATH)

    @staticmethod
    def get_path(root, variable):
        path = "{}{}_".format(root, variable)
        return path