from trame.widgets import vuetify3

def tooltip(content):
    """Add tooltip to surrounded content."""

    def wrapper(**kwargs):
        with vuetify3.VTooltip(
            text=kwargs["tooltip"],
            location=kwargs["tooltip_location"],
        ):
            with vuetify3.Template(v_slot_activator="{ props }"):
                content(**kwargs)
    
    return wrapper
