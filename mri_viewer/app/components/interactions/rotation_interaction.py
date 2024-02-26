from trame.widgets import html, vuetify3
from trame.decorators import hot_reload

from vtkmodules.vtkCommonTransforms import vtkTransform

from mri_viewer.app.components import button

import mri_viewer.app.constants as const

@hot_reload
def rotation_interaction(self):
    def rotate(direction):
        camera = self.pipeline.renderer.GetActiveCamera()
        x, y, z = self.pipeline.actor.GetCenter()

        rotation = vtkTransform()
        rotation.Translate(x, y, z)
        
        if direction == const.Directions.XAxisPlus:
            rotation.RotateX(-self.state.current_rotation_factor)
        elif direction == const.Directions.XAxisMinus:
            rotation.RotateX(self.state.current_rotation_factor)
        elif direction == const.Directions.YAxisPlus:
            rotation.RotateY(-self.state.current_rotation_factor)
        elif direction == const.Directions.YAxisMinus:
            rotation.RotateY(self.state.current_rotation_factor)
        elif direction == const.Directions.ZAxisPlus:
            rotation.RotateZ(-self.state.current_rotation_factor)
        elif direction == const.Directions.ZAxisMinus:
            rotation.RotateZ(self.state.current_rotation_factor)
        
        rotation.Translate(-x, -y, -z)
        camera.ApplyTransform(rotation)

        self.pipeline.renderer.SetActiveCamera(camera)
        self.pipeline.render_window.Render()
        self.ctrl.push_camera()
        
        _, _, group, _ = self.current_file_information
        group.current_view = self.pipeline.get_camera_params()

    with vuetify3.VCard(disabled=("ui_off",), border=True, classes="ma-4"):
        with vuetify3.VCardTitle(
            "{{ language.section_rotation_title }}",
            classes="d-flex justify-space-between bg-grey-darken-2 py-2"
        ):
            button(
                icon="mdi-information-variant",
                size="x-small",
                tooltip=("language.section_rotation_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                html.Div("X:", classes="d-flex align-center text-body-1 mx-1")
                button(
                    icon="mdi-minus",
                    tooltip=("language.rotate_x_axis_minus_tooltip",),
                    classes="mx-1",
                    click=(rotate, f"['{const.Directions.XAxisMinus}']"),
                )
                button(
                    icon="mdi-plus",
                    tooltip=("language.rotate_x_axis_plus_tooltip",),
                    classes="mx-1",
                    click=(rotate, f"['{const.Directions.XAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                html.Div("Y:", classes="d-flex align-center text-body-1 mx-1")
                button(
                    icon="mdi-minus",
                    tooltip=("language.rotate_y_axis_minus_tooltip",),
                    classes="mx-1",
                    click=(rotate, f"['{const.Directions.YAxisMinus}']"),
                )
                button(
                    icon="mdi-plus",
                    tooltip=("language.rotate_y_axis_plus_tooltip",),
                    classes="mx-1",
                    click=(rotate, f"['{const.Directions.YAxisPlus}']"),
                )
            
            with vuetify3.VRow(justify="center", classes="my-4"):
                html.Div("Z:", classes="d-flex align-center text-body-1 mx-1")
                button(
                    icon="mdi-minus",
                    tooltip=("language.rotate_z_axis_minus_tooltip",),
                    classes="mx-1",
                    click=(rotate, f"['{const.Directions.ZAxisMinus}']"),
                )
                button(
                    icon="mdi-plus",
                    tooltip=("language.rotate_z_axis_plus_tooltip",),
                    classes="mx-1",
                    click=(rotate, f"['{const.Directions.ZAxisPlus}']"),
                )
            
            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                vuetify3.VSlider(
                    label=("language.rotation_factor_slider_title",),
                    v_model="current_rotation_factor",
                    show_ticks="always",
                    min=const.MIN_ROTATION_FACTOR,
                    max=const.MAX_ROTATION_FACTOR,
                    step=const.ROTATION_STEP,
                    hide_details=True,
                )
                html.Span("{{ current_rotation_factor }}", classes="d-flex align-center text-caption mx-2")
