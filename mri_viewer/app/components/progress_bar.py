from trame.widgets import vuetify3
from trame.decorators import hot_reload

import mri_viewer.app.constants as const

@hot_reload
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
