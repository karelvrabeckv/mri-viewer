from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkActor,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from .constants import (
    Representation,
    COLD_TEMPERATURE_COLOR,
    LUKEWARM_TEMPERATURE_COLOR,
    HOT_TEMPERATURE_COLOR,
    BLACK_COLOR,
)

class VTIPipeline:
    def __init__(self):
        self._colors = vtkNamedColors()
        self._file_mapper = vtkDataSetMapper()
        self._file_actor = vtkActor()
        self._axes_actor = vtkCubeAxesActor()
        
        self.build_renderer()
        self.build_render_window()
        self.build_render_window_interactor()

        self.build_color_transfer_function()
        self.build_lookup_table()
        
        self.build_axes_actor()
        
    @property
    def render_window(self):
        return self._render_window

    @property
    def axes_actor(self):
        return self._axes_actor

    def build_renderer(self):
        self._renderer = vtkRenderer()
        self._renderer.SetBackground(self._colors.GetColor3d("Gainsboro"))
         
    def build_render_window(self):
        self._render_window = vtkRenderWindow()
        self._render_window.AddRenderer(self._renderer)

    def build_render_window_interactor(self):
        self._render_window_interactor = vtkRenderWindowInteractor()
        self._render_window_interactor.SetRenderWindow(self._render_window)
        
    def build_color_transfer_function(self):
        self._color_transfer_function = vtkColorTransferFunction()
        self._color_transfer_function.SetColorSpaceToDiverging()
        
        self._color_transfer_function.AddRGBPoint(0.0, *COLD_TEMPERATURE_COLOR)
        self._color_transfer_function.AddRGBPoint(0.5, *LUKEWARM_TEMPERATURE_COLOR)
        self._color_transfer_function.AddRGBPoint(1.0, *HOT_TEMPERATURE_COLOR)

    def build_lookup_table(self):
        self._lookup_table = vtkLookupTable()
        self._lookup_table.SetNumberOfTableValues(256)
        self._lookup_table.Build()
        
        for i in range(256):
            rgba = [*self._color_transfer_function.GetColor(float(i) / 256), 1]
            self._lookup_table.SetTableValue(i, rgba)

    def build_file_mapper(self, file, data_array):
        self._file_mapper.SetInputConnection(file.reader.GetOutputPort())
        self._file_mapper.SetScalarRange(file.data.GetArray(data_array).GetRange())
        self._file_mapper.SetLookupTable(self._lookup_table)

    def build_file_actor(self):
        self._file_actor.SetMapper(self._file_mapper)
        
        self._renderer.AddActor(self._file_actor)
        self._renderer.ResetCamera()
        
    def build_axes_actor(self):
        self._axes_actor.SetXTitle("X-Axis")
        self._axes_actor.SetYTitle("Y-Axis")
        self._axes_actor.SetZTitle("Z-Axis")
        
        self._axes_actor.GetXAxesLinesProperty().SetColor(*BLACK_COLOR)
        self._axes_actor.GetYAxesLinesProperty().SetColor(*BLACK_COLOR)
        self._axes_actor.GetZAxesLinesProperty().SetColor(*BLACK_COLOR)
        
        self._axes_actor.SetBounds(self._file_actor.GetBounds())
        self._axes_actor.SetCamera(self._renderer.GetActiveCamera())
        
        self._renderer.AddActor(self._axes_actor)
        self._renderer.ResetCamera()
        
    def set_file(self, file, group_data_array):
        data_array = group_data_array
        if data_array not in file.data_arrays:
            data_array = file.active_array
        
        file.data.SetActiveScalars(data_array)
        file.active_array = data_array    
        
        self.build_file_mapper(file, data_array)
        self.build_file_actor()
        self.build_axes_actor()
        
    def set_data_array(self, file, data_array):
        file.data.SetActiveScalars(data_array)
        file.active_array = data_array
        
        self._file_mapper.SetScalarRange(file.data.GetArray(data_array).GetRange())

    def set_representation(self, representation):
        property = self._file_actor.GetProperty()
        
        if representation == Representation.Points:
            property.SetRepresentationToPoints()
            property.SetPointSize(2)
            property.EdgeVisibilityOff()
        elif representation == Representation.Surface:
            property.SetRepresentationToSurface()
            property.SetPointSize(1)
            property.EdgeVisibilityOff()
        elif representation == Representation.SurfaceWithEdges:
            property.SetRepresentationToSurface()
            property.SetPointSize(1)
            property.EdgeVisibilityOn()
        elif representation == Representation.Wireframe:
            property.SetRepresentationToWireframe()
            property.SetPointSize(1)
            property.EdgeVisibilityOff()
