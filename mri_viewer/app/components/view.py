from trame.widgets import vtk, vuetify3

import mri_viewer.app.constants as const
import mri_viewer.app.styles as style

def view(self):
    def on_picker(event, **kwargs):
        if self.state.picker_mode == const.PickerModes.Off:
            return

        self.state.picker_info_style = style.HIDDEN

        file, _, _, _ = self.current_file_info
        image_data = file.reader.GetOutput()

        position = event["position"]
        x, y = position["x"], position["y"]
        
        if self.state.picker_mode == const.PickerModes.Points:
            message = self.pipeline.get_picked_point_info(image_data, x, y)

            if message:
                self.state.update({
                    "picker_info_title": self.state.language["point_info_title"],
                    "picker_info_message": message,
                    "picker_info_style": style.TOOLTIP,
                })

                point_id = message["Id"]
                point_position = image_data.GetPoint(point_id)
                self.pipeline.show_picked_point(point_position)
            else:
                self.pipeline.hide_picked_point()
        elif self.state.picker_mode == const.PickerModes.Cells:
            message = self.pipeline.get_picked_cell_info(image_data, x, y)

            if message:
                self.state.update({
                    "picker_info_title": self.state.language["cell_info_title"],
                    "picker_info_message": message,
                    "picker_info_style": style.TOOLTIP,
                })

                cell_id = message["Id"]
                cell_bounds = image_data.GetCell(cell_id).GetBounds()
                self.pipeline.show_picked_cell(cell_bounds)
            else:
                self.pipeline.hide_picked_cell()

        _, _, group, _ = self.current_file_info
        self.update_client_camera(group)

    def on_interaction(client_camera, **kwargs):
        if self.state.ui_off:
            return
        
        self.pipeline.set_camera_to_client_view(client_camera)
        
        _, _, group, _ = self.current_file_info
        group.current_view = self.pipeline.get_camera_params()
    
    with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
        view = vtk.VtkLocalView(
            self.pipeline.render_window,
            widgets=[self.pipeline.axes_widget],
            interactor_events=("events", ["LeftButtonPress", "EndAnimation"]),
            LeftButtonPress=(on_picker, "[utils.vtk.event($event)]"),
            EndAnimation=(on_interaction, "[$event.pokedRenderer.getActiveCamera().get()]")
        )
        self.ctrl.update = view.update
        self.ctrl.push_camera = view.push_camera
