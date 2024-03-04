from vtkmodules.vtkCommonDataModel import vtkImageData

from .pipeline_factory import PipelineFactory

from mri_viewer.app.files import *

import mri_viewer.app.constants as const

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch # noqa

import vtkmodules.vtkRenderingOpenGL2 # noqa

class Pipeline():
    def __init__(self):
        self.__factory = PipelineFactory()
        
        self.__renderer = self.__factory.create_renderer()
        self.__render_window = self.__factory.create_render_window(self.__renderer)
        self.__render_window_interactor = self.__factory.create_render_window_interactor(self.__render_window)
        
        self.__picker = self.__factory.create_picker()
        self.__axes_widget = self.__factory.create_axes_widget(self.__render_window_interactor)
        
        self.__objects = {}
        self.__latest_file_name = ""
        self.__initial_view = self.get_camera_params()
        self.__axes_on = True
        
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
    def axes_on(self):
        return self.__axes_on

    @axes_on.setter
    def axes_on(self, axes_on): 
        self.__axes_on = axes_on

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

    def get_object(self, object: const.Objects):
        if not self.__latest_file_name:
            return        
        return self.__objects[self.__latest_file_name][object]

    def get_file_actor_center(self):
        file_actor = self.get_object(const.Objects.FileActor)
        if not file_actor:
            return
        return file_actor.GetCenter()

    def hide_current_file(self):
        latest_file_actor = self.get_object(const.Objects.FileActor)
        latest_cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
        latest_slice_actor = self.get_object(const.Objects.SliceActor)
        
        self.set_visibility(False, latest_file_actor, latest_cube_axes_actor, latest_slice_actor)
        
        self.reset_camera()
        self.render()

    def render_file(self, file: File, group: FileGroup):
        self.__latest_file_name = file.name
        file.data.SetActiveScalars(group.data_array)
        
        if self.__latest_file_name in self.__objects.keys():
            file_actor = self.get_object(const.Objects.FileActor)
            cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
            
            self.set_visibility(True, file_actor)
        else:
            color_transfer_function = self.__factory.create_color_transfer_function()
            lookup_table = self.__factory.create_lookup_table(color_transfer_function)
            
            file_mapper = self.__factory.create_file_mapper(file, group.data_array, lookup_table)
            file_actor = self.__factory.create_file_actor(file_mapper)
            cube_axes_actor = self.__factory.create_cube_axes_actor(file_actor, self.__renderer)
            
            slice = self.__factory.create_slice(file)
            slice_mapper = self.__factory.create_slice_mapper(file, slice, group.data_array, lookup_table)
            slice_actor = self.__factory.create_slice_actor(slice_mapper)
            
            self.__objects[self.__latest_file_name] = {
                const.Objects.ColorTransferFunction: color_transfer_function,
                const.Objects.LookupTable: lookup_table,
                const.Objects.FileMapper: file_mapper,
                const.Objects.FileActor: file_actor,
                const.Objects.CubeAxesActor: cube_axes_actor,
                const.Objects.Slice: slice,
                const.Objects.SliceMapper: slice_mapper,
                const.Objects.SliceActor: slice_actor,
            }
            
            self.set_slice(file, group.slice_orientation, group.slice_position)
            self.add_actors(file_actor, cube_axes_actor, slice_actor)
        
        self.set_visibility(self.__axes_on, cube_axes_actor)

        self.reset_camera()
        self.render()

    def render_data_array(self, file: File, new_active_array):
        file.data.SetActiveScalars(new_active_array)
        
        file_mapper = self.get_object(const.Objects.FileMapper)
        file_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())
        
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

    def set_slice(self, file, slice_orientation, slice_position):
        min_x, max_x, min_y, max_y, min_z, max_z = file.extent
        slice = self.get_object(const.Objects.Slice)
        position = slice_position[slice_orientation]
        
        if slice_orientation == const.Planes.XY:
            slice.SetVOI(min_x, max_x, min_y, max_y, position, position)
        elif slice_orientation == const.Planes.YZ:
            slice.SetVOI(position, position, min_y, max_y, min_z, max_z)
        elif slice_orientation == const.Planes.XZ:
            slice.SetVOI(min_x, max_x, position, position, min_z, max_z)

    def set_visibility(self, visibility, *actors):
        for actor in actors:
            actor.SetVisibility(visibility)
    
    def add_actors(self, *actors):
        for actor in actors:
            self.__renderer.AddActor(actor)

    def reset_camera(self):
        self.__renderer.ResetCamera()

    def render(self):
        self.__render_window.Render()

    def render_axes(self):
        cube_axes_actor = self.get_object(const.Objects.CubeAxesActor)
        self.set_visibility(self.__axes_on, cube_axes_actor)

    def resize_window(self, width, height):
        self.__render_window.SetSize(width, height)
        self.render()

    def get_point_information(self, data: vtkImageData, x: float, y: float):
        self.__picker.Pick(x, y, 0.0, self.__renderer)

        message = {}
        point_id = self.__picker.GetPointId()
        
        if point_id != -1:
            point = data.GetPoint(point_id)
            message = { "Id": point_id, "X": point[0], "Y": point[1], "Z": point[2] }
        
        return message
    
    def get_cell_information(self, data: vtkImageData, x: float, y: float):
        self.__picker.Pick(x, y, 0.0, self.__renderer)
        
        message = {}
        cell_id = self.__picker.GetCellId()
        
        if cell_id != -1:
            cell_data = data.GetCellData()
            num_of_data_arrays = cell_data.GetNumberOfArrays()
            
            message["Id"] = cell_id
            for i in range(num_of_data_arrays):
                data_array = cell_data.GetArray(i)
                message[data_array.GetName()] = data_array.GetValue(cell_id)
        
        return message

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
