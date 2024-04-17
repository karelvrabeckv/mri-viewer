from trame.assets.local import LocalFileManager

from os.path import dirname

class AssetManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__assets = LocalFileManager(dirname(__file__))
        self.__assets.url("logo", "./logo.png")

    @property
    def assets(self):
        return self.__assets
