from trame.widgets import vuetify3

from ..constants import IKEM_COLOR

def progress_bar():
    vuetify3.VProgressLinear(
        active=("trame__busy",),
        indeterminate=True,
        bg_opacity=1,
        bg_color="white",
        color=IKEM_COLOR,
        absolute=True,
        location="bottom",
    )
