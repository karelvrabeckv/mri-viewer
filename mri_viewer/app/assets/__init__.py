import os

from trame.assets.local import LocalFileManager

asset_manager = LocalFileManager(os.path.dirname(__file__))
asset_manager.url("logo", "./logo.png")
