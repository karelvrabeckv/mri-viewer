from trame.app import asynchronous, get_server
from trame.decorators import change, life_cycle, TrameApp
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import html, trame, vuetify3

from asyncio import sleep

from mri_viewer.app.assets import *
from mri_viewer.app.components.icons import *
from mri_viewer.app.components.interactions import *
from mri_viewer.app.components.selects import *
from mri_viewer.app.components import *
from mri_viewer.app.files import *
from mri_viewer.app.localization import *
from mri_viewer.app.pipelines import *

import mri_viewer.app.constants as const
import mri_viewer.app.styles as style

@TrameApp()
class MRIViewerApp:
    def __init__(self, server=None):
        self._server = get_server(server, client_type="vue3")
        self._file_manager = FileManager()
        self._language_manager = LanguageManager()
        self._pipeline = Pipeline()
        self._ui = self._build_ui()
        
        self._current_file: File = None
        self._current_file_index: int = None
        self._current_group: FileGroup = None
        self._current_group_index: int = None
        
        self.state.trame__title = const.APPLICATION_NAME
        self.state.trame__favicon = asset_manager.favicon
        
        self.state.language = self._language_manager.get_language()

        self.state.player_on = False
        self.state.player_loop = False
        self.state.axes_on = True
        self.state.dialog_on = True
        self.state.ui_player_off = True
        self.state.ui_picker_modes_off = True
        self.state.ui_off = True

        self.state.current_zoom_factor = const.DEFAULT_ZOOM_FACTOR
        self.state.current_translation_factor = const.DEFAULT_TRANSLATION_FACTOR
        self.state.current_rotation_factor = const.DEFAULT_ROTATION_FACTOR

        self.state.picker_info_title = None
        self.state.picker_info_message = None
        self.state.picker_info_style = style.HIDDEN

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self._server.state

    @property
    def ctrl(self):
        return self._server.controller
    
    @property
    def pipeline(self):
        return self._pipeline
    
    @property
    def current_file_information(self):
        return self._current_file, self._current_file_index, self._current_group, self._current_group_index

    @change("uploaded_files")
    def on_uploaded_files_change(self, uploaded_files, **kwargs):
        if uploaded_files is None:
            return

        # Load all the files uploaded by a user        
        self._file_manager.load_new_files(uploaded_files)
        
        if self.state.current_file_name:
            # The user is trying to load another files
            self.toggle_player_ui()
        
        self.state.dialog_on = False
        self.state.uploaded_files = None
        self.state.current_file_name = self._file_manager.get_first_file_name()
        self.state.current_file_name_items = self._file_manager.get_all_file_names()

    @change("current_file_name")
    def on_current_file_name_change(self, current_file_name: str, **kwargs):
        if current_file_name is None:
            return

        self.load_current_file_information()
        file, _, group, _ = self.current_file_information

        self.state.current_data_array = group.data_array
        self.state.current_data_array_items = group.data_arrays
        self.state.current_representation = group.representation
        self.state.current_slice_orientation = group.slice_orientation
        self.state.current_slice_position = group.slice_position

        # Update the server camera
        self._pipeline.set_camera_to_initial_view()
        self._pipeline.render_file(file, group.data_array, group.slice_orientation, group.slice_position)

        if group.default_view is None:
            # Save current camera parameters
            group.default_view = self._pipeline.get_camera_params()
            group.current_view = self._pipeline.get_camera_params()
        else:
            # Load saved camera parameters
            self._pipeline.set_camera_to_group_current_view(group)

        if not self.state.player_on:
            # Transfer camera from server to client
            self.ctrl.push_camera()
                
        self.update_client_camera(group)
        
        # Activate the rest of UI
        self.state.ui_off = False
        self.toggle_player_ui()
        
        # Hide the point/cell information
        self.state.picker_info_style = style.HIDDEN

    @change("current_data_array")
    def on_current_data_array_change(self, current_data_array: str, **kwargs):
        if current_data_array is None:
            return
        
        # Render the particular data array
        file, _, group, _ = self.current_file_information
        self._pipeline.render_data_array(file, current_data_array)
        
        # Set the data array as the default of the group
        group.data_array = current_data_array
        
        self.update_client_camera(group)

    @change("current_representation")
    def on_current_representation_change(self, current_representation: int, **kwargs):
        if current_representation is None:
            return
        
        # Render the particular representation
        _, _, group, _ = self.current_file_information
        self._pipeline.render_representation(current_representation)
        
        # Set the representation as the default of the group
        group.representation = current_representation
        
        if current_representation == const.Representation.Slice:
            self._pipeline.actor.VisibilityOff()
            self._pipeline.slice_actor.VisibilityOn()
        
        self.toggle_picker_modes_ui()

        self.update_client_camera(group)

    @change("current_slice_orientation")
    def on_current_slice_orientation_change(self, current_slice_orientation, **kwargs):
        if current_slice_orientation is None:
            return
        
        file, _, group, _ = self.current_file_information
        image_data = file.reader.GetOutput()
        max_x, max_y, max_z = image_data.GetDimensions()

        # Set values for the slider
        self.state.min_slice_position = 0
        
        if current_slice_orientation == const.Planes.XY:
            self.state.max_slice_position = max_z - 1
        elif current_slice_orientation == const.Planes.YZ:
            self.state.max_slice_position = max_x - 1
        elif current_slice_orientation == const.Planes.XZ:
            self.state.max_slice_position = max_y - 1
            
        self.state.current_slice_position = const.DEFAULT_SLICE_POSITION

        # Render the particular slice
        self._pipeline.render_slice(current_slice_orientation, const.DEFAULT_SLICE_POSITION, max_x, max_y, max_z)

        # Set the slice orientation as the default of the group
        group.slice_orientation = current_slice_orientation

        self.update_client_camera(group)

    @change("current_slice_position")
    def on_current_slice_position_change(self, current_slice_position, **kwargs):
        if current_slice_position is None:
            return

        file, _, group, _ = self.current_file_information
        image_data = file.reader.GetOutput()
        max_x, max_y, max_z = image_data.GetDimensions()

        # Render the particular slice
        self._pipeline.render_slice(group.slice_orientation, current_slice_position, max_x, max_y, max_z)
        
        # Set the slice position as the default of the group
        group.slice_position = current_slice_position
        
        self.update_client_camera(group)

    @change("current_language")
    def on_current_language_change(self, current_language, **kwargs):
        # Load the vocabulary of the current language
        self._language_manager.language = current_language
        self.state.language = self._language_manager.get_language()
        
        # Change the titles of axes
        self._pipeline.cube_axes_actor.SetXTitle(self.state.language["x_axis_title"])
        self._pipeline.cube_axes_actor.SetYTitle(self.state.language["y_axis_title"])
        self._pipeline.cube_axes_actor.SetZTitle(self.state.language["z_axis_title"])

        # Change the title of picker information
        if self.state.picker_mode == const.PickerModes.Points:
            self.state.picker_info_title = self.state.language["point_information_title"]
        elif self.state.picker_mode == const.PickerModes.Cells:
            self.state.picker_info_title = self.state.language["cell_information_title"]
 
        if self.state.current_file_name:
            # Update the server camera
            self._pipeline.render_window.Render()
            
            # Update the client camera
            _, _, group, _ = self.current_file_information
            self.update_client_camera(group)

    @change("content_size")
    def on_content_size_change(self, content_size, **kwargs):
        if content_size is None:
            return
        
        size = content_size.get("size")
        pixel_ratio = content_size.get("pixelRatio")
        
        width = int(size["width"] * pixel_ratio)
        height = int(size["height"] * pixel_ratio)

        self._pipeline.render_window.SetSize(width, height)
        self._pipeline.render_window.Render()

    @change("picker_mode")
    def on_picker_mode_change(self, picker_mode, **kwargs):
        self.state.picker_info_title = ""
        self.state.picker_info_message = ""
        self.state.picker_info_style = style.HIDDEN

    @change("theme")
    def on_theme_change(self, theme, **kwargs):
        if theme == const.Theme.Light:
            self.state.icon = asset_manager.icon_dark
        else:
            self.state.icon = asset_manager.icon_light

    @change("player_on")
    @asynchronous.task
    async def on_player_on_change(self, player_on, **kwargs):
        if not self.state.player_loop:
            while self.state.player_on:
                self.state.player_loop = True
                
                _, file_index, group, _ = self.current_file_information
                
                next_file_index = file_index + 1
                if next_file_index >= group.get_num_of_files():
                    next_file_index = 0
                
                group_file_names = group.get_all_file_names() 
                self.state.current_file_name = group_file_names[next_file_index]
                
                self.state.flush()

                await sleep(0.25)
            self.state.player_loop = False

    def load_current_file_information(self):
        file, file_index, group, group_index = self._file_manager.get_file(self.state.current_file_name)

        self._current_file = file
        self._current_file_index = file_index
        self._current_group = group
        self._current_group_index = group_index

    def update_client_camera(self, group: FileGroup):
        self._pipeline.set_camera_to_group_default_view(group)
        self.ctrl.update()
        self._pipeline.set_camera_to_group_current_view(group)

    def toggle_player_ui(self):
        _, _, group, _ = self.current_file_information
        
        if group.get_num_of_files() > 1:
            # Activate the player UI
            self.state.ui_player_off = False
        else:
            # Deactivate the player UI
            self.state.ui_player_off = True

    def toggle_picker_modes_ui(self):
        player_on = self.state.player_on
        current_representation = self.state.current_representation
        
        if player_on or current_representation == const.Representation.Slice:
            self.state.ui_picker_modes_off = True
        else:
            self.state.ui_picker_modes_off = False

    @life_cycle.server_reload
    def _build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self._server, vuetify_config=const.VUETIFY_CONFIG) as layout:
            layout.root.theme = ("theme", const.DEFAULT_THEME)
            
            # Icon
            with layout.icon as icon:
                icon.click = None
                with html.A(href="https://www.ikem.cz/", target="_blank"):
                    html.Img(src=("icon",), height=35)

            # Title
            with layout.title as title:
                title.set_text(const.APPLICATION_NAME)
            
            # Toolbar
            with layout.toolbar:
                load_files_dialog(self)
                
                animation_icons(self)
                
                picker_modes_icons()
                toolbar_icons(self)
                language_buttons()
                
                progress_bar()

            # Sidebar
            with layout.drawer:
                file_name_select()
                data_array_select()
                representation_select()
                
                slice_interaction()
                
                zoom_interaction(self)
                translation_interaction(self)
                rotation_interaction(self)

            # Content
            with layout.content:
                with trame.SizeObserver("content_size"):
                    view(self)

                    # Picker information
                    with vuetify3.VCard(title=("picker_info_title",), style=("picker_info_style",)):
                        vuetify3.VCardText("<pre>{{ picker_info_message }}</pre>")

            # Footer
            layout.footer.hide()

            return layout
