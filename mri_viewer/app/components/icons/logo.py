from trame.decorators import hot_reload
from trame.widgets import html

@hot_reload
def logo(asset_manager):
    """The logo of the IKEM."""

    with html.A(href="https://www.ikem.cz/", target="_blank", classes="d-flex align-center"):
        html.Img(src=asset_manager.assets.logo, height=48)
