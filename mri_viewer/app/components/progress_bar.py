from trame.widgets import vuetify3

def progress_bar():
    vuetify3.VProgressLinear(
        active=("trame__busy",),
        indeterminate=True,
        bg_opacity=1,
        bg_color="white",
        color="blue",
        absolute=True,
        location="bottom",
    )
