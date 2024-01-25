from trame.widgets import vuetify3

def progress_bar():
    vuetify3.VProgressLinear(
        color="blue",
        indeterminate=True,
        active=("trame__busy",),
        absolute=True,
        location="bottom",
    )
