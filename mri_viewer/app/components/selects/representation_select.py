from trame.widgets import vuetify3

def representation_select():
    vuetify3.VSelect(
        label=("language.representation_select_title",),
        v_model=("current_representation", None),
        items=("language.current_representation_items",),
        disabled=("ui_off",),
        variant="outlined",
        hide_details=True,
        classes="ma-4",
    )
    vuetify3.VDivider()
