from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkCellPicker,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkActor,
)

from .pipeline_builder import PipelineBuilder
from ..files.file import File
from ..constants import (
    AXES_COLOR,
    DEFAULT_SLICE_POSITION,
    DEFAULT_SLICE_ORIENTATION,
    Planes,
    Representation,
)

class VTIPipeline(PipelineBuilder):
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

    @property
    def render_window(self):
        return self._render_window
        
    @property
    def renderer(self):
        return self._renderer
        
    @property
    def actor(self):
        return self._actor
        
    @property
    def cube_axes_actor(self):
        return self._cube_axes_actor
        
    @property
    def slice_actor(self):
        return self._slice_actor

    def run_vti_pipeline(self, file: File, group_active_array: str):
        self.build_data_set_mapper(file, group_active_array)
        self.build_actor()
        self.build_cube_axes_actor()
        
        self.build_slice(file, DEFAULT_SLICE_POSITION, DEFAULT_SLICE_ORIENTATION)
        self.build_slice_poly_data_mapper(file, group_active_array)
        self.build_slice_actor()
        
        self._render_window.Render()

    def build_data_set_mapper(self, file: File, group_active_array: str):
        self._data_set_mapper.SetInputConnection(file.reader.GetOutputPort())
        self._data_set_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        self._data_set_mapper.SetLookupTable(self._lookup_table)

    def build_actor(self):
        self._actor.SetMapper(self._data_set_mapper)
                
        self._renderer.AddActor(self._actor)
        self._renderer.ResetCamera()

    def build_cube_axes_actor(self):        
        self._cube_axes_actor.GetXAxesLinesProperty().SetColor(*AXES_COLOR)
        self._cube_axes_actor.GetYAxesLinesProperty().SetColor(*AXES_COLOR)
        self._cube_axes_actor.GetZAxesLinesProperty().SetColor(*AXES_COLOR)
        
        self._cube_axes_actor.SetBounds(self._actor.GetBounds())
        self._cube_axes_actor.SetCamera(self._renderer.GetActiveCamera())
        
        self._renderer.AddActor(self._cube_axes_actor)
        self._renderer.ResetCamera()
        
    def build_slice(self, file, slice_position: int, slice_orientation: Planes):
        self._slice.SetInputConnection(file.reader.GetOutputPort())
        image_data = file.reader.GetOutput()
        max_x, max_y, max_z = image_data.GetDimensions()
        
        self.set_slice(slice_position, slice_orientation, max_x, max_y, max_z)

    def build_slice_poly_data_mapper(self, file: File, group_active_array: str):
        self._slice_poly_data_mapper.SetInputConnection(self._slice.GetOutputPort())
        self._slice_poly_data_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        self._slice_poly_data_mapper.SetLookupTable(self._lookup_table)

    def build_slice_actor(self):
        self._slice_actor.SetMapper(self._slice_poly_data_mapper)
        self._slice_actor.GetProperty().LightingOff()

        self._renderer.AddActor(self._slice_actor)
        self._renderer.ResetCamera()

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
    
    def set_file(self, file: File, group_active_array: str):
        file.data.SetActiveScalars(group_active_array)
        self.run_vti_pipeline(file, group_active_array)
        
    def set_data_array(self, file: File, new_active_array: str):
        file.data.SetActiveScalars(new_active_array)
        
        self._data_set_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())
        self._slice_poly_data_mapper.SetScalarRange(file.data.GetArray(new_active_array).GetRange())

    def set_representation(self, new_active_representation):
        actor_property = self._actor.GetProperty()
        
        self._actor.VisibilityOn()
        self._slice_actor.VisibilityOff()

        if new_active_representation == Representation.Points:
            self.set_representation_to_points(actor_property)
        elif new_active_representation == Representation.Surface:
            self.set_representation_to_surface(actor_property)
        elif new_active_representation == Representation.SurfaceWithEdges:
            self.set_representation_to_surface_with_edges(actor_property)
        elif new_active_representation == Representation.Wireframe:
            self.set_representation_to_wireframe(actor_property)

    def set_representation_to_points(self, actor_property):
        actor_property.SetRepresentationToPoints()
        actor_property.SetPointSize(2)
        actor_property.EdgeVisibilityOff()

    def set_representation_to_surface(self, actor_property):
        actor_property.SetRepresentationToSurface()
        actor_property.SetPointSize(1)
        actor_property.EdgeVisibilityOff()
        
    def set_representation_to_surface_with_edges(self, actor_property):
        actor_property.SetRepresentationToSurface()
        actor_property.SetPointSize(1)
        actor_property.EdgeVisibilityOn()

    def set_representation_to_wireframe(self, actor_property):
        actor_property.SetRepresentationToWireframe()
        actor_property.SetPointSize(1)
        actor_property.EdgeVisibilityOff()

    def set_slice(self, slice_position, slice_orientation, max_x, max_y, max_z):
        if slice_orientation == Planes.XY:
            self._slice.SetVOI(0, max_x - 1, 0, max_y - 1, slice_position, slice_position)
        elif slice_orientation == Planes.YZ:
            self._slice.SetVOI(slice_position, slice_position, 0, max_y - 1, 0, max_z - 1)
        elif slice_orientation == Planes.XZ:
            self._slice.SetVOI(0, max_x - 1, slice_position, slice_position, 0, max_z - 1)
        
    def set_axes_visibility(self, axes_visibility):
        if self._cube_axes_actor is not None:
            self._cube_axes_actor.SetVisibility(axes_visibility)
