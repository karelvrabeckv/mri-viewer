from vtkmodules.vtkFiltersSources import vtkConeSource

from .pipeline_builder import PipelineBuilder
from ..file_management.vti_file import VTIFile
from ..constants import DEFAULT_PLANE_NORMAL, Planes, Representation

class VTIPipeline(PipelineBuilder):
    def __init__(self):
        self._renderer = self.build_renderer()
        self._render_window = self.build_render_window(self._renderer)
        self._render_window_interactor = self.build_render_window_interactor(self._render_window)
        self._color_transfer_function = self.build_color_transfer_function()
        self._lookup_table = self.build_lookup_table(self._color_transfer_function)
        
        self._data_set_mapper = None
        self._actor = None
        self._cube_axes_actor = None
        
        self._plane = None
        self._slicer = None
        
        self._sliced_data_set_mapper = None
        self._sliced_actor = None
        
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
        mapper = self.build_poly_data_mapper(vtkConeSource())
        actor = self.build_actor(mapper, self._renderer)
        actor.VisibilityOff()
    
    def run_vti_pipeline(self, file: VTIFile, data_array_name: str):
        self._data_set_mapper = self.build_data_set_mapper(file.reader, file.data, data_array_name, self._lookup_table)
        self._actor = self.build_actor(self._data_set_mapper, self._renderer)
        self._cube_axes_actor = self.build_cube_axes_actor(self._actor, self._renderer)
        
        self._slicing_plane = self.build_slicing_plane(DEFAULT_PLANE_NORMAL, (0, 0, 0))
        self._slicer = self.build_slicer(file.reader, self._slicing_plane)
        self._sliced_data_set_mapper = self.build_data_set_mapper(self._slicer, file.data, file.active_array, self._lookup_table)
        self._sliced_actor = self.build_actor(self._sliced_data_set_mapper, self._renderer)
        self._sliced_actor.GetProperty().LightingOff()
        
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
