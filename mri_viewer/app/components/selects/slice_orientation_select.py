from trame.widgets import vuetify3

from ...constants import Planes, Representation

def slice_orientation_select():
    vuetify3.VSelect(
        v_show=f"current_representation == {Representation.Slice}",
        label=("language.slice_orientation_select_title",),
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
        classes="ma-4",
    )
