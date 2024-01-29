from trame.widgets import vuetify3

def data_array_select():
    vuetify3.VSelect(
        label="Data Array",
        v_model=("current_data_array", None),
        items=("current_data_array_items", []),
        disabled=("ui_disabled", True),
        variant="outlined",
        hide_details=True,
        classes="ma-4",
    )
