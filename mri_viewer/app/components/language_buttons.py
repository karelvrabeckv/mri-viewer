from trame.widgets import vuetify3
from trame.decorators import hot_reload

import mri_viewer.app.constants as const

@hot_reload
def language_buttons():
    vuetify3.VDivider(vertical=True)
    
    with vuetify3.VBtnToggle(
        v_model=("current_language", const.DEFAULT_LANGUAGE),
        mandatory=True,
        border=True,
        classes="mx-2",
    ):
        vuetify3.VBtn(text=const.Languages.Czech, value=const.Languages.Czech)
        vuetify3.VBtn(text=const.Languages.English, value=const.Languages.English)
