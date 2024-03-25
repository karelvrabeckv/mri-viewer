from trame.decorators import hot_reload
from trame.widgets import html, vuetify3

from mri_viewer.app.components.icons import icon

from mri_viewer.app.constants import (
    Directions,
    MIN_TRANSLATION_FACTOR,
    MAX_TRANSLATION_FACTOR,
    TRANSLATION_STEP,
)
from mri_viewer.app.styles import TOOL_HEADER

@hot_reload
def translation_tool(ctrl):
    """A tool for translating data."""

    with vuetify3.VCard(border=True, classes="ma-4"): 
        with vuetify3.VCardTitle(
            "{{ language.section_translation_title }}",
            style=TOOL_HEADER,
            classes="d-flex justify-space-between text-uppercase text-button font-weight-bold py-2"
        ):
            icon(
                key="mdi-information-variant",
                disabled=("ui_off",),
                size="x-small",
                tooltip=("language.section_translation_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                icon(
                    key="mdi-arrow-left",
                    disabled=("ui_off",),
                    tooltip=("language.translate_x_axis_minus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.translate, f"['{Directions.XAxisMinus}']"),
                )
                html.Div("X", classes="d-flex align-center text-body-1 mx-4")
                icon(
                    key="mdi-arrow-right",
                    disabled=("ui_off",),
                    tooltip=("language.translate_x_axis_plus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.translate, f"['{Directions.XAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                icon(
                    key="mdi-arrow-left",
                    disabled=("ui_off",),
                    tooltip=("language.translate_y_axis_minus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.translate, f"['{Directions.YAxisMinus}']"),
                )
                html.Div("Y", classes="d-flex align-center text-body-1 mx-4")
                icon(
                    key="mdi-arrow-right",
                    disabled=("ui_off",),
                    tooltip=("language.translate_y_axis_plus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.translate, f"['{Directions.YAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                icon(
                    key="mdi-arrow-left",
                    disabled=("ui_off",),
                    tooltip=("language.translate_z_axis_minus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.translate, f"['{Directions.ZAxisMinus}']"),
                )
                html.Div("Z", classes="d-flex align-center text-body-1 mx-4")
                icon(
                    key="mdi-arrow-right",
                    disabled=("ui_off",),
                    tooltip=("language.translate_z_axis_plus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.translate, f"['{Directions.ZAxisPlus}']"),
                )

            vuetify3.VDivider()

            with vuetify3.VRow(justify="center", classes="px-2 mt-4"):
                html.Span("{{ language.section_translation_slider_title }}", classes="d-flex align-center ml-2 mr-4")
                vuetify3.VSpacer()
                html.Span("{{ current_translation_factor }}", classes="d-flex align-center ml-4 mr-2")

            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                vuetify3.VSlider(
                    disabled=("ui_off",),
                    v_model="current_translation_factor",
                    show_ticks="always",
                    min=MIN_TRANSLATION_FACTOR,
                    max=MAX_TRANSLATION_FACTOR,
                    step=TRANSLATION_STEP,
                    hide_details=True,
                )
