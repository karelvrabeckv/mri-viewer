from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import mri_viewer.app.constants as const

class PipelineBuilder:
    def create_renderer(self):
        renderer = vtkRenderer()
        
        renderer.SetBackground(vtkNamedColors().GetColor3d(const.BACKGROUND_COLOR))
        
        return renderer
         
    def create_render_window(self, renderer: vtkRenderer):
        render_window = vtkRenderWindow()
        
        render_window.OffScreenRenderingOn()
        render_window.AddRenderer(renderer)
        
        return render_window

    def create_render_window_interactor(self, render_window: vtkRenderWindow):
        render_window_interactor = vtkRenderWindowInteractor()
        
        render_window_interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
        render_window_interactor.SetRenderWindow(render_window)
        
        return render_window_interactor

    def create_axes_widget(self, render_window_interactor: vtkRenderWindowInteractor):
        axes_widget = vtkOrientationMarkerWidget()
        
        axes_widget.SetOrientationMarker(vtkAxesActor())
        axes_widget.SetInteractor(render_window_interactor)
        axes_widget.SetViewport(0.0, 0.0, 0.35, 0.35)
        
        axes_widget.EnabledOn()
        
        return axes_widget

    def create_color_transfer_function(self):
        color_transfer_function = vtkColorTransferFunction()
        
        color_transfer_function.SetColorSpaceToDiverging()
        
        color_transfer_function.AddRGBPoint(0.0, *const.COLD_TEMPERATURE_COLOR)
        color_transfer_function.AddRGBPoint(0.5, *const.LUKEWARM_TEMPERATURE_COLOR)
        color_transfer_function.AddRGBPoint(1.0, *const.HOT_TEMPERATURE_COLOR)
        
        return color_transfer_function

    def create_lookup_table(self, color_transfer_function: vtkColorTransferFunction):
        lookup_table = vtkLookupTable()
        
        lookup_table.SetNumberOfTableValues(256)
        lookup_table.Build()
        
        for value in range(256):
            rgba = [*color_transfer_function.GetColor(float(value) / 256), 1]
            lookup_table.SetTableValue(value, rgba)
        
        return lookup_table
