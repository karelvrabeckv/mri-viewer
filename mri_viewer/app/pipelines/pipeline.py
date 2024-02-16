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
        self._renderer = self.create_renderer()
        self._render_window = self.create_render_window(self._renderer)
        self._render_window_interactor = self.create_render_window_interactor(self._render_window)
        self._color_transfer_function = self.create_color_transfer_function()
        self._lookup_table = self.create_lookup_table(self._color_transfer_function)
        
        self._data_set_mapper = vtkDataSetMapper()
        self._actor = vtkActor()
        self._cube_axes_actor = vtkCubeAxesActor()
        
        self._slice = vtkExtractVOI()
        self._slice_poly_data_mapper = vtkPolyDataMapper()
        self._slice_actor = vtkActor()
        
        self._picker = vtkCellPicker()
        
        self._render_window.Render()

        self._initial_view = self.get_camera_params()

    @property
    def renderer(self):
        return self._renderer

    @property
    def render_window(self):
        return self._render_window

    @property
    def data_set_mapper(self):
        return self._data_set_mapper

    @property
    def actor(self):
        return self._actor

    @property
    def cube_axes_actor(self):
        return self._cube_axes_actor

    @property
    def slice(self):
        return self._slice

    @property
    def slice_poly_data_mapper(self):
        return self._slice_poly_data_mapper
      
    @property
    def slice_actor(self):
        return self._slice_actor

    @property
    def initial_view(self):
        return self._initial_view

    def build_data_set_mapper(self, file: File, group_active_array: str):
        self._data_set_mapper.SetInputConnection(file.reader.GetOutputPort())
        self._data_set_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        self._data_set_mapper.SetLookupTable(self._lookup_table)

    def build_actor(self):
        self._actor.SetMapper(self._data_set_mapper)
                
        self._renderer.AddActor(self._actor)
        self._renderer.ResetCamera()

    def build_cube_axes_actor(self):        
        self._cube_axes_actor.GetXAxesLinesProperty().SetColor(*const.AXES_COLOR)
        self._cube_axes_actor.GetYAxesLinesProperty().SetColor(*const.AXES_COLOR)
        self._cube_axes_actor.GetZAxesLinesProperty().SetColor(*const.AXES_COLOR)
        
        self._cube_axes_actor.SetBounds(self._actor.GetBounds())
        self._cube_axes_actor.SetCamera(self._renderer.GetActiveCamera())
        
        self._renderer.AddActor(self._cube_axes_actor)
        self._renderer.ResetCamera()

    def build_slice(self, file: File, slice_orientation: const.Planes, slice_position: int):
        image_data = file.reader.GetOutput()
        self._slice.SetInputData(image_data)
        
        max_x, max_y, max_z = image_data.GetDimensions()
        self.render_slice(slice_orientation, slice_position, max_x, max_y, max_z)

    def build_slice_poly_data_mapper(self, file: File, group_active_array: str):
        self._slice_poly_data_mapper.SetInputConnection(self._slice.GetOutputPort())
        self._slice_poly_data_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        self._slice_poly_data_mapper.SetLookupTable(self._lookup_table)

    def build_slice_actor(self):
        self._slice_actor.SetMapper(self._slice_poly_data_mapper)
        self._slice_actor.GetProperty().LightingOff()

        self._renderer.AddActor(self._slice_actor)
        self._renderer.ResetCamera()

    def render_file(self, file: File, group_active_array: str, slice_orientation: const.Planes, slice_position: int):
        file.data.SetActiveScalars(group_active_array)

        self.build_data_set_mapper(file, group_active_array)
        self.build_actor()
        self.build_cube_axes_actor()
        
        self.build_slice(file, slice_orientation, slice_position)
        self.build_slice_poly_data_mapper(file, group_active_array)
        self.build_slice_actor()
        
        self._render_window.Render()

    def render_data_array(self, file: File, new_active_array: str):
        file.data.SetActiveScalars(new_active_array)
        
        self._data_set_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())
        self._slice_poly_data_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())

    def render_representation(self, new_active_representation):
        actor_property = self._actor.GetProperty()
        
        self._actor.VisibilityOn()
        self._slice_actor.VisibilityOff()

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
            self._slice.SetVOI(0, max_x - 1, 0, max_y - 1, slice_position, slice_position)
        elif slice_orientation == const.Planes.YZ:
            self._slice.SetVOI(slice_position, slice_position, 0, max_y - 1, 0, max_z - 1)
        elif slice_orientation == const.Planes.XZ:
            self._slice.SetVOI(0, max_x - 1, slice_position, slice_position, 0, max_z - 1)
        
    def render_axes(self, axes_on: bool):
        self._cube_axes_actor.SetVisibility(axes_on)

    def get_point_information(self, data: vtkImageData, x: float, y: float):
        self._picker.Pick(x, y, 0.0, self._renderer)

        message = ""
        point_id = self._picker.GetPointId()
        
        if point_id != -1:
            point = data.GetPoint(point_id)
            message = f"Id: {point_id}\nX: {point[0]}\nY: {point[1]}\nZ: {point[2]}\n"
        
        return message
    
    def get_cell_information(self, data: vtkImageData, x: float, y: float):
        self._picker.Pick(x, y, 0.0, self._renderer)
        
        message = ""
        cell_id = self._picker.GetCellId()
        
        if cell_id != -1:
            cell_data = data.GetCellData()
            num_of_data_arrays = cell_data.GetNumberOfArrays()
            
            message = f"Id: {cell_id}\n"
            for i in range(num_of_data_arrays):
                data_array = cell_data.GetArray(i)
                message += f"{data_array.GetName()}: {data_array.GetValue(cell_id)}\n"
        
        return message

    def get_camera_params(self):
        camera = self._renderer.GetActiveCamera()
        
        return {
            const.CameraParams.Position: camera.GetPosition(),
            const.CameraParams.FocalPoint: camera.GetFocalPoint(),
            const.CameraParams.ViewUp: camera.GetViewUp(),
            const.CameraParams.ViewAngle: camera.GetViewAngle(),
        }

    def set_camera_params(self, position, focal_point, view_up, view_angle):
        camera = self._renderer.GetActiveCamera()
        
        camera.SetPosition(position)
        camera.SetFocalPoint(focal_point)
        camera.SetViewUp(view_up)
        camera.SetViewAngle(view_angle)
        
        self._renderer.ResetCameraClippingRange()
        self._render_window.Render()

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
