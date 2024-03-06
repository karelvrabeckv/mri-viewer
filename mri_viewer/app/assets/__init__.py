from trame.assets.local import LocalFileManager

import os

asset_manager = LocalFileManager(os.path.dirname(__file__))
asset_manager.url("logo", "./logo.png")
