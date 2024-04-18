from trame.decorators import hot_reload
from trame.widgets import vuetify3

@hot_reload
def color_map_select():
    """A selector for selecting a particular color map."""

    vuetify3.VSelect(
        variant="outlined",
        label=("language.color_map_select_title",),
        v_model=("current_color_map", None),
        items=("current_color_map_items", []),
        density="comfortable",
        disabled=("ui_off",),
        hide_details=True,
        classes="ma-4",
    )
