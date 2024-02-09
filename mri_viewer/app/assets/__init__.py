from trame.assets.local import LocalFileManager

asset_manager = LocalFileManager(__file__)
asset_manager.url("favicon", "./favicon.png")
asset_manager.url("icon_light", "./icon_light.png")
asset_manager.url("icon_dark", "./icon_dark.png")
