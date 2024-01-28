from trame.widgets import vuetify3

def slice_position_slider():
    vuetify3.VSlider(
        v_model=("current_slice_position", None),
        label="Slice Position",
        min=("slider_range_min", None),
        max=("slider_range_max", None),
        step=1,
        hide_details=True,
        classes=("ui_slice_classes", "ma-4 d-none"),
    )
