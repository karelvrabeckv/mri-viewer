from trame.decorators import hot_reload
import mri_viewer.app.constants as const

from .button_with_tooltip import button, toggle_button
from .language_buttons import language_buttons
from .progress_bar import progress_bar
from .load_files_dialog import load_files_dialog
from .view import view

if const.DEBUG_MODE:
    language_buttons = hot_reload(language_buttons)
    progress_bar = hot_reload(progress_bar)
    load_files_dialog = hot_reload(load_files_dialog)
    view = hot_reload(view)

__all__ = [
    "button",
    "toggle_button",
    "language_buttons",
    "progress_bar",
    "load_files_dialog",
    "view",
]
