from trame.widgets import vuetify3

from ..constants import Languages, DEFAULT_LANGUAGE

def language_buttons():
    with vuetify3.VBtnToggle(
        v_model=("current_language", DEFAULT_LANGUAGE),
        mandatory=True,
        border=True,
        classes="mx-2",
    ):
        vuetify3.VBtn(text=Languages.Czech, value=Languages.Czech)
        vuetify3.VBtn(text=Languages.English, value=Languages.English)
