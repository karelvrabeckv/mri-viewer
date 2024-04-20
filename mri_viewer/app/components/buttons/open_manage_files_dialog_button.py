from trame.decorators import hot_reload
from trame.widgets import vuetify3

@hot_reload
def open_manage_files_dialog_button():
    """A button to display a dialog for managing files."""
    
    with vuetify3.VBtnGroup(v_bind="props", classes="ml-1 mr-1", border=True):
        vuetify3.VBtn(text=("language.manage_files_button_title",))
