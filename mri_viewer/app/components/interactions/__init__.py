from trame.decorators import hot_reload
import mri_viewer.app.constants as const

from .slice_interaction import slice_interaction
from .zoom_interaction import zoom_interaction
from .translation_interaction import translation_interaction
from .rotation_interaction import rotation_interaction

if const.DEBUG_MODE:
    slice_interaction = hot_reload(slice_interaction)
    zoom_interaction = hot_reload(zoom_interaction)
    translation_interaction = hot_reload(translation_interaction)
    rotation_interaction = hot_reload(rotation_interaction)

__all__ = [
    "slice_interaction",
    "zoom_interaction",
    "translation_interaction",
    "rotation_interaction",
]
