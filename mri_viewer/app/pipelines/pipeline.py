from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
    vtkPolyDataMapper,
)

from .pipeline_builder import PipelineBuilder

from mri_viewer.app.files import *

import mri_viewer.app.constants as const

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch # noqa

import vtkmodules.vtkRenderingOpenGL2 # noqa

class Pipeline(PipelineBuilder):
    def __init__(self):
        self.__renderer = self.create_renderer()
        self.__render_window = self.create_render_window(self.__renderer)
        self.__render_window_interactor = self.create_render_window_interactor(self.__render_window)
        self.__axes_widget = self.create_axes_widget(self.__render_window_interactor)
        self.__color_transfer_function = self.create_color_transfer_function()
        self.__lookup_table = self.create_lookup_table(self.__color_transfer_function)
        
        self.__data_set_mapper = vtkDataSetMapper()
        self.__actor = vtkActor()
        self.__cube_axes_actor = vtkCubeAxesActor()
        
        self.__slice = vtkExtractVOI()
        self.__slice_poly_data_mapper = vtkPolyDataMapper()
        self.__slice_actor = vtkActor()
        
        self.__picker = vtkCellPicker()
        
        self.__render_window.Render()

        self.__initial_view = self.get_camera_params()

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
    def actor(self):
        return self.__actor

    @property
    def slice(self):
        return self.__slice

    @property
    def slice_actor(self):
        return self.__slice_actor

    @property
    def initial_view(self):
        return self.__initial_view

    def build_data_set_mapper(self, file: File, group_active_array: str):
        self.__data_set_mapper.SetInputConnection(file.reader.GetOutputPort())
        self.__data_set_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        self.__data_set_mapper.SetLookupTable(self.__lookup_table)

    def build_actor(self):
        self.__actor.SetMapper(self.__data_set_mapper)
                
        self.__renderer.AddActor(self.__actor)
        self.__renderer.ResetCamera()

    def build_cube_axes_actor(self):
        self.__cube_axes_actor.SetXTitle("X")
        self.__cube_axes_actor.SetYTitle("Y")
        self.__cube_axes_actor.SetZTitle("Z")
        
        self.__cube_axes_actor.GetXAxesLinesProperty().SetColor(*const.AXES_COLOR)
        self.__cube_axes_actor.GetYAxesLinesProperty().SetColor(*const.AXES_COLOR)
        self.__cube_axes_actor.GetZAxesLinesProperty().SetColor(*const.AXES_COLOR)
        
        self.__cube_axes_actor.SetBounds(self.__actor.GetBounds())
        self.__cube_axes_actor.SetCamera(self.__renderer.GetActiveCamera())
        
        self.__renderer.AddActor(self.__cube_axes_actor)
        self.__renderer.ResetCamera()

    def build_slice(self, file: File, slice_orientation: const.Planes, slice_position: int):
        image_data = file.reader.GetOutput()
        self.__slice.SetInputData(image_data)
        
        max_x, max_y, max_z = image_data.GetDimensions()
        self.render_slice(slice_orientation, slice_position, max_x, max_y, max_z)

    def build_slice_poly_data_mapper(self, file: File, group_active_array: str):
        self.__slice_poly_data_mapper.SetInputConnection(self.__slice.GetOutputPort())
        self.__slice_poly_data_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        self.__slice_poly_data_mapper.SetLookupTable(self.__lookup_table)

    def build_slice_actor(self):
        self.__slice_actor.SetMapper(self.__slice_poly_data_mapper)
        self.__slice_actor.GetProperty().LightingOff()

        self.__renderer.AddActor(self.__slice_actor)
        self.__renderer.ResetCamera()

    def render_file(self, file: File, group_active_array: str, slice_orientation: const.Planes, slice_position: int):
        file.data.SetActiveScalars(group_active_array)

        self.build_data_set_mapper(file, group_active_array)
        self.build_actor()
        self.build_cube_axes_actor()
        
        self.build_slice(file, slice_orientation, slice_position)
        self.build_slice_poly_data_mapper(file, group_active_array)
        self.build_slice_actor()
        
        self.__render_window.Render()

    def render_data_array(self, file: File, new_active_array: str):
        file.data.SetActiveScalars(new_active_array)
        
        self.__data_set_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())
        self.__slice_poly_data_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())

    def render_representation(self, new_active_representation):
        actor_property = self.__actor.GetProperty()
        
        self.__actor.VisibilityOn()
        self.__slice_actor.VisibilityOff()

        if new_active_representation == const.Representation.Points:
            actor_property.SetRepresentationToPoints()
            actor_property.SetPointSize(2)
            actor_property.EdgeVisibilityOff()
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

    def render_slice(self, slice_orientation, slice_position, max_x, max_y, max_z):
        if slice_orientation == const.Planes.XY:
            self.__slice.SetVOI(0, max_x - 1, 0, max_y - 1, slice_position, slice_position)
        elif slice_orientation == const.Planes.YZ:
            self.__slice.SetVOI(slice_position, slice_position, 0, max_y - 1, 0, max_z - 1)
        elif slice_orientation == const.Planes.XZ:
            self.__slice.SetVOI(0, max_x - 1, slice_position, slice_position, 0, max_z - 1)
        
    def render_axes(self, axes_on: bool):
        self.__cube_axes_actor.SetVisibility(axes_on)

    def get_point_information(self, data: vtkImageData, x: float, y: float):
        self.__picker.Pick(x, y, 0.0, self.__renderer)

        message = ""
        point_id = self.__picker.GetPointId()
        
        if point_id != -1:
            point = data.GetPoint(point_id)
            message = f"Id: {point_id}\nX: {point[0]}\nY: {point[1]}\nZ: {point[2]}\n"
        
        return message
    
    def get_cell_information(self, data: vtkImageData, x: float, y: float):
        self.__picker.Pick(x, y, 0.0, self.__renderer)
        
        message = ""
        cell_id = self.__picker.GetCellId()
        
        if cell_id != -1:
            cell_data = data.GetCellData()
            num_of_data_arrays = cell_data.GetNumberOfArrays()
            
            message = f"Id: {cell_id}\n"
            for i in range(num_of_data_arrays):
                data_array = cell_data.GetArray(i)
                message += f"{data_array.GetName()}: {data_array.GetValue(cell_id)}\n"
        
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
