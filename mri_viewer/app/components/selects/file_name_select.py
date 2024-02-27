from trame.widgets import vuetify3
from trame.decorators import hot_reload

@hot_reload
def file_name_select():
    vuetify3.VSelect(
        variant="outlined",
        label=("language.file_name_select_title",),
        v_model=("current_file_name", None),
        items=("current_file_name_items", []),
        density="comfortable",
        disabled=("ui_off",),
        hide_details=True,
        classes="ma-4",
    )