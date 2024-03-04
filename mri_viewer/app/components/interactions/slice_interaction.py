from trame.widgets import html, vuetify3

import mri_viewer.app.constants as const
import mri_viewer.app.styles as style

def slice_interaction():
    with vuetify3.VCard(v_show=f"current_representation == {const.Representation.Slice}", border=True, classes="ma-4"): 
        vuetify3.VCardTitle(
            "{{ language.section_slice_title }}",
            style=style.HEADER,
            classes="text-uppercase text-button font-weight-bold py-2"
        )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="mt-2 pa-4"):
                vuetify3.VSelect(
                    label=("language.slice_orientation_select_title",),
                    v_model=("current_slice_orientation", None),
                    items=(
                        [
                            {"title": "XY", "value": const.Planes.XY},
                            {"title": "YZ", "value": const.Planes.YZ},
                            {"title": "XZ", "value": const.Planes.XZ},
                        ],
                    ),
                    variant="outlined",
                    hide_details=True,
                )
            
            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                html.Span("{{ language.slice_position_slider_title }}", classes="d-flex align-center ml-2 mr-4")
                vuetify3.VSlider(
                    v_model=("current_slice_position", None),
                    min=("current_min_slice_position", None),
                    max=("current_max_slice_position", None),
                    step=1,
                    hide_details=True,
                )
