from trame.widgets import vuetify3

from mri_viewer.app.components.decorators import tooltip

@tooltip
def toggle_icon(**kwargs):
    """Toggle icon with tooltip for versatile use."""

    with vuetify3.VBtn(
        v_bind="props",
        icon=True,
        variant="flat",
        disabled=kwargs.get("disabled", False),
        classes=kwargs.get("classes", ""),
        click=kwargs.get("click"),
    ):
        vuetify3.VIcon(v_if=kwargs["condition"], icon=kwargs["if_key"])
        vuetify3.VIcon(v_else=kwargs["condition"], icon=kwargs["else_key"])
