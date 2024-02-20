from trame.assets.local import LocalFileManager

asset_manager = LocalFileManager(__file__)
asset_manager.url("logo", "./logo.png")
