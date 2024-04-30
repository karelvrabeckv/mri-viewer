from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkCommonTransforms import vtkTransform

from .vtk_creator import VTKCreator

from mri_viewer.app.files import File, FileGroup

import mri_viewer.app.constants as const

class VTKManager():
    """Class representing manager of VTK."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            # Create only one instance of this class
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__creator = VTKCreator()
        self.__objects = {}
        
        self.__picker = self.__creator.create_picker()
        self.__renderer = self.__creator.create_renderer(self.get_default_theme_background())
        self.__render_window = self.__creator.create_render_window(self.__renderer)
        self.__render_window_interactor = self.__creator.create_render_window_interactor(self.__render_window)
        self.__axes_widget = self.__creator.create_axes_widget(self.__render_window_interactor)
        self.__picked_point = None
        self.__picked_point_mapper = None
        self.__picked_point_actor = None
        self.__picked_cell = None
        self.__picked_cell_mapper = None
        self.__picked_cell_actor = None

        self.__axes_info_on = True
        self.__initial_view = self.get_camera_params()
        self.__latest_group = ""
        
        self.reset_camera()
        self.render()

    @property
    def render_window(self):
        return self.__render_window

    @property
    def axes_widget(self):
        return self.__axes_widget

    @property
    def axes_info_on(self):
        return self.__axes_info_on

    @axes_info_on.setter
    def axes_info_on(self, axes_info_on): 
        self.__axes_info_on = axes_info_on

    def get_object(self, object_type):
        """Return particular VTK object."""

        if not self.__latest_group:
            return
        
        return self.__objects[self.__latest_group][object_type]

    def render_file(self, file: File, group: FileGroup, theme: const.Theme):
        """Render particular VTI file."""

        self.__latest_group = group.id
        color = self.get_theme_color(theme)

        if self.__latest_group in self.__objects.keys():
            file_mapper = self.get_object(const.Objects.FileMapper)
            file_mapper.SetInputConnection(file.reader.GetOutputPort())
            file_mapper.SetScalarRange(file.data.GetArray(group.data_array).GetRange())

            slice = self.get_object(const.Objects.Slice)
            slice.SetInputData(file.reader.GetOutput())

            slice_mapper = self.get_object(const.Objects.SliceMapper)
            slice_mapper.SetScalarRange(file.data.GetArray(group.data_array).GetRange())

            file_actor = self.get_object(const.Objects.FileActor)

            cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
            self.__creator.set_cube_axes_actor_colors(cube_axes_actor, color)
            
            scalar_bar_actor = self.get_object(const.Objects.ScalarBarActor)
            self.__creator.set_scalar_bar_actor_colors(scalar_bar_actor, color)
            
            self.set_visibility(True, file_actor, scalar_bar_actor)
        else:
            color_transfer_function = self.__creator.create_color_transfer_function(group)
            lookup_table = self.__creator.create_lookup_table(color_transfer_function)            
            
            file_mapper = self.__creator.create_file_mapper(file, group.data_array, lookup_table)
            file_actor = self.__creator.create_file_actor(file_mapper)
            
            cube_axes_actor = self.__creator.create_cube_axes_actor(file_actor, color, self.__renderer)
            scalar_bar_actor = self.__creator.create_scalar_bar_actor(group, lookup_table, color)
            
            slice = self.__creator.create_slice(file)
            slice_mapper = self.__creator.create_slice_mapper(file, slice, group.data_array, lookup_table)
            slice_actor = self.__creator.create_slice_actor(slice_mapper)
            
            self.__objects[self.__latest_group] = {
                const.Objects.ColorTransferFunction: color_transfer_function,
                const.Objects.LookupTable: lookup_table,
                const.Objects.FileMapper: file_mapper,
                const.Objects.FileActor: file_actor,
                const.Objects.CubeAxesActor: cube_axes_actor,
                const.Objects.ScalarBarActor: scalar_bar_actor,
                const.Objects.Slice: slice,
                const.Objects.SliceMapper: slice_mapper,
                const.Objects.SliceActor: slice_actor,
            }
            
            self.set_slice(group)
            self.add_actors(file_actor, cube_axes_actor, slice_actor)
            self.add_2d_actors(scalar_bar_actor)
        
        self.set_visibility(self.__axes_info_on, cube_axes_actor)

        self.reset_camera()
        self.render()

    def render_data_array(self, file: File, new_active_array):
        """Render particular data array of VTI file."""

        file.data.SetActiveScalars(new_active_array)
        
        file_mapper = self.get_object(const.Objects.FileMapper)
        file_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())

        scalar_bar_actor = self.get_object(const.Objects.ScalarBarActor)
        scalar_bar_actor.SetTitle(new_active_array)
        
        slice_mapper = self.get_object(const.Objects.SliceMapper)
        slice_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())
        
        self.render()

    def render_representation(self, new_active_representation):
        """Render particular representation of VTI file."""

        file_actor = self.get_object(const.Objects.FileActor)
        self.set_visibility(True, file_actor)
        
        slice_actor = self.get_object(const.Objects.SliceActor)
        self.set_visibility(False, slice_actor)
        
        actor_property = file_actor.GetProperty()
        
        if new_active_representation == const.Representations.Points:
            actor_property.SetRepresentationToPoints()
            actor_property.SetPointSize(3)
            actor_property.EdgeVisibilityOff()
        elif new_active_representation == const.Representations.Slice:
            self.set_visibility(False, file_actor)
            self.set_visibility(True, slice_actor)
        elif new_active_representation == const.Representations.Surface:
            actor_property.SetRepresentationToSurface()
            actor_property.SetPointSize(1)
            actor_property.EdgeVisibilityOff()
        elif new_active_representation == const.Representations.SurfaceWithEdges:
            actor_property.SetRepresentationToSurface()
            actor_property.SetPointSize(1)
            actor_property.EdgeVisibilityOn()
        elif new_active_representation == const.Representations.Wireframe:
            actor_property.SetRepresentationToWireframe()
            actor_property.SetPointSize(1)
            actor_property.EdgeVisibilityOff()

        self.render()

    def render_color_map(self, new_active_color_map):
        """Render particular color map of VTI file."""

        color_transfer_function = self.get_object(const.Objects.ColorTransferFunction)
        color_transfer_function.RemoveAllPoints()

        if new_active_color_map == const.ColorMaps.CoolToWarm:
            self.__creator.set_color_map_cool_to_warm(color_transfer_function)
        elif new_active_color_map == const.ColorMaps.Grayscale:
            self.__creator.set_color_map_grayscale(color_transfer_function)

        lookup_table = self.get_object(const.Objects.LookupTable)
        self.__creator.set_lookup_table_values(color_transfer_function, lookup_table)

        self.render()

    def set_slice(self, group: FileGroup):
        """Set slice of VTI file."""

        min_x, max_x, min_y, max_y, min_z, max_z = group.extent
        origin_x, origin_y, origin_z = group.origin
        space_x, space_y, space_z = group.spacing
        
        slice = self.get_object(const.Objects.Slice)
        position = group.slice_position[group.slice_orientation]
        
        if group.slice_orientation == const.Planes.XY:
            position = int((position - origin_z) / space_z)
            slice.SetVOI(min_x, max_x, min_y, max_y, position, position)
        elif group.slice_orientation == const.Planes.YZ:
            position = int((position - origin_x) / space_x)
            slice.SetVOI(position, position, min_y, max_y, min_z, max_z)
        elif group.slice_orientation == const.Planes.XZ:
            position = int((position - origin_y) / space_y)
            slice.SetVOI(min_x, max_x, position, position, min_z, max_z)

    def set_visibility(self, visibility, *actors):
        """Set visibility of given actors."""

        for actor in actors:
            actor.SetVisibility(visibility)

    def add_actors(self, *actors):
        """Add actors to scene."""

        for actor in actors:
            self.__renderer.AddActor(actor)

    def add_2d_actors(self, *actors):
        """Add 2D actors to scene."""

        for actor in actors:
            self.__renderer.AddActor2D(actor)

    def reset_camera(self):
        """Reset camera to see every actor."""

        self.__renderer.ResetCamera()

    def render(self):
        """Command renderers to render their scenes."""

        self.__render_window.Render()

    def render_axes_info(self):
        """Set visibility of axes grid."""

        cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
        self.set_visibility(self.__axes_info_on, cube_axes_actor)

    def resize_window(self, content_size):
        """Set size of scene based on size of browser."""

        size = content_size["size"]
        pixel_ratio = content_size["pixelRatio"]
        
        width = int(size["width"] * pixel_ratio)
        height = int(size["height"] * pixel_ratio)

        self.__render_window.SetSize(width, height)

        self.render()

    def get_theme_color(self, theme):
        """Return current theme color."""

        if theme == const.Theme.Light:
            return const.Theme.BlackColor
        return const.Theme.WhiteColor
    
    def get_theme_background(self, theme):
        """Return current theme background."""

        if theme == const.Theme.Light:
            return const.Theme.LightBackground
        return const.Theme.DarkBackground

    def get_default_theme_background(self):
        """Return default theme background."""

        if const.DEFAULT_THEME == const.Theme.Light:
            return const.Theme.LightBackground
        return const.Theme.DarkBackground

    def hide_current_file(self):
        """Hide current VTI file."""

        file_actor = self.get_object(const.Objects.FileActor)
        cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
        scalar_bar_actor = self.get_object(const.Objects.ScalarBarActor)
        slice_actor = self.get_object(const.Objects.SliceActor)
        
        self.set_visibility(False, file_actor, cube_axes_actor, scalar_bar_actor, slice_actor)

        self.hide_picked_point()
        self.hide_picked_cell()
        
        self.reset_camera()
        self.render()
    
    def change_colors(self, theme):
        """Change colors of axes grid and side scalar scale based on theme."""

        background = self.get_theme_background(theme)
        self.__renderer.SetBackground(background)

        color = self.get_theme_color(theme)

        cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
        if cube_axes_actor:
            self.__creator.set_cube_axes_actor_colors(cube_axes_actor, color)

        scalar_bar_actor = self.get_object(const.Objects.ScalarBarActor)
        if scalar_bar_actor:
            self.__creator.set_scalar_bar_actor_colors(scalar_bar_actor, color)

        self.render()

    def zoom(self, direction, power):
        """Execute camera zoom."""

        camera = self.__renderer.GetActiveCamera()

        if direction == const.Zoom.In:
            for _ in range(power):
                camera.Zoom(1 + const.Zoom.Factor)
        elif direction == const.Zoom.Out:
            for _ in range(power):
                camera.Zoom(1 - const.Zoom.Factor)
        
        self.render()

    def translate(self, direction, step):
        """Execute camera translation."""

        offset_x, offset_y, offset_z = 0.0, 0.0, 0.0

        if direction == const.Directions.XAxisPlus:
            offset_x -= step
        elif direction == const.Directions.XAxisMinus:
            offset_x += step
        elif direction == const.Directions.YAxisPlus:
            offset_y -= step
        elif direction == const.Directions.YAxisMinus:
            offset_y += step
        elif direction == const.Directions.ZAxisPlus:
            offset_z -= step
        elif direction == const.Directions.ZAxisMinus:
            offset_z += step
        
        offset = (offset_x, offset_y, offset_z)
        camera = self.__renderer.GetActiveCamera()
        
        new_camera_position = list(map(lambda i, j: i + j, camera.GetPosition(), offset))
        camera.SetPosition(*new_camera_position)

        new_focal_point_position = list(map(lambda i, j: i + j, camera.GetFocalPoint(), offset))
        camera.SetFocalPoint(*new_focal_point_position)
        
        self.render()

    def rotate(self, direction, angle):
        """Execute camera rotation."""

        file_actor = self.get_object(const.Objects.FileActor)
        x, y, z = file_actor.GetCenter()

        rotation = vtkTransform()
        rotation.Translate(x, y, z)
        
        if direction == const.Directions.XAxisPlus:
            rotation.RotateX(angle)
        elif direction == const.Directions.XAxisMinus:
            rotation.RotateX(-angle)
        elif direction == const.Directions.YAxisPlus:
            rotation.RotateY(angle)
        elif direction == const.Directions.YAxisMinus:
            rotation.RotateY(-angle)
        elif direction == const.Directions.ZAxisPlus:
            rotation.RotateZ(angle)
        elif direction == const.Directions.ZAxisMinus:
            rotation.RotateZ(-angle)
        
        rotation.Translate(-x, -y, -z)

        camera = self.__renderer.GetActiveCamera()
        camera.ApplyTransform(rotation)

        self.render()

    def get_picked_point_info(self, data: vtkImageData, x, y):
        """Return information about picked point."""

        self.__picker.Pick(x, y, 0.0, self.__renderer)

        message = {}
        point_id = self.__picker.GetPointId()
        
        if point_id != -1:
            point = data.GetPoint(point_id)
            message = { const.ID: point_id, const.Axes.X: point[0], const.Axes.Y: point[1], const.Axes.Z: point[2] }

            point_data = data.GetPointData()
            num_of_data_arrays = point_data.GetNumberOfArrays()
        
            for i in range(num_of_data_arrays):
                data_array = point_data.GetArray(i)
                value = data_array.GetValue(point_id)
                message[data_array.GetName()] = round(value, const.PickedParams.Precision)

        return message

    def show_picked_point(self, position):
        """Show picked point at given position."""

        if not self.__picked_point:
            self.__picked_point = self.__creator.create_picked_point(position)
            self.__picked_point_mapper = self.__creator.create_picked_primitive_mapper(self.__picked_point)
            self.__picked_point_actor = self.__creator.create_picked_point_actor(self.__picked_point_mapper)
            
            self.add_actors(self.__picked_point_actor)
        else:
            self.__creator.set_picked_point_properties(self.__picked_point, position)
            self.set_visibility(True, self.__picked_point_actor)

        self.render()

    def hide_picked_point(self):
        """Hide picked point."""

        if self.__picked_point_actor:
            self.set_visibility(False, self.__picked_point_actor)

        self.render()

    def get_picked_cell_info(self, data: vtkImageData, x, y):
        """Return information about picked cell."""

        self.__picker.Pick(x, y, 0.0, self.__renderer)
        
        message = {}
        cell_id = self.__picker.GetCellId()
        
        if cell_id != -1:
            cell_data = data.GetCellData()
            num_of_data_arrays = cell_data.GetNumberOfArrays()
            
            message[const.ID] = cell_id
            for i in range(num_of_data_arrays):
                data_array = cell_data.GetArray(i)
                value = data_array.GetValue(cell_id)
                message[data_array.GetName()] = round(value, const.PickedParams.Precision)
        
        return message

    def show_picked_cell(self, bounds):
        """Show picked cell with given bounds."""

        if not self.__picked_cell:
            self.__picked_cell = self.__creator.create_picked_cell(bounds)
            self.__picked_cell_mapper = self.__creator.create_picked_primitive_mapper(self.__picked_cell)
            self.__picked_cell_actor = self.__creator.create_picked_cell_actor(self.__picked_cell_mapper)

            self.add_actors(self.__picked_cell_actor)
        else:
            self.__creator.set_picked_cell_properties(self.__picked_cell, bounds)
            self.set_visibility(True, self.__picked_cell_actor)

        self.render()

    def hide_picked_cell(self):
        """Hide picked cell."""

        if self.__picked_cell_actor:
            self.set_visibility(False, self.__picked_cell_actor)

        self.render()

    def get_camera_params(self):
        """Return camera parameters."""

        camera = self.__renderer.GetActiveCamera()
        
        return {
            const.CameraParams.Position: camera.GetPosition(),
            const.CameraParams.FocalPoint: camera.GetFocalPoint(),
            const.CameraParams.ViewUp: camera.GetViewUp(),
            const.CameraParams.ViewAngle: camera.GetViewAngle(),
        }

    def set_camera_params(self, position, focal_point, view_up, view_angle):
        """Set camera parameters."""

        camera = self.__renderer.GetActiveCamera()
        
        camera.SetPosition(position)
        camera.SetFocalPoint(focal_point)
        camera.SetViewUp(view_up)
        camera.SetViewAngle(view_angle)
        
        self.__renderer.ResetCameraClippingRange()
        
        self.render()

    def set_camera_to_group_default_view(self, group: FileGroup):
        """Set camera to default view of group."""

        self.set_camera_params(
            group.default_view[const.CameraParams.Position],
            group.default_view[const.CameraParams.FocalPoint],
            group.default_view[const.CameraParams.ViewUp],
            group.default_view[const.CameraParams.ViewAngle],
        )

    def set_camera_to_group_current_view(self, group: FileGroup):
        """Set camera to current view of group."""

        self.set_camera_params(
            group.current_view[const.CameraParams.Position],
            group.current_view[const.CameraParams.FocalPoint],
            group.current_view[const.CameraParams.ViewUp],
            group.current_view[const.CameraParams.ViewAngle],
        )

    def set_camera_to_initial_view(self):
        """Set camera to initial view."""

        self.set_camera_params(
            self.__initial_view[const.CameraParams.Position],
            self.__initial_view[const.CameraParams.FocalPoint],
            self.__initial_view[const.CameraParams.ViewUp],
            self.__initial_view[const.CameraParams.ViewAngle],
        )

    def set_camera_to_client_view(self, client_camera):
        """Synchronize server camera with client camera."""

        self.set_camera_params(
            client_camera.get("position"),
            client_camera.get("focalPoint"),
            client_camera.get("viewUp"),
            client_camera.get("viewAngle"),
        )
