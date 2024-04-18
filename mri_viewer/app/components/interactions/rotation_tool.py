from trame.decorators import hot_reload
from trame.widgets import html, vuetify3

from mri_viewer.app.components.icons import icon
from mri_viewer.app.constants import Axis, Directions, RotationParams
from mri_viewer.app.styles import TOOL_HEADER

@hot_reload
def rotation_tool(ctrl):
    """A tool for rotating data."""

    with vuetify3.VCard(border=True, classes="ma-4"):
        with vuetify3.VCardTitle(
            "{{ language.section_rotation_title }}",
            style=TOOL_HEADER,
            classes="d-flex justify-space-between text-uppercase text-button font-weight-bold py-2"
        ):
            icon(
                key="mdi-information-variant",
                disabled=("ui_off",),
                size="x-small",
                tooltip=("language.section_rotation_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                icon(
                    key="mdi-undo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_x_axis_minus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.rotate, f"['{Directions.XAxisMinus}']"),
                )
                html.Div(Axis.X, classes="d-flex align-center text-body-1 mx-4")
                icon(
                    key="mdi-redo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_x_axis_plus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.rotate, f"['{Directions.XAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                icon(
                    key="mdi-undo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_y_axis_minus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.rotate, f"['{Directions.YAxisMinus}']"),
                )
                html.Div(Axis.Y, classes="d-flex align-center text-body-1 mx-4")
                icon(
                    key="mdi-redo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_y_axis_plus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.rotate, f"['{Directions.YAxisPlus}']"),
                )
            
            with vuetify3.VRow(justify="center", classes="my-4"):
                icon(
                    key="mdi-undo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_z_axis_minus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.rotate, f"['{Directions.ZAxisMinus}']"),
                )
                html.Div(Axis.Z, classes="d-flex align-center text-body-1 mx-4")
                icon(
                    key="mdi-redo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_z_axis_plus_tooltip",),
                    tooltip_location="bottom",
                    click=(ctrl.rotate, f"['{Directions.ZAxisPlus}']"),
                )
            
            vuetify3.VDivider()

            with vuetify3.VRow(justify="center", classes="px-2 mt-4"):
                html.Span("{{ language.section_rotation_slider_title }}", classes="d-flex align-center ml-2 mr-4")
                vuetify3.VSpacer()
                html.Span("{{ current_rotation_factor }}&deg;", classes="d-flex align-center ml-4 mr-2")

            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                vuetify3.VSlider(
                    disabled=("ui_off",),
                    v_model="current_rotation_factor",
                    show_ticks="always",
                    min=RotationParams.Min,
                    max=RotationParams.Max,
                    step=RotationParams.Step,
                    hide_details=True,
                )
