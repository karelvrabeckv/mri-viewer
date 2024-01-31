from trame.app import get_server, asynchronous
from trame.decorators import TrameApp, change, life_cycle
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vuetify3, vtk

from asyncio import sleep

from .components.progress_bar import progress_bar
from .components.upload_vti_files import upload_vti_files
from .components.slice_position_slider import slice_position_slider
from .components.icons.animation_icons import animation_icons
from .components.icons.toolbar_icons import toolbar_icons
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
        self.state.is_playing = False
        self.state.player_loop = False
        self.state.axes = True

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
        file, _, group, _ = self._file_manager.get_file(current_vti_file)
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
        file, _, group, _ = self._file_manager.get_file(self.state.current_vti_file)
        self._pipeline.set_data_array(file, current_data_array)
        
        # Set the data array as the default of the group
        group.active_array = current_data_array
        
        self.ctrl.update()

    @change("current_representation")
    def on_current_representation_change(self, current_representation: int, **kwargs):
        if current_representation is None:
            return
        
        # Render the particular representation of the VTI file
        _, _, group, _ = self._file_manager.get_file(self.state.current_vti_file)
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

    @change("is_playing")
    @asynchronous.task
    async def on_is_playing_change(self, is_playing, **kwargs):
        if not self.state.player_loop:
            while is_playing:
                self.state.player_loop = True
                if not self.state.is_playing:
                    self.state.player_loop = False
                    break
                
                self.on_next_file()
                
                file, _, group, _ = self._file_manager.get_file(self.state.current_vti_file)
                self._pipeline.set_file(file, group.active_array)
                
                self.ctrl.update()
                
                await sleep(1)

    def on_previous_file(self, **kwargs):
        _, file_index, group, _ = self._file_manager.get_file(self.state.current_vti_file)
        
        previous_file_index = file_index - 1
        if previous_file_index < 0:
            previous_file_index = group.get_num_of_files() - 1
        
        group_file_names = group.get_all_file_names() 
        self.state.current_vti_file = group_file_names[previous_file_index]

    def on_toggle_player(self, **kwargs):
        self.state.is_playing = not self.state.is_playing

    def on_next_file(self, **kwargs):
        _, file_index, group, _ = self._file_manager.get_file(self.state.current_vti_file)
        
        next_file_index = file_index + 1
        if next_file_index >= group.get_num_of_files():
            next_file_index = 0
        
        group_file_names = group.get_all_file_names() 
        self.state.current_vti_file = group_file_names[next_file_index]
        
    def on_axes_visibility(self, **kwargs):
        self.state.axes = not self.state.axes
        self._pipeline.set_axes_visibility(self.state.axes)
        
        self.ctrl.update()

    def on_push_camera(self, **kwargs):
        self.ctrl.push_camera()

    @life_cycle.server_reload
    def _build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self._server) as layout:
            layout.title.set_text(APPLICATION_NAME)
            
            # Toolbar
            with layout.toolbar:
                vuetify3.VDivider(vertical=True, classes="mx-2")
                animation_icons(self)
                vuetify3.VDivider(vertical=True, classes="mx-2")
                toolbar_icons(self)
                progress_bar()

            # Sidebar
            with layout.drawer:
                upload_vti_files()
                vuetify3.VDivider()
                vti_file_select()
                data_array_select()
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
