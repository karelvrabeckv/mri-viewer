from trame.widgets import html, vuetify3

from vtkmodules.vtkCommonTransforms import vtkTransform

from mri_viewer.app.components.buttons import button

import mri_viewer.app.constants as const
import mri_viewer.app.styles as style

def rotation_interaction(self):
    def rotate(direction):
        camera = self.pipeline.camera
        x, y, z = self.pipeline.get_file_actor_center()

        rotation = vtkTransform()
        rotation.Translate(x, y, z)
        
        if direction == const.Directions.XAxisPlus:
            rotation.RotateX(self.state.current_rotation_factor)
        elif direction == const.Directions.XAxisMinus:
            rotation.RotateX(-self.state.current_rotation_factor)
        elif direction == const.Directions.YAxisPlus:
            rotation.RotateY(self.state.current_rotation_factor)
        elif direction == const.Directions.YAxisMinus:
            rotation.RotateY(-self.state.current_rotation_factor)
        elif direction == const.Directions.ZAxisPlus:
            rotation.RotateZ(self.state.current_rotation_factor)
        elif direction == const.Directions.ZAxisMinus:
            rotation.RotateZ(-self.state.current_rotation_factor)
        
        rotation.Translate(-x, -y, -z)
        camera.ApplyTransform(rotation)

        self.pipeline.camera = camera
        self.pipeline.render()
        self.ctrl.push_camera()
        
        _, _, group, _ = self.current_file_info
        group.current_view = self.pipeline.get_camera_params()

    # Bind method to controller
    self.ctrl.rotate = rotate

    with vuetify3.VCard(border=True, classes="ma-4"):
        with vuetify3.VCardTitle(
            "{{ language.section_rotation_title }}",
            style=style.TOOL_HEADER,
            classes="d-flex justify-space-between text-uppercase text-button font-weight-bold py-2"
        ):
            button(
                icon="mdi-information-variant",
                disabled=("ui_off",),
                size="x-small",
                tooltip=("language.section_rotation_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                button(
                    icon="mdi-undo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_x_axis_minus_tooltip",),
                    click=(self.ctrl.rotate, f"['{const.Directions.XAxisMinus}']"),
                )
                html.Div("X", classes="d-flex align-center text-body-1 mx-4")
                button(
                    icon="mdi-redo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_x_axis_plus_tooltip",),
                    click=(self.ctrl.rotate, f"['{const.Directions.XAxisPlus}']"),
                )

            with vuetify3.VRow(justify="center", classes="my-4"):
                button(
                    icon="mdi-undo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_y_axis_minus_tooltip",),
                    click=(self.ctrl.rotate, f"['{const.Directions.YAxisMinus}']"),
                )
                html.Div("Y", classes="d-flex align-center text-body-1 mx-4")
                button(
                    icon="mdi-redo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_y_axis_plus_tooltip",),
                    click=(self.ctrl.rotate, f"['{const.Directions.YAxisPlus}']"),
                )
            
            with vuetify3.VRow(justify="center", classes="my-4"):
                button(
                    icon="mdi-undo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_z_axis_minus_tooltip",),
                    click=(self.ctrl.rotate, f"['{const.Directions.ZAxisMinus}']"),
                )
                html.Div("Z", classes="d-flex align-center text-body-1 mx-4")
                button(
                    icon="mdi-redo",
                    disabled=("ui_off",),
                    tooltip=("language.rotate_z_axis_plus_tooltip",),
                    click=(self.ctrl.rotate, f"['{const.Directions.ZAxisPlus}']"),
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
                    min=const.MIN_ROTATION_FACTOR,
                    max=const.MAX_ROTATION_FACTOR,
                    step=const.ROTATION_STEP,
                    hide_details=True,
                )
