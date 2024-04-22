from trame.decorators import hot_reload
from trame.widgets import html, vuetify3

from mri_viewer.app.constants import Planes, Representations
from mri_viewer.app.styles import TOOL_HEADER

@hot_reload
def slice_tool():
    """Tool for slicing data."""

    with vuetify3.VCard(v_show=f"current_representation == {Representations.Slice}", border=True, classes="ma-4"): 
        vuetify3.VCardTitle(
            "{{ language.section_slice_title }}",
            style=TOOL_HEADER,
            classes="text-uppercase text-button font-weight-bold py-2"
        )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="px-4 my-4"):
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
                )

            vuetify3.VDivider()
            
            with vuetify3.VRow(justify="center", classes="px-2 mt-4"):
                html.Span("{{ language.slice_position_slider_title }}", classes="d-flex align-center ml-2 mr-4")
                vuetify3.VSpacer()
                html.Span("{{ current_slice_position }}", classes="d-flex align-center ml-4 mr-2")

            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                vuetify3.VSlider(
                    v_model=("current_slice_position", None),
                    min=("current_slice_min", None),
                    max=("current_slice_max", None),
                    step=("current_slice_step", None),
                    hide_details=True,
                )
