import os


def here(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))
