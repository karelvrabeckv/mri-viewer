from trame.decorators import hot_reload
from trame.widgets import vuetify3

@hot_reload
def representation_select():
    """Selector for selecting particular representation."""

    vuetify3.VSelect(
        variant="outlined",
        label=("language.representation_select_title",),
        v_model=("current_representation", None),
        items=("current_representation_items", []),
        density="comfortable",
        disabled=("ui_off",),
        hide_details=True,
        classes="ma-4",
    )
