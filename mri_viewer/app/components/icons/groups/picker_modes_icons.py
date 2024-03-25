from trame.decorators import hot_reload
from trame.widgets import vuetify3

from mri_viewer.app.components.icons import icon
from mri_viewer.app.constants import DEFAULT_PICKER_MODE, PickerModes

@hot_reload
def picker_modes_icons():
    """Icons for switching between different picker modes."""

    with vuetify3.VBtnToggle(
        v_model=("picker_mode", DEFAULT_PICKER_MODE),
        disabled=("ui_picker_modes_off",),
        mandatory=True,
        border=True,
        classes="mx-2",
    ):
        vuetify3.VBtn(text="Off", value=PickerModes.Off)

        icon(
            key="mdi-dots-grid",
            value=PickerModes.Points,
            border=False,
            tooltip=("language.picker_mode_points_tooltip",),
            tooltip_location="bottom",
        )

        icon(
            key="mdi-grid",
            value=PickerModes.Cells,
            border=False,
            tooltip=("language.picker_mode_cells_tooltip",),
            tooltip_location="bottom",
        )
