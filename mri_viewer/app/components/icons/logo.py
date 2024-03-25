from trame.decorators import hot_reload
from trame.widgets import html

from mri_viewer.app.assets import asset_manager

@hot_reload
def logo():
    """The logo of the IKEM."""

    with html.A(href="https://www.ikem.cz/", target="_blank", classes="d-flex align-center"):
        html.Img(src=asset_manager.logo, height=48)
