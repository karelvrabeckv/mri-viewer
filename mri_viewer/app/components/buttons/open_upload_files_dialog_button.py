from trame.decorators import hot_reload
from trame.widgets import vuetify3

from mri_viewer.app.constants import Theme

@hot_reload
def open_upload_files_dialog_button():
    """Button to display dialog for uploading files."""
    
    with vuetify3.VBtnGroup(v_bind="props", classes="ml-2 mr-1"):
        vuetify3.VBtn(text=("language.upload_files_button_title",), color=Theme.IKEMColor)
