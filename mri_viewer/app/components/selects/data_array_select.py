from trame.decorators import hot_reload
from trame.widgets import vuetify3

@hot_reload
def data_array_select():
    """Selector for selecting particular data array."""

    vuetify3.VSelect(
        variant="outlined",
        label=("language.data_array_select_title",),
        v_model=("current_data_array", None),
        items=("current_data_array_items", []),
        density="comfortable",
        disabled=("ui_off",),
        hide_details=True,
        classes="ma-4",
    )
