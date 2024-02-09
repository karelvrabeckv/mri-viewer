from trame.widgets import vuetify3

from ...constants import Planes, Representation

def slice_interaction():
    with vuetify3.VCard(v_show=f"current_representation == {Representation.Slice}", classes="ma-4", border=True): 
        # Title
        vuetify3.VCardTitle("{{ language.section_slice_title }}", classes="bg-grey-darken-2 py-1")
        
        # Content
        with vuetify3.VCardText(classes="py-2"):
            vuetify3.VSelect(
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
                classes="py-2",
            )
            vuetify3.VSlider(
                label=("language.slice_position_slider_title",),
                v_model=("current_slice_position", None),
                min=("slider_range_min", None),
                max=("slider_range_max", None),
                step=1,
                hide_details=True,
                classes="py-2",
            )
