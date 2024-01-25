from trame.widgets import vuetify3

def axes_icon():
    vuetify3.VCheckbox(
        v_model=("axes_visibility", True),
        true_icon="mdi-cube-outline",
        false_icon="mdi-cube-off-outline",
        hide_details=True,
        classes="ma-4",
    )
