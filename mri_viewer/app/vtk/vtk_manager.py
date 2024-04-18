from vtkmodules.vtkCommonDataModel import vtkImageData

from .vtk_factory import VTKFactory

from mri_viewer.app.files import File, FileGroup

import mri_viewer.app.constants as const

class VTKManager():
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__factory = VTKFactory()
        
        self.__renderer = self.__factory.create_renderer()
        self.__render_window = self.__factory.create_render_window(self.__renderer)
        self.__render_window_interactor = self.__factory.create_render_window_interactor(self.__render_window)
        
        self.__picker = self.__factory.create_picker()
        self.__axes_widget = self.__factory.create_axes_widget(self.__render_window_interactor)
        
        self.__objects = {}
        self.__latest_group = ""
        self.__initial_view = self.get_camera_params()
        self.__axes_info_on = True
        
        self.reset_camera()
        self.render()

    @property
    def renderer(self):
        return self.__renderer

    @property
    def render_window(self):
        return self.__render_window

    @property
    def axes_widget(self):
        return self.__axes_widget

    @property
    def initial_view(self):
        return self.__initial_view

    @property
    def axes_info_on(self):
        return self.__axes_info_on

    @axes_info_on.setter
    def axes_info_on(self, axes_info_on): 
        self.__axes_info_on = axes_info_on

    @property
    def camera(self):
        return self.__renderer.GetActiveCamera()
    
    @camera.setter 
    def camera(self, camera):
        self.__renderer.SetActiveCamera(camera)

    @property
    def file_actor(self):
        return self.get_object(const.Objects.FileActor)
    
    @property
    def slice(self):
        return self.get_object(const.Objects.Slice)

    @property
    def slice_actor(self):
        return self.get_object(const.Objects.SliceActor)

    def get_object(self, object_type: const.Objects):
        if not self.__latest_group:
            return        
        return self.__objects[self.__latest_group][object_type]

    def set_object(self, object_type: const.Objects, object):
        if not self.__latest_group:
            return        
        self.__objects[self.__latest_group][object_type] = object

    def get_file_actor_center(self):
        file_actor = self.get_object(const.Objects.FileActor)
        if not file_actor:
            return
        return file_actor.GetCenter()

    def hide_current_file(self):
        latest_file_actor = self.get_object(const.Objects.FileActor)
        latest_cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
        latest_scalar_bar_actor = self.get_object(const.Objects.ScalarBarActor)
        latest_slice_actor = self.get_object(const.Objects.SliceActor)
        
        self.set_visibility(
            False,
            latest_file_actor, latest_cube_axes_actor,
            latest_scalar_bar_actor, latest_slice_actor
        )

        self.hide_picked_point()
        self.hide_picked_cell()
        
        self.reset_camera()
        self.render()

    def render_file(self, file: File, group: FileGroup):
        self.__latest_group = group.id
        file.data.SetActiveScalars(group.data_array)
        
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
            scalar_bar_actor = self.get_object(const.Objects.ScalarBarActor)
            
            self.set_visibility(True, file_actor, scalar_bar_actor)
        else:
            color_transfer_function = self.__factory.create_color_transfer_function(group)
            lookup_table = self.__factory.create_lookup_table(color_transfer_function)
            
            file_mapper = self.__factory.create_file_mapper(file, group.data_array, lookup_table)
            file_actor = self.__factory.create_file_actor(file_mapper)
            cube_axes_actor = self.__factory.create_cube_axes_actor(file_actor, self.__renderer)
            scalar_bar_actor = self.__factory.create_scalar_bar_actor(file, lookup_table)
            
            slice = self.__factory.create_slice(file)
            slice_mapper = self.__factory.create_slice_mapper(file, slice, group.data_array, lookup_table)
            slice_actor = self.__factory.create_slice_actor(slice_mapper)
            
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
                const.Objects.PickedPoint: None,
                const.Objects.PickedPointMapper: None,
                const.Objects.PickedPointActor: None,
                const.Objects.PickedCell: None,
                const.Objects.PickedCellMapper: None,
                const.Objects.PickedCellActor: None,
            }
            
            self.set_slice(file, group.slice_orientation, group.slice_position)
            self.add_actors(file_actor, cube_axes_actor, slice_actor)
            self.add_actors_2d(scalar_bar_actor)
        
        self.set_visibility(self.__axes_info_on, cube_axes_actor)

        self.reset_camera()
        self.render()

    def render_data_array(self, file: File, new_active_array):
        file.data.SetActiveScalars(new_active_array)
        
        file_mapper = self.get_object(const.Objects.FileMapper)
        file_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())

        scalar_bar_actor = self.get_object(const.Objects.ScalarBarActor)
        scalar_bar_actor.SetTitle(new_active_array)
        
        slice_mapper = self.get_object(const.Objects.SliceMapper)
        slice_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())
        
        self.reset_camera()
        self.render()

    def render_representation(self, new_active_representation):
        file_actor = self.get_object(const.Objects.FileActor)
        self.set_visibility(True, file_actor)
        
        slice_actor = self.get_object(const.Objects.SliceActor)
        self.set_visibility(False, slice_actor)
        
        actor_property = file_actor.GetProperty()
        
        if new_active_representation == const.Representation.Points:
            actor_property.SetRepresentationToPoints()
            actor_property.SetPointSize(2)
            actor_property.EdgeVisibilityOff()
        elif new_active_representation == const.Representation.Slice:
            self.set_visibility(False, file_actor)
            self.set_visibility(True, slice_actor)
        elif new_active_representation == const.Representation.Surface:
            actor_property.SetRepresentationToSurface()
            actor_property.SetPointSize(1)
            actor_property.EdgeVisibilityOff()
        elif new_active_representation == const.Representation.SurfaceWithEdges:
            actor_property.SetRepresentationToSurface()
            actor_property.SetPointSize(1)
            actor_property.EdgeVisibilityOn()
        elif new_active_representation == const.Representation.Wireframe:
            actor_property.SetRepresentationToWireframe()
            actor_property.SetPointSize(1)
            actor_property.EdgeVisibilityOff()

        self.reset_camera()
        self.render()

    def render_color_map(self, new_active_color_map):
        color_transfer_function = self.get_object(const.Objects.ColorTransferFunction)
        color_transfer_function.RemoveAllPoints()

        if new_active_color_map == const.ColorMaps.CoolToWarm:
            self.__factory.set_color_map_cool_to_warm(color_transfer_function)
        elif new_active_color_map == const.ColorMaps.Grayscale:
            self.__factory.set_color_map_grayscale(color_transfer_function)

        lookup_table = self.get_object(const.Objects.LookupTable)
        self.__factory.set_lookup_table_values(color_transfer_function, lookup_table)

        self.reset_camera()
        self.render()

    def set_slice(self, file, slice_orientation, slice_position):
        min_x, max_x, min_y, max_y, min_z, max_z = file.extent
        origin_x, origin_y, origin_z = file.origin
        space_x, space_y, space_z = file.spacing
        
        slice = self.get_object(const.Objects.Slice)
        position = slice_position[slice_orientation]
        
        if slice_orientation == const.Planes.XY:
            position = int((position - origin_z) / space_z)
            slice.SetVOI(min_x, max_x, min_y, max_y, position, position)
        elif slice_orientation == const.Planes.YZ:
            position = int((position - origin_x) / space_x)
            slice.SetVOI(position, position, min_y, max_y, min_z, max_z)
        elif slice_orientation == const.Planes.XZ:
            position = int((position - origin_y) / space_y)
            slice.SetVOI(min_x, max_x, position, position, min_z, max_z)

    def set_visibility(self, visibility, *actors):
        for actor in actors:
            actor.SetVisibility(visibility)
    
    def add_actors(self, *actors):
        for actor in actors:
            self.__renderer.AddActor(actor)

    def add_actors_2d(self, *actors):
        for actor in actors:
            self.__renderer.AddActor2D(actor)

    def reset_camera(self):
        self.__renderer.ResetCamera()

    def render(self):
        self.__render_window.Render()

    def render_axes_info(self):
        cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
        self.set_visibility(self.__axes_info_on, cube_axes_actor)

    def resize_window(self, width, height):
        self.__render_window.SetSize(width, height)
        self.render()

    def get_picked_point_info(self, data: vtkImageData, x: float, y: float):
        self.__picker.Pick(x, y, 0.0, self.__renderer)

        message = {}
        point_id = self.__picker.GetPointId()
        
        if point_id != -1:
            point = data.GetPoint(point_id)
            message = { const.ID: point_id, const.Axis.X: point[0], const.Axis.Y: point[1], const.Axis.Z: point[2] }

            point_data = data.GetPointData()
            num_of_data_arrays = point_data.GetNumberOfArrays()
        
            for i in range(num_of_data_arrays):
                data_array = point_data.GetArray(i)
                value = data_array.GetValue(point_id)
                message[data_array.GetName()] = round(value, 5)

        return message
    
    def show_picked_point(self, position):
        if not self.get_object(const.Objects.PickedPoint):
            picked_point = self.__factory.create_picked_point(position)
            self.set_object(const.Objects.PickedPoint, picked_point)

            picked_point_mapper = self.__factory.create_picked_point_mapper(picked_point)
            self.set_object(const.Objects.PickedPointMapper, picked_point_mapper)

            picked_point_actor = self.__factory.create_picked_point_actor(picked_point_mapper)
            self.set_object(const.Objects.PickedPointActor, picked_point_actor)

            self.add_actors(picked_point_actor)
        else:
            picked_point = self.get_object(const.Objects.PickedPoint)
            self.__factory.set_picked_point_properties(picked_point, position)

            picked_point_actor = self.get_object(const.Objects.PickedPointActor)
            self.set_visibility(True, picked_point_actor)

        self.reset_camera()
        self.render()

    def hide_picked_point(self):
        picked_point_actor = self.get_object(const.Objects.PickedPointActor)
        if picked_point_actor:
            self.set_visibility(False, picked_point_actor)

    def get_picked_cell_info(self, data: vtkImageData, x: float, y: float):
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
                message[data_array.GetName()] = round(value, 5)
        
        return message

    def show_picked_cell(self, bounds):
        if not self.get_object(const.Objects.PickedCell):
            picked_cell = self.__factory.create_picked_cell(bounds)
            self.set_object(const.Objects.PickedCell, picked_cell)

            picked_cell_mapper = self.__factory.create_picked_cell_mapper(picked_cell)
            self.set_object(const.Objects.PickedCellMapper, picked_cell_mapper)

            picked_cell_actor = self.__factory.create_picked_cell_actor(picked_cell_mapper)
            self.set_object(const.Objects.PickedCellActor, picked_cell_actor)

            self.add_actors(picked_cell_actor)
        else:
            picked_cell = self.get_object(const.Objects.PickedCell)
            self.__factory.set_picked_cell_properties(picked_cell, bounds)

            picked_cell_actor = self.get_object(const.Objects.PickedCellActor)
            self.set_visibility(True, picked_cell_actor)

        self.reset_camera()
        self.render()

    def hide_picked_cell(self):
        picked_cell_actor = self.get_object(const.Objects.PickedCellActor)
        if picked_cell_actor:
            self.set_visibility(False, picked_cell_actor)

    def get_camera_params(self):
        camera = self.__renderer.GetActiveCamera()
        
        return {
            const.CameraParams.Position: camera.GetPosition(),
            const.CameraParams.FocalPoint: camera.GetFocalPoint(),
            const.CameraParams.ViewUp: camera.GetViewUp(),
            const.CameraParams.ViewAngle: camera.GetViewAngle(),
        }

    def set_camera_params(self, position, focal_point, view_up, view_angle):
        camera = self.__renderer.GetActiveCamera()
        
        camera.SetPosition(position)
        camera.SetFocalPoint(focal_point)
        camera.SetViewUp(view_up)
        camera.SetViewAngle(view_angle)
        
        self.__renderer.ResetCameraClippingRange()
        self.__render_window.Render()

    def set_camera_to_group_default_view(self, group: FileGroup):
        self.set_camera_params(
            group.default_view[const.CameraParams.Position],
            group.default_view[const.CameraParams.FocalPoint],
            group.default_view[const.CameraParams.ViewUp],
            group.default_view[const.CameraParams.ViewAngle],
        )

    def set_camera_to_group_current_view(self, group: FileGroup):
        self.set_camera_params(
            group.current_view[const.CameraParams.Position],
            group.current_view[const.CameraParams.FocalPoint],
            group.current_view[const.CameraParams.ViewUp],
            group.current_view[const.CameraParams.ViewAngle],
        )

    def set_camera_to_initial_view(self):
        self.set_camera_params(
            self.initial_view[const.CameraParams.Position],
            self.initial_view[const.CameraParams.FocalPoint],
            self.initial_view[const.CameraParams.ViewUp],
            self.initial_view[const.CameraParams.ViewAngle],
        )

    def set_camera_to_client_view(self, client_camera):
        self.set_camera_params(
            client_camera.get("position"),
            client_camera.get("focalPoint"),
            client_camera.get("viewUp"),
            client_camera.get("viewAngle"),
        )
