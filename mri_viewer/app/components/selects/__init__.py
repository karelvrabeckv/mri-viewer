from trame.decorators import hot_reload

import mri_viewer.app.constants as const

from .file_name_select import file_name_select
from .data_array_select import data_array_select
from .representation_select import representation_select

if const.DEBUG_MODE:
    file_name_select = hot_reload(file_name_select)
    data_array_select = hot_reload(data_array_select)
    representation_select = hot_reload(representation_select)

__all__ = [
    "file_name_select",
    "data_array_select",
    "representation_select",
]
