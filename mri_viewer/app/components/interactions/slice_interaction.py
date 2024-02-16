from trame.widgets import vuetify3

import mri_viewer.app.constants as const

def slice_interaction():
    with vuetify3.VCard(v_show=f"current_representation == {const.Representation.Slice}", border=True, classes="ma-4"): 
        vuetify3.VCardTitle("{{ language.section_slice_title }}", classes="bg-grey-darken-2 py-2")
        
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
                vuetify3.VSlider(
                    label=("language.slice_position_slider_title",),
                    v_model=("current_slice_position", None),
                    min=("min_slice_position", None),
                    max=("max_slice_position", None),
                    step=1,
                    hide_details=True,
                )
