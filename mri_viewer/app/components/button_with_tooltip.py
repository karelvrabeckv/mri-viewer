from trame.widgets import vuetify3

def tooltip(content):
    def tooltip(**kwargs):
        with vuetify3.VTooltip(
            text=kwargs["tooltip"],
            location=kwargs["tooltip_location"] if "tooltip_location" in kwargs.keys() else "bottom",
        ):
            with vuetify3.Template(v_slot_activator="{ props }"):
                content(**kwargs)
    return tooltip

@tooltip
def button(**kwargs):
    with vuetify3.VBtn(
        v_bind="props",
        icon=True,
        variant="flat",
        disabled=kwargs["disabled"] if "disabled" in kwargs.keys() else False,
        border=kwargs["border"] if "border" in kwargs.keys() else True,
        value=kwargs["value"] if "value" in kwargs.keys() else None,
        size=kwargs["size"] if "size" in kwargs.keys() else "default",
        classes=kwargs["classes"] if "classes" in kwargs.keys() else "",
        click=kwargs["click"] if "click" in kwargs.keys() else None,
    ):
        vuetify3.VIcon(icon=kwargs["icon"])

@tooltip
def toggle_button(**kwargs):
    with vuetify3.VBtn(
        v_bind="props",
        icon=True,
        variant="flat",
        disabled=kwargs["disabled"] if "disabled" in kwargs.keys() else False,
        classes=kwargs["classes"] if "classes" in kwargs.keys() else "",
        click=kwargs["click"] if "click" in kwargs.keys() else None,
    ):
        vuetify3.VIcon(v_if=kwargs["condition"], icon=kwargs["if_icon"])
        vuetify3.VIcon(v_else=kwargs["condition"], icon=kwargs["else_icon"])
