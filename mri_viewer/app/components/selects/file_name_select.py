from trame.widgets import vuetify3

def file_name_select():
    vuetify3.VSelect(
        label=("language.file_name_select_title",),
        v_model=("current_file_name", None),
        items=("current_file_name_items", []),
        disabled=("ui_off",),
        variant="outlined",
        hide_details=True,
        classes="ma-4",
    )
