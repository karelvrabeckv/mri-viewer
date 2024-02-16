from trame.widgets import vtk, vuetify3

import mri_viewer.app.constants as const
import mri_viewer.app.styles as style

def view(self):
    def on_picker(event, **kwargs):
        if self.state.picker_mode == const.PickerModes.Off:
            return

        file, _, _, _ = self.current_file_information
        image_data = file.reader.GetOutput()

        position = event["position"]
        x, y = position["x"], position["y"]
        
        if self.state.picker_mode == const.PickerModes.Points:
            self.state.picker_info_title = self.state.language["point_information_title"]
            message = self.pipeline.get_point_information(image_data, x, y)
        elif self.state.picker_mode == const.PickerModes.Cells:
            self.state.picker_info_title = self.state.language["cell_information_title"]
            message = self.pipeline.get_cell_information(image_data, x, y)
        
        self.state.picker_info_message = message
        self.state.picker_info_style = style.TOOLTIP if message else style.HIDDEN

    def on_interaction(client_camera, **kwargs):
        self.pipeline.set_camera_to_client_view(client_camera)
        
        _, _, group, _ = self.current_file_information
        group.current_view = self.pipeline.get_camera_params()
    
    with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
        view = vtk.VtkLocalView(
            self.pipeline.render_window,
            interactor_events=("events", ["LeftButtonPress", "EndAnimation"]),
            LeftButtonPress=(on_picker, "[utils.vtk.event($event)]"),
            EndAnimation=(on_interaction, "[$event.pokedRenderer.getActiveCamera().get()]")
        )
        self.ctrl.update = view.update
        self.ctrl.push_camera = view.push_camera
