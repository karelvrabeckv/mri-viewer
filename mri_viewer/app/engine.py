from trame.app import asynchronous, get_server
from trame.decorators import hot_reload, change, TrameApp
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import trame, vuetify3

from asyncio import sleep
from pathlib import Path

from vtkmodules.vtkCommonTransforms import vtkTransform

from mri_viewer.app.components.buttons import (
    language_buttons,
    user_guide_button,
)
from mri_viewer.app.components.icons.groups import (
    picker_modes_icons,
    player_icons,
    toolbar_icons,
)
from mri_viewer.app.components.icons import (
    logo,
)
from mri_viewer.app.components.interactions import (
    rotation_tool,
    slice_tool,
    translation_tool,
    zoom_tool,
)
from mri_viewer.app.components.selects import (
    data_array_select,
    file_name_select,
    representation_select,
    color_map_select,
)
from mri_viewer.app.components import (
    load_files_dialog,
    picker_info,
    progress_bar,
    visualization,
)

from mri_viewer.app.assets import AssetManager
from mri_viewer.app.files import FileManager
from mri_viewer.app.localization import LanguageManager
from mri_viewer.app.vtk import VTKManager

from mri_viewer.app.watchdog import watchdog
from mri_viewer.app.styles import HIDDEN, PICKER_INFO

import mri_viewer.app.constants as const

