from trame.widgets import vuetify3

from ...constants import DEFAULT_PICKER_MODE, PickerModes

def picker_modes_icons():
    with vuetify3.VBtnToggle(
        v_model=("picker_mode", DEFAULT_PICKER_MODE),
        disabled=("ui_disabled", True),
        mandatory=True,
        border=True,
    ):
        with vuetify3.VBtn(icon=True, value=PickerModes.Off):
            vuetify3.VIcon("mdi-cube-outline")
        with vuetify3.VBtn(icon=True, value=PickerModes.Points):
            vuetify3.VIcon("mdi-circle-small")
        with vuetify3.VBtn(icon=True, value=PickerModes.Cells):
            vuetify3.VIcon("mdi-triangle-outline")
