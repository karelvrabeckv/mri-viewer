from trame.widgets import html, vuetify3
from trame.decorators import hot_reload

from mri_viewer.app.components import button

import mri_viewer.app.constants as const

@hot_reload
def translation_interaction(self):
    def translate(direction):
        camera = self.pipeline.renderer.GetActiveCamera()
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
        
        self.pipeline.renderer.SetActiveCamera(camera)
        self.pipeline.render_window.Render()
        self.ctrl.push_camera()
        
        _, _, group, _ = self.current_file_information
        group.current_view = self.pipeline.get_camera_params()
    
    with vuetify3.VCard(disabled=("ui_off",), border=True, classes="ma-4"): 
        with vuetify3.VCardTitle(
            "{{ language.section_translation_title }}",
            classes="d-flex justify-space-between bg-grey-darken-2 py-2"
        ):
            button(
                icon="mdi-information-variant",
                size="x-small",
                tooltip=("language.section_translation_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                html.Div("X:", classes="d-flex align-center text-body-1 mx-1")
                button(
                    icon="mdi-minus",
                    tooltip=("language.translate_x_axis_minus_tooltip",),
                    classes="mx-1",
                    click=(translate, f"['{const.Directions.XAxisMinus}']"),
                )
                button(
                    icon="mdi-plus",
                    tooltip=("language.translate_x_axis_plus_tooltip",),
                    classes="mx-1",
                    click=(translate, f"['{const.Directions.XAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                html.Div("Y:", classes="d-flex align-center text-body-1 mx-1")
                button(
                    icon="mdi-minus",
                    tooltip=("language.translate_y_axis_minus_tooltip",),
                    classes="mx-1",
                    click=(translate, f"['{const.Directions.YAxisMinus}']"),
                )
                button(
                    icon="mdi-plus",
                    tooltip=("language.translate_y_axis_plus_tooltip",),
                    classes="mx-1",
                    click=(translate, f"['{const.Directions.YAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                html.Div("Z:", classes="d-flex align-center text-body-1 mx-1")
                button(
                    icon="mdi-minus",
                    tooltip=("language.translate_z_axis_minus_tooltip",),
                    classes="mx-1",
                    click=(translate, f"['{const.Directions.ZAxisMinus}']"),
                )
                button(
                    icon="mdi-plus",
                    tooltip=("language.translate_z_axis_plus_tooltip",),
                    classes="mx-1",
                    click=(translate, f"['{const.Directions.ZAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                vuetify3.VSlider(
                    label=("language.translation_factor_slider_title",),
                    v_model="current_translation_factor",
                    show_ticks="always",
                    min=const.MIN_TRANSLATION_FACTOR,
                    max=const.MAX_TRANSLATION_FACTOR,
                    step=const.TRANSLATION_STEP,
                    hide_details=True,
                )
                html.Span("{{ current_translation_factor }}", classes="d-flex align-center text-caption mx-2")
