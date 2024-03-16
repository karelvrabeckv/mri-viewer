from trame.decorators import hot_reload
from trame.widgets import html, vuetify3

from mri_viewer.app.components.icons import icon

from mri_viewer.app.constants import (
    Zoom,
    MIN_ZOOM_FACTOR,
    MAX_ZOOM_FACTOR,
    ZOOM_STEP,
)
from mri_viewer.app.styles import TOOL_HEADER

@hot_reload
def zoom_tool(ctrl):
    """A tool for zooming data."""

    with vuetify3.VCard(border=True, classes="ma-4"):
        with vuetify3.VCardTitle(
            "{{ language.section_zoom_title }}",
            style=TOOL_HEADER,
            classes="d-flex justify-space-between text-uppercase text-button font-weight-bold py-2"
        ):
            icon(
                key="mdi-information-variant",
                disabled=("ui_off",),
                size="x-small",
                tooltip=("language.section_zoom_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                icon(
                    key="mdi-minus",
                    disabled=("ui_off",),
                    tooltip=("language.zoom_out_tooltip",),
                    tooltip_location="bottom",
                    classes="mx-1",
                    click=(ctrl.zoom, f"['{Zoom.Out}']"),
                )
                icon(
                    key="mdi-plus",
                    disabled=("ui_off",),
                    tooltip=("language.zoom_in_tooltip",),
                    tooltip_location="bottom",
                    classes="mx-1",
                    click=(ctrl.zoom, f"['{Zoom.In}']"),
                )

            vuetify3.VDivider()

            with vuetify3.VRow(justify="center", classes="px-2 mt-4"):
                html.Span("{{ language.section_zoom_slider_title }}", classes="d-flex align-center ml-2 mr-4")
                vuetify3.VSpacer()
                html.Span("{{ current_zoom_factor }}x", classes="d-flex align-center ml-4 mr-2")

            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                vuetify3.VSlider(
                    disabled=("ui_off",),
                    v_model="current_zoom_factor",
                    show_ticks="always",
                    min=MIN_ZOOM_FACTOR,
                    max=MAX_ZOOM_FACTOR,
                    step=ZOOM_STEP,
                    hide_details=True,
                )