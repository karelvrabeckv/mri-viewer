from trame.decorators import hot_reload
from trame.widgets import vuetify3

from mri_viewer.app.constants import IKEM_COLOR

@hot_reload
def open_dialog_button():
    """A button to display a dialog for uploading files."""
    
    with vuetify3.VBtnGroup(v_bind="props", classes="ml-2 mr-1"):
        vuetify3.VBtn(text=("language.load_files_title",), color=IKEM_COLOR)
