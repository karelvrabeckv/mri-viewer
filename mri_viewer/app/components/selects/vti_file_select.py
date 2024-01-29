from trame.widgets import vuetify3

def vti_file_select():
    vuetify3.VSelect(
        label="File",
        v_model=("current_vti_file", None),
        items=("current_vti_file_items", []),
        disabled=("ui_disabled", True),
        variant="outlined",
        hide_details=True,
        classes="ma-4",
    )
