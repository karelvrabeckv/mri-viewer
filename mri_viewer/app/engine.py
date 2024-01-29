from trame.app import get_server
from trame.decorators import TrameApp, change, life_cycle
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vuetify3, vtk

from .components.axes_icon import axes_icon
from .components.progress_bar import progress_bar
from .components.upload_vti_files import upload_vti_files
from .components.slice_position_slider import slice_position_slider
from .components.selects.vti_file_select import vti_file_select
from .components.selects.data_array_select import data_array_select
from .components.selects.representation_select import representation_select
from .components.selects.slice_orientation_select import slice_orientation_select

from .constants import (
    APPLICATION_NAME,
    DEFAULT_PLANE,
    Representation,
    Planes,
) 

from .files.file_manager import FileManager
from .pipelines.vti_pipeline import VTIPipeline

@TrameApp()
class MRIViewerApp:
    def __init__(self, server=None):
        self._server = get_server(server, client_type="vue3")
        self._file_manager = FileManager()
        self._pipeline = VTIPipeline()
        self._ui = self._build_ui()
        
        self.state.trame__title = APPLICATION_NAME

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self._server.state

    @property
    def ctrl(self):
        return self._server.controller

    @change("current_vti_files")
    def on_current_vti_files_change(self, current_vti_files, **kwargs):
        if current_vti_files is None:
            return
        
        # Load VTI files selected by a user
        self._file_manager.load_new_files(current_vti_files)
        
        self.state.current_vti_files = None
        self.state.current_vti_file = self._file_manager.get_first_file_name()
        self.state.current_vti_file_items = self._file_manager.get_all_file_names()
        
    @change("current_vti_file")
    def on_current_vti_file_change(self, current_vti_file: str, **kwargs):
        if current_vti_file is None:
            return
        
        # Render the particular VTI file
        file, group = self._file_manager.get_file(current_vti_file)
        self._pipeline.set_file(file, group.active_array)
        
        self.state.current_data_array = group.active_array
        self.state.current_data_array_items = group.data_arrays
        self.state.current_representation = group.active_representation
        
        if self.state.ui_disabled == True:
            self.ctrl.push_camera()
        self.state.ui_disabled = False
        
        self.ctrl.update()

    @change("current_data_array")
    def on_current_data_array_change(self, current_data_array: str, **kwargs):
        if current_data_array is None:
            return
        
        # Render the particular data array of the VTI file
        file, group = self._file_manager.get_file(self.state.current_vti_file)
        self._pipeline.set_data_array(file, current_data_array)
        
        # Set the data array as the default of the group
        group.active_array = current_data_array
        
        self.ctrl.update()

    @change("current_representation")
    def on_current_representation_change(self, current_representation: int, **kwargs):
        if current_representation is None:
            return
        
        # Render the particular representation of the VTI file
        _, group = self._file_manager.get_file(self.state.current_vti_file)
        self._pipeline.set_representation(current_representation)
        
        # Set the representation as the default of the group
        group.active_representation = current_representation
        
        if current_representation == Representation.Slice:
            self.state.current_slice_orientation = DEFAULT_PLANE
            self.state.ui_slice_classes = "ma-4"
            
            self._pipeline.actor.VisibilityOff()
            self._pipeline.sliced_actor.VisibilityOn()
        else:
            self.state.current_slice_orientation = None
            self.state.ui_slice_classes = "ma-4 d-none"
        
        self.ctrl.update()
        
    @change("current_slice_orientation")
    def on_current_slice_orientation_change(self, current_slice_orientation, **kwargs):
        if current_slice_orientation is None:
            return

        # Set the orientation of the slice plane
        self._pipeline.set_slice_orientation(current_slice_orientation)

        # Set values for the slider
        min_x, max_x, min_y, max_y, min_z, max_z = self._pipeline.actor.GetBounds()
        
        if current_slice_orientation == Planes.XY:
            self.state.slider_range_min = min_z
            self.state.slider_range_max = max_z
            self.state.current_slice_position = min_z
        elif current_slice_orientation == Planes.YZ:
            self.state.slider_range_min = min_x
            self.state.slider_range_max = max_x
            self.state.current_slice_position = min_x
        elif current_slice_orientation == Planes.XZ:
            self.state.slider_range_min = min_y
            self.state.slider_range_max = max_y
            self.state.current_slice_position = min_y

        self.ctrl.update()
        
    @change("current_slice_position")
    def on_current_slice_position_change(self, current_slice_position, **kwargs):
        if current_slice_position is None:
            return

        # Set the position of the slice plane
        current_slice_orientation = self.state.current_slice_orientation
        self._pipeline.set_slice_position(current_slice_orientation, current_slice_position)
        
        self.ctrl.update()        

    @change("axes_visibility")
    def on_axes_visibility_change(self, axes_visibility, **kwargs):
        # Set the visibility of the coordinate axes
        self._pipeline.set_axes_visibility(axes_visibility)
        
        self.ctrl.update()

    def on_push_camera_icon_click(self, **kwargs):
        self.ctrl.push_camera()

    @life_cycle.server_reload
    def _build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self._server) as layout:
            layout.title.set_text(APPLICATION_NAME)
            
            # Toolbar
            with layout.toolbar:
                vuetify3.VSpacer()
                vuetify3.VDivider(vertical=True, classes="mx-1")
                axes_icon()
                with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), click=self.on_push_camera_icon_click):
                    vuetify3.VIcon("mdi-crop-free")
                progress_bar()

            # Sidebar
            with layout.drawer:
                upload_vti_files()
                vuetify3.VDivider()
                vti_file_select()
                vuetify3.VDivider()
                data_array_select()
                vuetify3.VDivider()
                representation_select()
                vuetify3.VDivider()
                slice_orientation_select()
                slice_position_slider()

            # Content
            with layout.content:
                with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    view = vtk.VtkLocalView(self._pipeline.render_window)
                    self.ctrl.update = view.update
                    self.ctrl.push_camera = view.push_camera

            # Footer
            layout.footer.hide()

            return layout
