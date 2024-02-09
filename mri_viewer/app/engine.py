from trame.app import get_server, asynchronous
from trame.decorators import TrameApp, change, life_cycle
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vuetify3, vtk, trame, html

from asyncio import sleep
from vtkmodules.vtkCommonTransforms import vtkTransform

from .assets import asset_manager

from .components.progress_bar import progress_bar
from .components.upload_vti_files import upload_vti_files
from .components.icons.animation_icons import animation_icons
from .components.icons.picker_modes_icons import picker_modes_icons
from .components.icons.toolbar_icons import toolbar_icons
from .components.language_buttons import language_buttons
from .components.selects.vti_file_select import vti_file_select
from .components.selects.data_array_select import data_array_select
from .components.selects.representation_select import representation_select
from .components.interaction.slice_interaction import slice_interaction
from .components.interaction.zoom_interaction import zoom_interaction
from .components.interaction.rotation_interaction import rotation_interaction
from .components.interaction.translation_interaction import translation_interaction

from .constants import (
    APPLICATION_NAME,
    DEFAULT_THEME,
    VUETIFY_CONFIG,
    DEFAULT_SLICE_ORIENTATION,
    ZOOM_FACTOR,
    TRANSLATION_FACTOR,
    Theme,
    Zoom,
    Directions,
    Representation,
    Planes,
    PickerModes,
)
from .styles import (
    TOOLTIP_STYLE,
    HIDDEN_STYLE,
)

from .files.file_manager import FileManager
from .localization.language_manager import LanguageManager
from .pipelines.vti_pipeline import VTIPipeline

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

import vtkmodules.vtkRenderingOpenGL2  # noqa

