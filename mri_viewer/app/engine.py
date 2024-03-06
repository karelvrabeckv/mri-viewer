from trame.app import asynchronous, get_server
from trame.decorators import hot_reload, change, TrameApp
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import html, trame, vuetify3

from asyncio import sleep
from pathlib import Path

from mri_viewer.app.assets import *
from mri_viewer.app.components.buttons import *
from mri_viewer.app.components.icons import *
from mri_viewer.app.components.interactions import *
from mri_viewer.app.components.selects import *
from mri_viewer.app.components import *
from mri_viewer.app.files import *
from mri_viewer.app.localization import *
from mri_viewer.app.pipelines import *

from mri_viewer.app.watchdog import watchdog

import mri_viewer.app.constants as const
import mri_viewer.app.styles as style

@TrameApp()
class MRIViewerApp:
    def __init__(self, server=None):
        self.__server = get_server(server, client_type="vue3")
        self.__server.enable_module({ "serve": { "docs": str(Path(__file__).parent.resolve() / "docs") } })
        
        self.__file_manager = FileManager()
        self.__language_manager = LanguageManager()
        self.__pipeline = Pipeline()
        
        self.__current_file_info = None
        
        if const.DEBUG_MODE:
            self.build_ui = hot_reload(self.build_ui)
            self.__ui = self.build_ui()
            watchdog(self)
        else:
            self.__ui = self.build_ui()
        
        self.state.trame__title = const.APPLICATION_NAME
        self.state.trame__favicon = asset_manager.logo
        
        self.state.language = self.__language_manager.get_language()
        self.state.user_guide_url = self.__language_manager.get_user_guide_url()

        self.state.player_on = False
        self.state.player_loop = False
        self.state.dialog_on = True
        
        self.state.ui_player_off = True
        self.state.ui_picker_modes_off = True
        self.state.ui_off = True

        self.state.current_zoom_factor = const.DEFAULT_ZOOM_FACTOR
        self.state.current_translation_factor = const.DEFAULT_TRANSLATION_FACTOR
        self.state.current_rotation_factor = const.DEFAULT_ROTATION_FACTOR

        self.state.picker_info_title = None
        self.state.picker_info_message = {}
        self.state.picker_info_style = style.HIDDEN

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
    def pipeline(self):
        return self.__pipeline

    @property
    def current_file_info(self):
        return self.__current_file_info

    @property
    def ui(self):
        return self.__ui

    """ Load all files from local computer uploaded by user. """
    @change("files_from_pc")
    def on_files_from_pc_change(self, files_from_pc, **kwargs):
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
    
    """ Load file from url typed by user. """
    def on_file_from_url_load(self):
        try:
            self.__file_manager.load_file_from_url(self.state.file_from_url)
            self.post_loading_actions()
        except Exception as e:
            self.state.file_from_url_error_message = f"{self.state.language['load_file_from_url_error']} {str(e)}"

    """ Actions to be executed after loading file/s. """
    def post_loading_actions(self):
        if self.state.current_file_name:
            # The user is trying to load another files
            self.toggle_player_ui()
        
        self.state.update({
            "dialog_on": False,
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

        old_file_info = self.__current_file_info
        self.__current_file_info = self.__file_manager.get_file(current_file_name)
        new_file_info = self.__current_file_info

        if not old_file_info:
            # There are no files so far
            self.load_file_at_startup()
        else:
            # There are already some files
            _, _, _, old_group_index = old_file_info
            _, _, _, new_group_index = new_file_info

            if old_group_index == new_group_index:
                # Switching files within same group
                self.load_file_from_same_group()
            else:
                # Switching files between different groups
                self.load_file_from_different_group()

    def load_file_at_startup(self):
        file, _, group, _ = self.__current_file_info
        
        self.__pipeline.render_file(file, group)
        
        group.default_view = self.__pipeline.get_camera_params()
        group.current_view = self.__pipeline.get_camera_params()
        
        self.update_client_camera(group)
        self.ctrl.push_camera()

        self.toggle_player_ui()

        self.state.update({
            "ui_off": False,
            "current_data_array": group.data_array,
            "current_data_array_items": group.data_arrays,
            "current_representation": group.representation,
            "current_slice_orientation": group.slice_orientation,
        })

    def load_file_from_same_group(self):
        file, _, group, _ = self.__current_file_info
        
        self.__pipeline.hide_current_file()
        self.__pipeline.set_camera_to_initial_view()
        
        self.__pipeline.render_file(file, group)
        self.__pipeline.render_data_array(file, group.data_array)
        self.__pipeline.render_representation(group.representation)
        
        self.__pipeline.set_slice(file, group.slice_orientation, group.slice_position)
        
        self.update_client_camera(group)
        
        self.toggle_player_ui()
        self.state.picker_info_style = style.HIDDEN

    def load_file_from_different_group(self):
        file, _, group, _ = self.__current_file_info
        
        self.__pipeline.hide_current_file()
        self.__pipeline.set_camera_to_initial_view()
        
        self.__pipeline.render_file(file, group)
        self.__pipeline.render_data_array(file, group.data_array)
        self.__pipeline.render_representation(group.representation)
        
        self.__pipeline.set_slice(file, group.slice_orientation, group.slice_position)

        if group.default_view is None:
            group.default_view = self.__pipeline.get_camera_params()
            group.current_view = self.__pipeline.get_camera_params()
        else:
            self.__pipeline.set_camera_to_group_current_view(group)

        self.update_client_camera(group)
        self.ctrl.push_camera()
        
        self.toggle_player_ui()
        self.state.picker_info_style = style.HIDDEN
        
        self.state.update({
            "current_data_array": group.data_array,
            "current_data_array_items": group.data_arrays,
            "current_representation": group.representation,
            "current_slice_orientation": group.slice_orientation,
            "current_min_slice_position": group.deduce_min_slice_position(group.slice_orientation),
            "current_slice_position": group.slice_position[group.slice_orientation],
            "current_max_slice_position": group.deduce_max_slice_position(group.slice_orientation),
        })

    @change("current_data_array")
    def on_current_data_array_change(self, current_data_array: str, **kwargs):
        if current_data_array is None:
            return
        
        file, _, group, _ = self.__current_file_info
        group.data_array = current_data_array
        
        self.__pipeline.render_data_array(file, group.data_array)
        
        self.update_client_camera(group)

    @change("current_representation")
    def on_current_representation_change(self, current_representation: str, **kwargs):
        if current_representation is None:
            return
        
        _, _, group, _ = self.__current_file_info
        group.representation = current_representation
        
        self.__pipeline.render_representation(group.representation)
        
        self.toggle_picker_modes_ui()

        self.update_client_camera(group)

    @change("current_slice_orientation")
    def on_current_slice_orientation_change(self, current_slice_orientation: str, **kwargs):
        if current_slice_orientation is None:
            return
        
        file, _, group, _ = self.__current_file_info
        group.slice_orientation = current_slice_orientation

        self.state.update({
            "current_min_slice_position": group.deduce_min_slice_position(group.slice_orientation),
            "current_slice_position": group.slice_position[group.slice_orientation],
            "current_max_slice_position": group.deduce_max_slice_position(group.slice_orientation),
        })

        self.__pipeline.set_slice(file, group.slice_orientation, group.slice_position)
        self.update_client_camera(group)

    @change("current_slice_position")
    def on_current_slice_position_change(self, current_slice_position: int, **kwargs):
        if current_slice_position is None:
            return

        file, _, group, _ = self.__current_file_info
        group.slice_position[group.slice_orientation] = current_slice_position

        self.__pipeline.set_slice(file, group.slice_orientation, group.slice_position)
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
 
        if self.state.current_file_name:
            self.__pipeline.render()
            
            _, _, group, _ = self.__current_file_info
            self.update_client_camera(group)

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

        self.__pipeline.resize_window(width, height)

    @change("picker_mode")
    def on_picker_mode_change(self, picker_mode, **kwargs):
        self.__pipeline.hide_picked_point()
        self.__pipeline.hide_picked_cell()

        self.state.update({
            "picker_info_title": "",
            "picker_info_message": {},
            "picker_info_style": style.HIDDEN,
        })

        if self.state.current_file_name:
            _, _, group, _ = self.current_file_info
            self.update_client_camera(group)

    @change("player_on")
    @asynchronous.task
    async def on_player_on_change(self, player_on, **kwargs):
        if not self.state.player_loop:
            while self.state.player_on:
                self.state.player_loop = True
                
                _, file_index, group, _ = self.__current_file_info
                
                next_file_index = file_index + 1
                if next_file_index >= group.get_num_of_files():
                    next_file_index = 0
                
                group_file_names = group.get_all_file_names() 
                self.state.current_file_name = group_file_names[next_file_index]
                
                self.state.flush()

                await sleep(0.2)
            self.state.player_loop = False

    def update_client_camera(self, group):
        self.__pipeline.set_camera_to_group_default_view(group)
        self.ctrl.update()
        self.__pipeline.set_camera_to_group_current_view(group)

    def toggle_player_ui(self):
        _, _, group, _ = self.__current_file_info
        
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
            self.__pipeline.hide_picked_point()
            self.__pipeline.hide_picked_cell()

            self.state.update({
                "ui_picker_modes_off": True,
                "picker_info_style": style.HIDDEN,
            })
        else:
            self.state.update({
                "ui_picker_modes_off": False,
            })

        _, _, group, _ = self.current_file_info
        self.update_client_camera(group)

    def build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self.server, vuetify_config=const.VUETIFY_CONFIG) as layout:
            layout.root.theme = ("theme", const.DEFAULT_THEME)
            
            # Icon
            with layout.icon as icon:
                icon.click = None
                with html.A(href="https://www.ikem.cz/", target="_blank", classes="d-flex align-center"):
                    html.Img(src=asset_manager.logo, height=48)

            # Title
            with layout.title as title:
                title.set_text(const.APPLICATION_NAME)
            
            # Toolbar
            with layout.toolbar:
                load_files_dialog(self)
                user_guide_button()
                
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
                        with vuetify3.VCardText():
                            with vuetify3.Template(v_for="value, key in picker_info_message"):
                                html.Pre("<b>{{ key }}:</b> {{ value }}")

            # Footer
            layout.footer.hide()

            return layout
