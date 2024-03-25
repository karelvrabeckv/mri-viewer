from trame.decorators import hot_reload
from trame.widgets import vuetify3

from mri_viewer.app.constants import IKEM_COLOR

@hot_reload
def progress_bar():
    """A progress bar for indicating the busyness."""

    vuetify3.VProgressLinear(
        active=("trame__busy",),
        indeterminate=True,
        bg_opacity=1,
        bg_color="white",
        color=IKEM_COLOR,
        absolute=True,
        location="bottom",
    )
