from trame.widgets import vuetify3

from ...constants import Planes

def slice_orientation_select():
    vuetify3.VSelect(
        label="Slice Orientation",
        v_model=("current_slice_orientation", None),
        items=(
            [
                {"title": "XY", "value": Planes.XY},
                {"title": "YZ", "value": Planes.YZ},
                {"title": "XZ", "value": Planes.XZ},
            ],
        ),
        variant="outlined",
        hide_details=True,
        classes=("ui_slice_classes", "ma-4 d-none"),
    )
