from trame.widgets import html, vuetify3

from mri_viewer.app.components.buttons import button

import mri_viewer.app.constants as const
import mri_viewer.app.styles as style

def translation_interaction(self):
    def translate(direction):
        camera = self.pipeline.camera
        offset_x, offset_y, offset_z = 0.0, 0.0, 0.0

        if direction == const.Directions.XAxisPlus:
            offset_x -= self.state.current_translation_factor
        elif direction == const.Directions.XAxisMinus:
            offset_x += self.state.current_translation_factor
        elif direction == const.Directions.YAxisPlus:
            offset_y -= self.state.current_translation_factor
        elif direction == const.Directions.YAxisMinus:
            offset_y += self.state.current_translation_factor
        elif direction == const.Directions.ZAxisPlus:
            offset_z -= self.state.current_translation_factor
        elif direction == const.Directions.ZAxisMinus:
            offset_z += self.state.current_translation_factor
        
        offset = (offset_x, offset_y, offset_z)
        
        new_camera_position = list(map(lambda i, j: i + j, camera.GetPosition(), offset))
        new_focal_point_position = list(map(lambda i, j: i + j, camera.GetFocalPoint(), offset))
        
        camera.SetPosition(*new_camera_position)
        camera.SetFocalPoint(*new_focal_point_position)
        
        self.pipeline.camera = camera
        self.pipeline.render()
        self.ctrl.push_camera()
        
        _, _, group, _ = self.current_file_info
        group.current_view = self.pipeline.get_camera_params()
    
    with vuetify3.VCard(border=True, classes="ma-4"): 
        with vuetify3.VCardTitle(
            "{{ language.section_translation_title }}",
            style=style.HEADER,
            classes="d-flex justify-space-between text-uppercase text-button font-weight-bold py-2"
        ):
            button(
                icon="mdi-information-variant",
                disabled=("ui_off",),
                size="x-small",
                tooltip=("language.section_translation_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                button(
                    icon="mdi-arrow-left",
                    disabled=("ui_off",),
                    tooltip=("language.translate_x_axis_minus_tooltip",),
                    click=(translate, f"['{const.Directions.XAxisMinus}']"),
                )
                html.Div("X", classes="d-flex align-center text-body-1 mx-4")
                button(
                    icon="mdi-arrow-right",
                    disabled=("ui_off",),
                    tooltip=("language.translate_x_axis_plus_tooltip",),
                    click=(translate, f"['{const.Directions.XAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                button(
                    icon="mdi-arrow-left",
                    disabled=("ui_off",),
                    tooltip=("language.translate_y_axis_minus_tooltip",),
                    click=(translate, f"['{const.Directions.YAxisMinus}']"),
                )
                html.Div("Y", classes="d-flex align-center text-body-1 mx-4")
                button(
                    icon="mdi-arrow-right",
                    disabled=("ui_off",),
                    tooltip=("language.translate_y_axis_plus_tooltip",),
                    click=(translate, f"['{const.Directions.YAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                button(
                    icon="mdi-arrow-left",
                    disabled=("ui_off",),
                    tooltip=("language.translate_z_axis_minus_tooltip",),
                    click=(translate, f"['{const.Directions.ZAxisMinus}']"),
                )
                html.Div("Z", classes="d-flex align-center text-body-1 mx-4")
                button(
                    icon="mdi-arrow-right",
                    disabled=("ui_off",),
                    tooltip=("language.translate_z_axis_plus_tooltip",),
                    click=(translate, f"['{const.Directions.ZAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                html.Span("{{ language.factor_slider_title }}", classes="d-flex align-center ml-2 mr-4")
                vuetify3.VSlider(
                    disabled=("ui_off",),
                    v_model="current_translation_factor",
                    show_ticks="always",
                    min=const.MIN_TRANSLATION_FACTOR,
                    max=const.MAX_TRANSLATION_FACTOR,
                    step=const.TRANSLATION_STEP,
                    hide_details=True,
                )
                html.Span("{{ current_translation_factor }}", classes="d-flex align-center ml-4 mr-2")
