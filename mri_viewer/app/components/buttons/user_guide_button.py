from trame.decorators import hot_reload
from trame.widgets import html, vuetify3

@hot_reload
def user_guide_button():
    """Button to display user guide."""

    with html.A(href=("user_guide_url",), target="_blank"):
        with vuetify3.VBtnGroup(classes="ml-1 mr-2", border=True):
            vuetify3.VBtn(text=("language.user_guide_button_title",))
