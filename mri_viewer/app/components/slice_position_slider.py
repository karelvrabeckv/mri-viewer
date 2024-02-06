from trame.widgets import vuetify3

from ..constants import Representation

def slice_position_slider():
    show = f"current_representation == {Representation.Slice}"
    
    vuetify3.VSlider(
        v_show=show,
        label=("language.slice_position_slider_title",),
        v_model=("current_slice_position", None),
        min=("slider_range_min", None),
        max=("slider_range_max", None),
        step=1,
        hide_details=True,
        classes="ma-4",
    )
    vuetify3.VDivider(v_show=show)
