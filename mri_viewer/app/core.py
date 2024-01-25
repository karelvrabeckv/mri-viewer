from trame.app import get_server
from trame.decorators import TrameApp, change, life_cycle
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vuetify3, vtk

from .components.axes_icon import axes_icon
from .components.progress_bar import progress_bar
from .components.upload_vti_files import upload_vti_files
from .components.vti_file_select import vti_file_select
from .components.data_array_select import data_array_select
from .components.representation_select import representation_select

from .constants import APPLICATION_NAME

from .vti_file_manager import VTIFileManager
from .vti_pipeline import VTIPipeline

@TrameApp()
class MRIViewerApp:
    def __init__(self, server=None):
        self._server = get_server(server, client_type="vue3")
        self._file_manager = VTIFileManager()
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
        
        self._file_manager.load_input_files(current_vti_files)
        
        self.state.selectors_disabled = False
        self.state.current_vti_files = None
        self.state.current_vti_file = self._file_manager.get_first_file_name()
        self.state.current_vti_file_items = self._file_manager.get_all_file_names()
        
    @change("current_vti_file")
    def on_current_vti_file_change(self, current_vti_file, **kwargs):
        if current_vti_file is None:
            return
        
        file = self._file_manager.get_file(current_vti_file)
        data_array = self._file_manager.group_active_array
        self._pipeline.set_file(file, data_array)
        self.ctrl.push_camera()
        
        if data_array not in file.data_arrays:
            self.state.current_data_array = file.active_array
            self.state.current_data_array_items = file.data_arrays
        else:
            self.state.current_data_array = self._file_manager.group_active_array
            self.state.current_data_array_items = self._file_manager.group_data_arrays
        
        self.ctrl.view_update()

    @change("current_data_array")
    def on_current_data_array_change(self, current_data_array, **kwargs):
        if current_data_array is None:
            return
        
        file = self._file_manager.get_file(self.state.current_vti_file)
        self._pipeline.set_data_array(file, current_data_array)
        
        self._file_manager.group_active_array = current_data_array
        self.state.current_representation = self._file_manager.group_active_representation
        self.ctrl.view_update()

    @change("current_representation")
    def on_current_representation_change(self, current_representation, **kwargs):
        if current_representation is None:
            return
        
        self._file_manager.group_active_representation = current_representation
        self._pipeline.set_representation(current_representation)
        self.ctrl.view_update()

    @change("axes_visibility")
    def on_axes_visibility_change(self, axes_visibility, **kwargs):
        self._pipeline.axes_actor.SetVisibility(axes_visibility)
        self.ctrl.view_update()

    @life_cycle.server_reload
    def _build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self._server) as layout:
            layout.title.set_text(APPLICATION_NAME)
            
            # Toolbar
            with layout.toolbar:
                vuetify3.VSpacer()
                vuetify3.VDivider(vertical=True, classes="mx-1")
                axes_icon()
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

            # Content
            with layout.content:
                with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    view = vtk.VtkLocalView(self._pipeline.render_window)
                    self.ctrl.view_update = view.update
                    self.ctrl.push_camera = view.push_camera

            # Footer
            # layout.footer.hide()

            return layout