@TrameApp()
class MRIViewerApp:
    def __init__(self, server=None):
        self._server = get_server(server, client_type="vue3")
        self._file_manager = FileManager()
        self._language_manager = LanguageManager()
        self._pipeline = VTIPipeline()
        self._ui = self._build_ui()
        
        self.state.trame__title = APPLICATION_NAME
        self.state.trame__favicon = asset_manager.favicon
        
        self.state.language = self._language_manager.get_language()
        
        self.state.is_playing = False
        self.state.player_loop = False
        
        self.state.axes = True

        self.state.tooltip_title = None
        self.state.tooltip_message = None
        self.state.tooltip_style = None

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
        
        self.state.ui_disabled = False
        self.state.tooltip_style = HIDDEN_STYLE
        
        self.ctrl.push_camera()
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
            self.state.current_slice_orientation = DEFAULT_SLICE_ORIENTATION
            
            self._pipeline.actor.VisibilityOff()
            self._pipeline.slice_actor.VisibilityOn()
        else:
            self.state.current_slice_orientation = None
        
        self.ctrl.update()
        
    @change("current_slice_orientation")
    def on_current_slice_orientation_change(self, current_slice_orientation, **kwargs):
        if current_slice_orientation is None:
            return

        file, _, _, _ = self._file_manager.get_file(self.state.current_vti_file)
        image_data = file.reader.GetOutput()
        max_x, max_y, max_z = image_data.GetDimensions()

        # Set values for the slider        
        self.state.current_slice_position = 0
        self.state.slider_range_min = 0
        
        if current_slice_orientation == Planes.XY:
            self.state.slider_range_max = max_z - 1
        elif current_slice_orientation == Planes.YZ:
            self.state.slider_range_max = max_x - 1
        elif current_slice_orientation == Planes.XZ:
            self.state.slider_range_max = max_y - 1

        # Set the position of the slice plane
        self._pipeline.set_slice(self.state.current_slice_position, current_slice_orientation, max_x, max_y, max_z)

        self.ctrl.update()
        
    @change("current_slice_position")
    def on_current_slice_position_change(self, current_slice_position, **kwargs):
        if current_slice_position is None:
            return

        file, _, _, _ = self._file_manager.get_file(self.state.current_vti_file)
        image_data = file.reader.GetOutput()
        max_x, max_y, max_z = image_data.GetDimensions()

        # Set the position of the slice plane
        self._pipeline.set_slice(current_slice_position, self.state.current_slice_orientation, max_x, max_y, max_z)
        
        self.ctrl.update()

    @change("current_language")
    def on_current_language_change(self, current_language, **kwargs):
        self._language_manager.language = current_language
        self.state.language = self._language_manager.get_language()
        
        self._pipeline.cube_axes_actor.SetXTitle(self.state.language["x_axis_title"])
        self._pipeline.cube_axes_actor.SetYTitle(self.state.language["y_axis_title"])
        self._pipeline.cube_axes_actor.SetZTitle(self.state.language["z_axis_title"])

        if self.state.picker_mode == PickerModes.Points:
            self.state.tooltip_title = self.state.language["point_information_title"]
        elif self.state.picker_mode == PickerModes.Cells:
            self.state.tooltip_title = self.state.language["cell_information_title"]

        self._pipeline.render_window.Render()
        self.ctrl.update()

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
        self.state.tooltip_title = ""
        self.state.tooltip_message = ""
        self.state.tooltip_style = HIDDEN_STYLE

    @change("theme")
    def on_theme_change(self, theme, **kwargs):
        if theme == Theme.Light:
            self.state.icon = asset_manager.icon_dark
        else:
            self.state.icon = asset_manager.icon_light

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
        self.ctrl.update()

    def on_change_theme(self, **kwargs):
        if self.state.theme == Theme.Light:
            self.state.theme = Theme.Dark
        else:
            self.state.theme = Theme.Light

    def on_picker(self, event, **kwargs):
        if self.state.picker_mode == PickerModes.Off:
            return

        file, _, _, _ = self._file_manager.get_file(self.state.current_vti_file)
        image_data = file.reader.GetOutput()

        position = event["position"]
        x, y = position["x"], position["y"]
        
        if self.state.picker_mode == PickerModes.Points:
            self.state.tooltip_title = self.state.language["point_information_title"]
            message = self._pipeline.get_point_information(image_data, x, y)
        elif self.state.picker_mode == PickerModes.Cells:
            self.state.tooltip_title = self.state.language["cell_information_title"]
            message = self._pipeline.get_cell_information(image_data, x, y)
        
        self.state.tooltip_message = message
        self.state.tooltip_style = TOOLTIP_STYLE if message else HIDDEN_STYLE
  
    def on_interaction(self, client_camera, **kwargs):
        server_camera = self._pipeline.renderer.GetActiveCamera()
        
        server_camera.SetPosition(client_camera.get("position"))
        server_camera.SetFocalPoint(client_camera.get("focalPoint"))
        server_camera.SetViewUp(client_camera.get("viewUp"))
        server_camera.SetViewAngle(client_camera.get("viewAngle"))
        
        self._pipeline.renderer.ResetCameraClippingRange()
        self._pipeline.render_window.Render()

    def zoom(self, direction, **kwargs):
        camera = self._pipeline.renderer.GetActiveCamera()
        
        if direction == Zoom.In:
            camera.Zoom(1 + ZOOM_FACTOR)
        elif direction == Zoom.Out:
            camera.Zoom(1 - ZOOM_FACTOR)
        
        self._pipeline.renderer.SetActiveCamera(camera)
        self._pipeline.render_window.Render()
        self.ctrl.push_camera()

    def translate(self, direction, **kwargs):
        camera = self._pipeline.renderer.GetActiveCamera()
        camera_position = camera.GetPosition()
        focal_point_position = camera.GetFocalPoint()
        offset_x, offset_y, offset_z = 0.0, 0.0, 0.0
        
        if direction == Directions.XAxisPlus:
            offset_x -= TRANSLATION_FACTOR
        elif direction == Directions.XAxisMinus:
            offset_x += TRANSLATION_FACTOR
        elif direction == Directions.YAxisPlus:
            offset_y -= TRANSLATION_FACTOR
        elif direction == Directions.YAxisMinus:
            offset_y += TRANSLATION_FACTOR
        elif direction == Directions.ZAxisPlus:
            offset_z -= TRANSLATION_FACTOR
        elif direction == Directions.ZAxisMinus:
            offset_z += TRANSLATION_FACTOR
        
        offset = (offset_x, offset_y, offset_z)
        
        new_camera_position = list(map(lambda i, j: i + j, camera_position, offset))
        new_focal_point_position = list(map(lambda i, j: i + j, focal_point_position, offset))
        
        camera.SetPosition(*new_camera_position)
        camera.SetFocalPoint(*new_focal_point_position)
        
        self._pipeline.renderer.SetActiveCamera(camera)
        self._pipeline.render_window.Render()
        self.ctrl.push_camera()

    def rotate(self, direction, **kwargs):
        camera = self._pipeline.renderer.GetActiveCamera()
        x, y, z = camera.GetFocalPoint()
        
        rotation = vtkTransform()
        rotation.Translate(x, y, z)
        
        if direction == Directions.XAxisPlus:
            rotation.RotateX(-30.0)
        elif direction == Directions.XAxisMinus:
            rotation.RotateX(30.0)
        elif direction == Directions.YAxisPlus:
            rotation.RotateY(-30.0)
        elif direction == Directions.YAxisMinus:
            rotation.RotateY(30.0)
        elif direction == Directions.ZAxisPlus:
            rotation.RotateZ(-30.0)
        elif direction == Directions.ZAxisMinus:
            rotation.RotateZ(30.0)
        
        rotation.Translate(-x, -y, -z)
        camera.ApplyTransform(rotation)
        
        self._pipeline.renderer.SetActiveCamera(camera)
        self._pipeline.render_window.Render()
        self.ctrl.push_camera()

    @life_cycle.server_reload
    def _build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self._server, vuetify_config=VUETIFY_CONFIG) as layout:
            layout.root.theme = ("theme", DEFAULT_THEME)
            
            # Icon
            with layout.icon as icon:
                icon.click = None
                with html.A(href="https://www.ikem.cz/", target="_blank"):
                    html.Img(src=("icon",), height=35)
            
            # Title
            with layout.title as title:
                title.set_text(APPLICATION_NAME)
            
            # Toolbar
            with layout.toolbar:
                vuetify3.VSpacer()
                vuetify3.VDivider(vertical=True, classes="mx-2")
                animation_icons(self)
                vuetify3.VDivider(vertical=True, classes="mx-2")
                vuetify3.VSpacer()

                vuetify3.VDivider(vertical=True)
                picker_modes_icons()
                vuetify3.VDivider(vertical=True)
                toolbar_icons(self)
                vuetify3.VDivider(vertical=True)
                language_buttons()
                
                progress_bar()

            # Sidebar
            with layout.drawer:
                # Upload
                upload_vti_files()
                
                # Selects
                vti_file_select()
                data_array_select()
                representation_select()
                
                # Slice
                slice_interaction()
                
                # Interaction
                zoom_interaction(self)
                translation_interaction(self)
                rotation_interaction(self)

            # Content
            with layout.content:
                with trame.SizeObserver("content_size"):
                    # Local view
                    with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
                        view = vtk.VtkLocalView(
                            self._pipeline.render_window,
                            interactor_events=("events", ["LeftButtonPress", "EndAnimation"]),
                            LeftButtonPress=(self.on_picker, "[utils.vtk.event($event)]"),
                            EndAnimation=(self.on_interaction, "[$event.pokedRenderer.getActiveCamera().get()]")
                        )
                        self.ctrl.update = view.update
                        self.ctrl.push_camera = view.push_camera

                    # Tooltip
                    with vuetify3.VCard(title=("tooltip_title",), style=("tooltip_style", HIDDEN_STYLE)):
                        vuetify3.VCardText("<pre>{{ tooltip_message }}</pre>")

            # Footer
            layout.footer.hide()

            return layout
