from trame.decorators import hot_reload
import mri_viewer.app.constants as const

from .animation_icons import animation_icons
from .picker_modes_icons import picker_modes_icons
from .toolbar_icons import toolbar_icons

if const.DEBUG_MODE:
    animation_icons = hot_reload(animation_icons)
    picker_modes_icons = hot_reload(picker_modes_icons)
    toolbar_icons = hot_reload(toolbar_icons)

__all__ = [
    "animation_icons",
    "picker_modes_icons",
    "toolbar_icons",
]
