from trame.widgets import vuetify3

from mri_viewer.app.components.decorators import tooltip

@tooltip
def icon(**kwargs):
    """An icon with a tooltip for versatile use."""

    with vuetify3.VBtn(
        v_bind="props",
        icon=True,
        variant="flat",
        disabled=kwargs.get("disabled", False),
        border=kwargs.get("border", True),
        value=kwargs.get("value"),
        size=kwargs.get("size", "default"),
        classes=kwargs.get("classes", ""),
        click=kwargs.get("click"),
    ):
        vuetify3.VIcon(icon=kwargs["key"])