@TrameApp()
class MRIViewerApp:
    def __init__(self, server=None):
        self.__server = get_server(server)
        self.__server.enable_module({ "serve": { "docs": str(Path(__file__).parent.resolve() / "docs") } })
        
        self.__asset_manager = AssetManager()
        self.__file_manager = FileManager()
        self.__language_manager = LanguageManager()
        self.__vtk_manager = VTKManager()
        
        # ========================================
        # State
        # ========================================
        
        self.state.trame__title = const.APPLICATION_NAME
        self.state.trame__favicon = self.__asset_manager.assets.logo
        
        self.state.language = self.__language_manager.get_language()
        self.state.user_guide_url = self.__language_manager.get_user_guide_url()

        self.state.player_on = False
        self.state.player_loop = False
        self.state.dialog_on = True
        
        self.state.loading_option = const.LoadingOptions.Default
        
        self.state.ui_player_off = True
        self.state.ui_picker_modes_off = True
        self.state.ui_off = True

        self.state.current_zoom_factor = const.ZoomParams.Default
        self.state.current_translation_factor = const.TranslationParams.Default
        self.state.current_rotation_factor = const.RotationParams.Default

        self.state.picker_info_title = None
        self.state.picker_info_message = {}
        self.state.picker_info_style = HIDDEN

        # ========================================
        # Controller
        # ========================================

        self.ctrl.on_previous_file = self.on_previous_file
        self.ctrl.on_toggle_player = self.on_toggle_player
        self.ctrl.on_next_file = self.on_next_file

        self.ctrl.on_toggle_axes_info = self.on_toggle_axes_info
        self.ctrl.on_reset_camera = self.on_reset_camera
        self.ctrl.on_change_theme = self.on_change_theme

        self.ctrl.zoom = self.zoom
        self.ctrl.translate = self.translate
        self.ctrl.rotate = self.rotate

        self.ctrl.close_dialog = self.close_dialog
        self.ctrl.clear_files_from_pc_error_message = self.clear_files_from_pc_error_message
        self.ctrl.on_file_from_url_load = self.on_file_from_url_load

        self.ctrl.on_picker = self.on_picker
        self.ctrl.on_interaction = self.on_interaction

        # ========================================
        # UI
        # ========================================

        self.__ui = self.build_ui()
        if const.DEVELOPER_MODE:
            watchdog(self)

    @property
    def server(self):
        return self.__server

    @property
    def state(self):
        return self.__server.state

    @property
    def ctrl(self):
        return self.__server.controller
    
    @property
    def asset_manager(self):
        return self.__asset_manager

    @property
    def file_manager(self):
        return self.__file_manager

    @property
    def language_manager(self):
        return self.__language_manager

    @property
    def vtk_manager(self):
        return self.__vtk_manager

    @property
    def ui(self):
        return self.__ui

    @change("files_from_pc")
    def on_files_from_pc_change(self, files_from_pc, **kwargs):
        """ Load all files from local computer uploaded by user. """

        if files_from_pc is None:
            return
        
        try:
            self.__file_manager.load_files_from_pc(files_from_pc)
            self.post_loading_actions()
        except Exception as e:
            self.state.files_from_pc_error_message = f"{self.state.language['load_files_from_pc_error']} {str(e)}"

    def clear_files_from_pc_error_message(self):
        self.state.files_from_pc = None
        self.state.files_from_pc_error_message = ""

    @change("file_from_url")
    def on_file_from_url_change(self, file_from_url, **kwargs):
        self.state.file_from_url_error_message = ""
    
    def on_file_from_url_load(self):
        """ Load file from url typed by user. """

        try:
            self.__file_manager.load_file_from_url(self.state.file_from_url)
            self.post_loading_actions()
        except Exception as e:
            self.state.file_from_url_error_message = f"{self.state.language['load_file_from_url_error']} {str(e)}"

    def post_loading_actions(self):
        """ Actions to be executed after loading file/s. """

        if self.state.current_file_name:
            # The user is trying to load another files
            self.toggle_player_ui()
        
        self.state.update({
            "dialog_on": False,
            "loading_option": const.LoadingOptions.Default,
            "files_from_pc": None,
            "files_from_pc_error_message": "",
            "file_from_url": None,
            "file_from_url_error_message": "",
            "current_file_name": self.__file_manager.file_to_show,
            "current_file_name_items": self.__file_manager.get_all_file_names(),
        })

    @change("current_file_name")
    def on_current_file_name_change(self, current_file_name: str, **kwargs):
        if current_file_name is None:
            return

        old_group_index = self.__file_manager.current_group_index
        self.__file_manager.set_as_current(current_file_name)
        new_group_index = self.__file_manager.current_group_index

        if old_group_index is None:
            # There are no files so far
            self.load_file_at_startup()
        else:
            # There are already some files
            if old_group_index == new_group_index:
                # Switching files within same group
                self.load_file_from_same_group()
            else:
                # Switching files between different groups
                self.load_file_from_different_group()

    def load_file_at_startup(self):
        file = self.__file_manager.current_file
        group = self.__file_manager.current_group
        
        self.__vtk_manager.render_file(file, group)
        
        group.default_view = self.__vtk_manager.get_camera_params()
        group.current_view = self.__vtk_manager.get_camera_params()
        
        self.update_client_camera(group)
        self.ctrl.push_camera()

        self.toggle_player_ui()

        self.state.update({
            "ui_off": False,
            "current_data_array": group.data_array,
            "current_data_array_items": group.data_arrays,
            "current_representation": group.representation,
            "current_color_map": group.color_map,
            "current_slice_orientation": group.slice_orientation,
        })

    def load_file_from_same_group(self):
        file = self.__file_manager.current_file
        group = self.__file_manager.current_group
        
        self.__vtk_manager.hide_current_file()
        self.__vtk_manager.set_camera_to_initial_view()
        
        self.__vtk_manager.render_file(file, group)
        self.__vtk_manager.render_data_array(file, group.data_array)
        self.__vtk_manager.render_representation(group.representation)
        
        self.__vtk_manager.set_slice(file, group.slice_orientation, group.slice_position)
        
        self.update_client_camera(group)
        
        self.toggle_player_ui()
        self.state.picker_info_style = HIDDEN

    def load_file_from_different_group(self):
        file = self.__file_manager.current_file
        group = self.__file_manager.current_group
        
        self.__vtk_manager.hide_current_file()
        self.__vtk_manager.set_camera_to_initial_view()
        
        self.__vtk_manager.render_file(file, group)
        self.__vtk_manager.render_data_array(file, group.data_array)
        self.__vtk_manager.render_representation(group.representation)
        
        self.__vtk_manager.set_slice(file, group.slice_orientation, group.slice_position)

        if group.default_view is None:
            group.default_view = self.__vtk_manager.get_camera_params()
            group.current_view = self.__vtk_manager.get_camera_params()
        else:
            self.__vtk_manager.set_camera_to_group_current_view(group)

        self.update_client_camera(group)
        self.ctrl.push_camera()
        
        self.toggle_player_ui()
        self.state.picker_info_style = HIDDEN
        
        self.state.update({
            "current_data_array": group.data_array,
            "current_data_array_items": group.data_arrays,
            "current_representation": group.representation,
            "current_color_map": group.color_map,
            "current_slice_orientation": group.slice_orientation,
            "current_slice_position": group.slice_position[group.slice_orientation],
            "current_slice_min": group.deduce_min_slice_position(group.slice_orientation),
            "current_slice_max": group.deduce_max_slice_position(group.slice_orientation),
            "current_slice_step": group.deduce_slice_step(group.slice_orientation),
        })

    @change("current_data_array")
    def on_current_data_array_change(self, current_data_array: str, **kwargs):
        if current_data_array is None:
            return
        
        file = self.__file_manager.current_file
        group = self.__file_manager.current_group
        group.data_array = current_data_array
        
        self.__vtk_manager.render_data_array(file, group.data_array)
        
        self.update_client_camera(group)

    @change("current_representation")
    def on_current_representation_change(self, current_representation: str, **kwargs):
        if current_representation is None:
            return
        
        self.__vtk_manager.hide_picked_point()
        self.__vtk_manager.hide_picked_cell()

        self.state.picker_info_style = HIDDEN

        group = self.__file_manager.current_group
        group.representation = current_representation
        
        self.__vtk_manager.render_representation(group.representation)
        
        self.toggle_picker_modes_ui()
        self.update_client_camera(group)

    @change("current_color_map")
    def on_current_color_map_change(self, current_color_map: str, **kwargs):
        if current_color_map is None:
            return
        
        group = self.__file_manager.current_group
        group.color_map = current_color_map

        self.__vtk_manager.render_color_map(group.color_map)

        self.update_client_camera(group)

    @change("current_slice_orientation")
    def on_current_slice_orientation_change(self, current_slice_orientation: str, **kwargs):
        if current_slice_orientation is None:
            return
        
        self.__vtk_manager.hide_picked_point()
        self.__vtk_manager.hide_picked_cell()

        file = self.__file_manager.current_file
        group = self.__file_manager.current_group
        group.slice_orientation = current_slice_orientation

        self.state.update({
            "picker_info_style": HIDDEN,
            "current_slice_position": group.slice_position[group.slice_orientation],
            "current_slice_min": group.deduce_min_slice_position(group.slice_orientation),
            "current_slice_max": group.deduce_max_slice_position(group.slice_orientation),
            "current_slice_step": group.deduce_slice_step(group.slice_orientation),
        })

        self.__vtk_manager.set_slice(file, group.slice_orientation, group.slice_position)
        self.update_client_camera(group)

    @change("current_slice_position")
    def on_current_slice_position_change(self, current_slice_position: int, **kwargs):
        if current_slice_position is None:
            return

        self.__vtk_manager.hide_picked_point()
        self.__vtk_manager.hide_picked_cell()

        self.state.picker_info_style = HIDDEN

        file = self.__file_manager.current_file
        group = self.__file_manager.current_group
        group.slice_position[group.slice_orientation] = current_slice_position

        self.__vtk_manager.set_slice(file, group.slice_orientation, group.slice_position)
        self.update_client_camera(group)

    @change("current_language")
    def on_current_language_change(self, current_language, **kwargs):
        # Load the vocabulary of the current language
        self.__language_manager.language = current_language
        self.state.language = self.__language_manager.get_language()
        self.state.user_guide_url = self.__language_manager.get_user_guide_url()
        
        # Change the title of picker information
        if self.state.picker_mode == const.PickerModes.Points:
            self.state.picker_info_title = self.state.language["point_info_title"]
        elif self.state.picker_mode == const.PickerModes.Cells:
            self.state.picker_info_title = self.state.language["cell_info_title"]
 
        # Change labels of representations
        self.state.current_representation_items = [
            {
                "title": self.state.language["representation_select_item_points"],
                "value": const.Representation.Points,
            },
            {
                "title": self.state.language["representation_select_item_slice"],
                "value": const.Representation.Slice,
            },
            {
                "title": self.state.language["representation_select_item_surface"],
                "value": const.Representation.Surface,
            },
            {
                "title": self.state.language["representation_select_item_surface_with_edges"],
                "value": const.Representation.SurfaceWithEdges,
            },
            {
                "title": self.state.language["representation_select_item_wireframe"],
                "value": const.Representation.Wireframe,
            },
        ]

        # Change labels of color maps
        self.state.current_color_map_items = [
            {
                "title": self.state.language["color_map_select_item_cool_to_warm"],
                "value": const.ColorMaps.CoolToWarm,
            },
            {
                "title": self.state.language["color_map_select_item_grayscale"],
                "value": const.ColorMaps.Grayscale,
            }
        ]

    @change("dialog_on")
    def on_dialog_on_change(self, dialog_on, **kwargs):
        if dialog_on == False:
            self.state.update({
                "files_from_pc": None,
                "files_from_pc_error_message": "",
                "file_from_url": None,
                "file_from_url_error_message": "",
            })

    @change("content_size")
    def on_content_size_change(self, content_size, **kwargs):
        if content_size is None:
            return
        
        size = content_size.get("size")
        pixel_ratio = content_size.get("pixelRatio")
        
        width = int(size["width"] * pixel_ratio)
        height = int(size["height"] * pixel_ratio)

        self.__vtk_manager.resize_window(width, height)

    @change("picker_mode")
    def on_picker_mode_change(self, picker_mode, **kwargs):
        self.__vtk_manager.hide_picked_point()
        self.__vtk_manager.hide_picked_cell()

        self.state.update({
            "picker_info_title": "",
            "picker_info_message": {},
            "picker_info_style": HIDDEN,
        })

        if self.state.current_file_name:
            group = self.__file_manager.current_group
            self.update_client_camera(group)

    @change("player_on")
    @asynchronous.task
    async def on_player_on_change(self, player_on, **kwargs):
        if not self.state.player_loop:
            while self.state.player_on:
                self.state.player_loop = True
                
                file_index = self.__file_manager.current_file_index
                group = self.__file_manager.current_group
                
                next_file_index = file_index + 1
                if next_file_index >= group.get_num_of_files():
                    next_file_index = 0
                
                # Synchronize state between client and server
                with self.state:
                    # Change current file
                    group_file_names = group.get_all_file_names()
                    self.state.current_file_name = group_file_names[next_file_index]

                # Wait for certain time interval
                await sleep(0.25)
            self.state.player_loop = False

    def update_client_camera(self, group):
        self.__vtk_manager.set_camera_to_group_default_view(group)
        self.ctrl.update()
        self.__vtk_manager.set_camera_to_group_current_view(group)

    def toggle_player_ui(self):
        group = self.__file_manager.current_group
        
        if group.get_num_of_files() > 1:
            # Activate the player UI
            self.state.ui_player_off = False
        else:
            # Deactivate the player UI
            self.state.ui_player_off = True

    def toggle_picker_modes_ui(self):
        if self.state.player_on:
            self.__vtk_manager.hide_picked_point()
            self.__vtk_manager.hide_picked_cell()

            self.state.update({
                "ui_picker_modes_off": True,
                "picker_info_style": HIDDEN,
            })
        else:
            self.state.update({
                "ui_picker_modes_off": False,
            })

        group = self.__file_manager.current_group
        self.update_client_camera(group)

    def on_previous_file(self):
        """Skip to the previous file."""

        # Turn off player
        self.state.player_on = False

        # Enable picker modes
        self.toggle_picker_modes_ui()
        
        file_index = self.__file_manager.current_file_index
        group = self.__file_manager.current_group
        
        previous_file_index = file_index - 1
        if previous_file_index < 0:
            previous_file_index = group.get_num_of_files() - 1
        
        group_file_names = group.get_all_file_names()

        # Set previous file name as current
        self.state.current_file_name = group_file_names[previous_file_index]

    def on_toggle_player(self):
        """Play or pause the player."""

        self.state.player_on = not self.state.player_on
        self.toggle_picker_modes_ui()

    def on_next_file(self):
        """Skip to the next file."""

        # Turn off player
        self.state.player_on = False

        # Enable picker modes
        self.toggle_picker_modes_ui()
        
        file_index = self.__file_manager.current_file_index
        group = self.__file_manager.current_group
        
        next_file_index = file_index + 1
        if next_file_index >= group.get_num_of_files():
            next_file_index = 0
        
        group_file_names = group.get_all_file_names()

        # Set next file name as current
        self.state.current_file_name = group_file_names[next_file_index]

    def on_toggle_axes_info(self):
        """Show or hide the axes information with a grid."""

        self.__vtk_manager.axes_info_on = not self.__vtk_manager.axes_info_on
        self.__vtk_manager.render_axes_info()
        
        group = self.__file_manager.current_group
        self.update_client_camera(group)

    def on_reset_camera(self):
        """Reset the camera."""

        group = self.__file_manager.current_group
        group.current_view = group.default_view

        self.__vtk_manager.set_camera_to_group_default_view(group)
        self.ctrl.push_camera()

    def on_change_theme(self):
        """Change the theme to light or dark."""

        if self.state.theme == const.Theme.Light:
            self.state.theme = const.Theme.Dark
        else:
            self.state.theme = const.Theme.Light

    def zoom(self, direction):
        """Zoom the camera in a given direction."""

        camera = self.__vtk_manager.camera
        
        if direction == const.Zoom.In:
            for _ in range(self.state.current_zoom_factor):
                camera.Zoom(1 + 0.1)
        elif direction == const.Zoom.Out:
            for _ in range(self.state.current_zoom_factor):
                camera.Zoom(1 - 0.1)
        
        self.__vtk_manager.camera = camera
    
        self.__vtk_manager.render()
        self.ctrl.push_camera()

        group = self.__file_manager.current_group
        group.current_view = self.__vtk_manager.get_camera_params()

    def translate(self, direction):
        """Translate the camera in a given direction."""

        camera = self.__vtk_manager.camera
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
        
        self.__vtk_manager.camera = camera
        self.__vtk_manager.render()
        self.ctrl.push_camera()
        
        group = self.__file_manager.current_group
        group.current_view = self.__vtk_manager.get_camera_params()

    def rotate(self, direction):
        """Rotate the camera in a given direction."""

        camera = self.__vtk_manager.camera
        x, y, z = self.__vtk_manager.get_file_actor_center()

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
        self.__vtk_manager.camera = camera

        self.__vtk_manager.render()
        self.ctrl.push_camera()
        
        group = self.__file_manager.current_group
        group.current_view = self.__vtk_manager.get_camera_params()

    def close_dialog(self):
        """Close the dialog for uploading files."""

        # Hide dialog
        self.state.dialog_on = False

    def on_picker(self, event, **kwargs):
        """Pick a point or cell."""

        if self.state.picker_mode == const.PickerModes.Off:
            return

        # Hide picker info
        self.state.picker_info_style = HIDDEN

        file = self.__file_manager.current_file
        image_data = file.reader.GetOutput()

        if self.state.current_representation == const.Representation.Slice:
            slice = self.__vtk_manager.get_object(const.Objects.Slice)
            image_data = slice.GetOutput()

        position = event["position"]
        x, y = position["x"], position["y"]
        
        if self.state.picker_mode == const.PickerModes.Points:
            message = self.__vtk_manager.get_picked_point_info(image_data, x, y)

            if message:
                self.state.update({
                    "picker_info_title": self.state.language["point_info_title"],
                    "picker_info_message": message,
                    "picker_info_style": PICKER_INFO,
                })

                point_id = message[const.ID]
                point_position = image_data.GetPoint(point_id)
                self.__vtk_manager.show_picked_point(point_position)
            else:
                self.__vtk_manager.hide_picked_point()
        elif self.state.picker_mode == const.PickerModes.Cells:
            message = self.__vtk_manager.get_picked_cell_info(image_data, x, y)

            if message:
                self.state.update({
                    "picker_info_title": self.state.language["cell_info_title"],
                    "picker_info_message": message,
                    "picker_info_style": PICKER_INFO,
                })

                cell_id = message[const.ID]
                cell_bounds = image_data.GetCell(cell_id).GetBounds()
                self.__vtk_manager.show_picked_cell(cell_bounds)
            else:
                self.__vtk_manager.hide_picked_cell()

        group = self.__file_manager.current_group
        self.update_client_camera(group)

    def on_interaction(self, client_camera, **kwargs):
        """Update the server camera."""

        if self.state.ui_off:
            return
        
        self.__vtk_manager.set_camera_to_client_view(client_camera)
        
        group = self.__file_manager.current_group
        group.current_view = self.__vtk_manager.get_camera_params()

    @hot_reload
    def build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self.server, vuetify_config=const.VUETIFY_CONFIG) as layout:
            layout.root.theme = ("theme", const.DEFAULT_THEME)
            
            # Icon
            with layout.icon as icon:
                icon.click = None
                logo(self.asset_manager)

            # Title
            with layout.title as title:
                title.set_text(const.APPLICATION_NAME)
            
            # Toolbar
            with layout.toolbar:
                vuetify3.VDivider(vertical=True)

                load_files_dialog(self.ctrl)
                user_guide_button()

                vuetify3.VDivider(vertical=True)

                vuetify3.VSpacer()
                player_icons(self.ctrl)
                vuetify3.VSpacer()

                vuetify3.VDivider(vertical=True)

                picker_modes_icons()

                vuetify3.VDivider(vertical=True)

                toolbar_icons(self.ctrl)

                vuetify3.VDivider(vertical=True)

                language_buttons()
                
                progress_bar()

            # Sidebar
            with layout.drawer:
                file_name_select()
                data_array_select()
                representation_select()
                color_map_select()

                vuetify3.VDivider()
                
                slice_tool()
                zoom_tool(self.ctrl)
                translation_tool(self.ctrl)
                rotation_tool(self.ctrl)

            # Content
            with layout.content:
                with trame.SizeObserver("content_size"):
                    visualization(self.ctrl, self.vtk_manager)
                    picker_info()

            # Footer
            layout.footer.hide()

            return layout
