from trame.decorators import hot_reload

import mri_viewer.app.constants as const

from .button_with_tooltip import button, toggle_button
from .dialog_button import dialog_button
from .language_buttons import language_buttons
from .user_guide_button import user_guide_button

if const.DEBUG_MODE:
    dialog_button = hot_reload(dialog_button)
    language_buttons = hot_reload(language_buttons)
    user_guide_button = hot_reload(user_guide_button)

__all__ = [
    "button",
    "toggle_button",
    "dialog_button",
    "language_buttons",
    "user_guide_button",
]
