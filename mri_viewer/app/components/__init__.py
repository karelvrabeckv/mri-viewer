from trame.decorators import hot_reload

import mri_viewer.app.constants as const

from .load_files_dialog import load_files_dialog
from .progress_bar import progress_bar
from .view import view

if const.DEBUG_MODE:
    load_files_dialog = hot_reload(load_files_dialog)
    progress_bar = hot_reload(progress_bar)
    view = hot_reload(view)

__all__ = [
    "load_files_dialog",
    "progress_bar",
    "view",
]
