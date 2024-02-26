from trame.widgets import vuetify3
from trame.decorators import hot_reload

from mri_viewer.app.components import button

import mri_viewer.app.constants as const

@hot_reload
def picker_modes_icons():
    vuetify3.VDivider(vertical=True)
    
    with vuetify3.VBtnToggle(
        v_model=("picker_mode", const.DEFAULT_PICKER_MODE),
        disabled=("ui_picker_modes_off",),
        mandatory=True,
        border=True,
        classes="mx-2",
    ):
        vuetify3.VBtn(text="Off", value=const.PickerModes.Off)

        button(
            icon="mdi-dots-grid",
            value=const.PickerModes.Points,
            border=False,
            tooltip=("language.picker_mode_points_tooltip",),
        )

        button(
            icon="mdi-grid",
            value=const.PickerModes.Cells,
            border=False,
            tooltip=("language.picker_mode_cells_tooltip",),
        )

    vuetify3.VDivider(vertical=True)
