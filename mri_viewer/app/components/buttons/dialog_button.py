from trame.widgets import vuetify3

import mri_viewer.app.constants as const

def dialog_button():
    vuetify3.VDivider(vertical=True)
    
    with vuetify3.VBtnGroup(v_bind="props", classes="ml-2 mr-1"):
        vuetify3.VBtn(text=("language.load_files_title",), color=const.IKEM_COLOR)
