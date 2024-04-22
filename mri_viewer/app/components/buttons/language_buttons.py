from trame.decorators import hot_reload
from trame.widgets import vuetify3

from mri_viewer.app.constants import DEFAULT_LANGUAGE, Languages

@hot_reload
def language_buttons():
    """Buttons for switching between different languages."""

    with vuetify3.VBtnToggle(
        v_model=("current_language", DEFAULT_LANGUAGE),
        mandatory=True,
        border=True,
        classes="mx-2",
    ):
        vuetify3.VBtn(text=Languages.Czech, value=Languages.Czech)
        vuetify3.VBtn(text=Languages.English, value=Languages.English)
