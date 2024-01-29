from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkDataSetMapper,
    vtkActor,
)

from .pipeline_builder import PipelineBuilder
from ..file_management.file import VTIFile
from ..constants import (
    AXES_COLOR,
    DEFAULT_PLANE_NORMAL,
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
        
        self._initial_cone = vtkConeSource()
        self._initial_mapper = vtkPolyDataMapper()
        self._initial_actor = vtkActor()
        
        self._data_set_mapper = vtkDataSetMapper()
        self._actor = vtkActor()
        self._cube_axes_actor = vtkCubeAxesActor()
        
        self._slicing_plane = vtkPlane()
        self._slicer = vtkClipDataSet()
        
        self._sliced_data_set_mapper = vtkDataSetMapper()
        self._sliced_actor = vtkActor()
        
        self.create_blank_scene()
        
    @property
    def render_window(self):
        return self._render_window        
        
    @property
    def actor(self):
        return self._actor
        
    @property
    def sliced_actor(self):
        return self._sliced_actor
        
    def create_blank_scene(self):
        self.build_initial_mapper()
        self.build_initial_actor()
        
    def build_initial_mapper(self):
        self._initial_mapper.SetInputConnection(self._initial_cone.GetOutputPort())

    def build_initial_actor(self):
        self._initial_actor.SetMapper(self._initial_mapper)
        self._initial_actor.VisibilityOff()
        
        self._renderer.AddActor(self._initial_actor)
        self._renderer.ResetCamera()

    def run_vti_pipeline(self, file: VTIFile, data_array_name: str):
        self.build_data_set_mapper(file, data_array_name)
        self.build_actor()
        self.build_cube_axes_actor()
        
        self.build_slicing_plane()
        self.build_slicer(file)
        self.build_sliced_data_set_mapper(file)
        self.build_sliced_actor()

    def build_data_set_mapper(self, file: VTIFile, data_array_name: str):
        self._data_set_mapper.SetInputConnection(file.reader.GetOutputPort())
        self._data_set_mapper.SetScalarRange(file.data.GetArray(data_array_name).GetRange())
        self._data_set_mapper.SetLookupTable(self._lookup_table)

    def build_actor(self):
        self._actor.SetMapper(self._data_set_mapper)

        self._renderer.AddActor(self._actor)
        self._renderer.ResetCamera()

    def build_cube_axes_actor(self):
        self._cube_axes_actor.SetXTitle("X-Axis")
        self._cube_axes_actor.SetYTitle("Y-Axis")
        self._cube_axes_actor.SetZTitle("Z-Axis")
        
        self._cube_axes_actor.GetXAxesLinesProperty().SetColor(*AXES_COLOR)
        self._cube_axes_actor.GetYAxesLinesProperty().SetColor(*AXES_COLOR)
        self._cube_axes_actor.GetZAxesLinesProperty().SetColor(*AXES_COLOR)
        
        self._cube_axes_actor.SetBounds(self._actor.GetBounds())
        self._cube_axes_actor.SetCamera(self._renderer.GetActiveCamera())
        
        self._renderer.AddActor(self._cube_axes_actor)
        self._renderer.ResetCamera()
        
    def build_slicing_plane(self):
        self._slicing_plane.SetNormal(*DEFAULT_PLANE_NORMAL)
        self._slicing_plane.SetOrigin(0, 0, 0)

    def build_slicer(self, file):
        self._slicer.SetInputConnection(file.reader.GetOutputPort())
        self._slicer.SetClipFunction(self._slicing_plane)
        self._slicer.GenerateClippedOutputOn()
        
    def build_sliced_data_set_mapper(self, file: VTIFile):
        self._sliced_data_set_mapper.SetInputConnection(self._slicer.GetOutputPort())
        self._sliced_data_set_mapper.SetScalarRange(file.data.GetArray(file.active_array).GetRange())
        self._sliced_data_set_mapper.SetLookupTable(self._lookup_table)     

    def build_sliced_actor(self):
        self._sliced_actor.SetMapper(self._sliced_data_set_mapper)
        self._sliced_actor.GetProperty().LightingOff()

        self._renderer.AddActor(self._sliced_actor)
        self._renderer.ResetCamera()
        
    def set_file(self, file: VTIFile, group_data_array_name: str):
        data_array_name = group_data_array_name
        if data_array_name not in file.data_arrays:
            data_array_name = file.active_array
        
        file.data.SetActiveScalars(data_array_name)
        file.active_array = data_array_name
        
        self.run_vti_pipeline(file, data_array_name)
        
    def set_data_array(self, file: VTIFile, data_array_name: str):
        file.data.SetActiveScalars(data_array_name)
        file.active_array = data_array_name
        
        self._data_set_mapper.SetScalarRange(file.data.GetArray(data_array_name).GetRange())
        self._sliced_data_set_mapper.SetScalarRange(file.data.GetArray(data_array_name).GetRange())

    def set_representation(self, representation):
        actor_property = self._actor.GetProperty()
        
        self._actor.VisibilityOn()
        self._sliced_actor.VisibilityOff()

        if representation == Representation.Points:
            self.set_representation_to_points(actor_property)
        elif representation == Representation.Surface:
            self.set_representation_to_surface(actor_property)
        elif representation == Representation.SurfaceWithEdges:
            self.set_representation_to_surface_with_edges(actor_property)
        elif representation == Representation.Wireframe:
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

    def set_slice_orientation(self, current_slice_orientation):
        if current_slice_orientation == Planes.XY:
            self._slicing_plane.SetNormal(*Planes.XYNormal)
        elif current_slice_orientation == Planes.YZ:
            self._slicing_plane.SetNormal(*Planes.YZNormal)
        elif current_slice_orientation == Planes.XZ:
            self._slicing_plane.SetNormal(*Planes.XZNormal)

    def set_slice_position(self, current_slice_orientation, current_slice_position):
        if current_slice_orientation == Planes.XY:
            self._slicing_plane.SetOrigin(0, 0, current_slice_position)
        elif current_slice_orientation == Planes.YZ:
            self._slicing_plane.SetOrigin(current_slice_position, 0, 0)
        elif current_slice_orientation == Planes.XZ:
            self._slicing_plane.SetOrigin(0, current_slice_position, 0)
        
    def set_axes_visibility(self, axes_visibility):
        if self._cube_axes_actor is not None:
            self._cube_axes_actor.SetVisibility(axes_visibility)
