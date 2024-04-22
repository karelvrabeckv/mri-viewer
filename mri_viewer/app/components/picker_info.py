from trame.decorators import hot_reload
from trame.widgets import html, vuetify3

@hot_reload
def picker_info():
    """Information about picked point or cell."""

    with vuetify3.VCard(title=("picker_info_title",), style=("picker_info_style",)):
        with vuetify3.VCardText():
            with vuetify3.Template(v_for="(value, key) in picker_info_message"):
                html.Pre("<b>{{ key }}:</b> {{ value }}")
