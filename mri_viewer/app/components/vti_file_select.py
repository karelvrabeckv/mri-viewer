from trame.widgets import vuetify3

def vti_file_select():
    vuetify3.VSelect(
        v_model=("current_vti_file", None),
        label="File",
        items=("current_vti_file_items", []),
        disabled=("selectors_disabled", True),
        variant="outlined",
        hide_details=True,
        classes="ma-4",
    )
