from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkDataSetMapper,
    vtkMapper,
    vtkActor,
)

from ..constants import (
    BACKGROUND_COLOR,
    AXES_COLOR,
    COLD_TEMPERATURE_COLOR,
    LUKEWARM_TEMPERATURE_COLOR,
    HOT_TEMPERATURE_COLOR,
)

class PipelineBuilder:
    def build_renderer(self):
        renderer = vtkRenderer()
        
        renderer.SetBackground(vtkNamedColors().GetColor3d(BACKGROUND_COLOR))
        
        return renderer
         
    def build_render_window(self, renderer: vtkRenderer):
        render_window = vtkRenderWindow()
        
        render_window.AddRenderer(renderer)
        
        return render_window

    def build_render_window_interactor(self, render_window: vtkRenderWindow):
        render_window_interactor = vtkRenderWindowInteractor()
        
        render_window_interactor.SetRenderWindow(render_window)
        
        return render_window_interactor

    def build_color_transfer_function(self):
        color_transfer_function = vtkColorTransferFunction()
        
        color_transfer_function.SetColorSpaceToDiverging()
        
        color_transfer_function.AddRGBPoint(0.0, *COLD_TEMPERATURE_COLOR)
        color_transfer_function.AddRGBPoint(0.5, *LUKEWARM_TEMPERATURE_COLOR)
        color_transfer_function.AddRGBPoint(1.0, *HOT_TEMPERATURE_COLOR)
        
        return color_transfer_function

    def build_lookup_table(self, color_transfer_function: vtkColorTransferFunction):
        lookup_table = vtkLookupTable()
        
        lookup_table.SetNumberOfTableValues(256)
        lookup_table.Build()
        
        for value in range(256):
            rgba = [*color_transfer_function.GetColor(float(value) / 256), 1]
            lookup_table.SetTableValue(value, rgba)
        
        return lookup_table

    def build_poly_data_mapper(self, source):
        mapper = vtkPolyDataMapper()
        
        mapper.SetInputConnection(source.GetOutputPort())
        
        return mapper

    def build_data_set_mapper(self, source, data, data_array_name: str, lookup_table: vtkLookupTable):
        mapper = vtkDataSetMapper()
        
        mapper.SetInputConnection(source.GetOutputPort())
        mapper.SetScalarRange(data.GetArray(data_array_name).GetRange())
        mapper.SetLookupTable(lookup_table)
        
        return mapper

    def build_actor(self, mapper: vtkMapper, renderer: vtkRenderer):
        actor = vtkActor()
        
        actor.SetMapper(mapper)
        
        renderer.AddActor(actor)
        renderer.ResetCamera()
        
        return actor

    def build_cube_axes_actor(self, actor: vtkActor, renderer: vtkRenderer):
        cube_axes_actor = vtkCubeAxesActor()
        
        cube_axes_actor.SetXTitle("X-Axis")
        cube_axes_actor.SetYTitle("Y-Axis")
        cube_axes_actor.SetZTitle("Z-Axis")
        
        cube_axes_actor.GetXAxesLinesProperty().SetColor(*AXES_COLOR)
        cube_axes_actor.GetYAxesLinesProperty().SetColor(*AXES_COLOR)
        cube_axes_actor.GetZAxesLinesProperty().SetColor(*AXES_COLOR)
        
        cube_axes_actor.SetBounds(actor.GetBounds())
        cube_axes_actor.SetCamera(renderer.GetActiveCamera())
        
        renderer.AddActor(cube_axes_actor)
        renderer.ResetCamera()
        
        return cube_axes_actor

    def build_slicing_plane(self, normal: tuple, origin: tuple):
        plane = vtkPlane()
        
        plane.SetNormal(*normal)
        plane.SetOrigin(*origin)
        
        return plane

    def build_slicer(self, source, plane: vtkPlane):
        slicer = vtkClipDataSet()
        
        slicer.SetInputConnection(source.GetOutputPort())
        slicer.SetClipFunction(plane)
        slicer.GenerateClippedOutputOn()
        
        return slicer
