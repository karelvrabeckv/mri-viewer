from trame.widgets import vuetify3

import mri_viewer.app.constants as const

def progress_bar():
    vuetify3.VProgressLinear(
        active=("trame__busy",),
        indeterminate=True,
        bg_opacity=1,
        bg_color="white",
        color=const.IKEM_COLOR,
        absolute=True,
        location="bottom",
    )
