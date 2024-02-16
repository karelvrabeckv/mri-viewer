from trame.widgets import vuetify3

import mri_viewer.app.constants as const

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
