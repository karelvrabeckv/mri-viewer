from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersSources import (
    vtkSphereSource,
    vtkCubeSource,
)
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import (
    vtkAxesActor,
    vtkCubeAxesActor,
)
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkCellPicker,
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
)

from mri_viewer.app.files import File

import mri_viewer.app.constants as const

class PipelineFactory:
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

    def create_picker(self):
        return vtkCellPicker()

    def create_picked_point(self, position):
        picked_point = vtkSphereSource()

        picked_point.SetCenter(position)
        picked_point.SetRadius(0.25)
        picked_point.SetPhiResolution(100)
        picked_point.SetThetaResolution(100)

        return picked_point

    def create_picked_point_mapper(self, picked_point):
        picked_point_mapper = vtkPolyDataMapper()

        picked_point_mapper.SetInputConnection(picked_point.GetOutputPort())

        return picked_point_mapper

    def create_picked_point_actor(self, picked_point_mapper):
        picked_point_actor = vtkActor()

        picked_point_actor.SetMapper(picked_point_mapper)
        picked_point_actor.GetProperty().SetColor(vtkNamedColors().GetColor3d("White"))
        picked_point_actor.GetProperty().LightingOff()

        return picked_point_actor

    def create_picked_cell(self, bounds):
        picked_cell = vtkCubeSource()

        picked_cell.SetBounds(
            bounds[0] - const.PICKED_CELL_OFFSET, bounds[1] + const.PICKED_CELL_OFFSET,
            bounds[2] - const.PICKED_CELL_OFFSET, bounds[3] + const.PICKED_CELL_OFFSET,
            bounds[4] - const.PICKED_CELL_OFFSET, bounds[5] + const.PICKED_CELL_OFFSET,
        )
        picked_cell.SetCenter(
            (bounds[0] + bounds[1]) / 2,
            (bounds[2] + bounds[3]) / 2,
            (bounds[4] + bounds[5]) / 2,
        )

        return picked_cell

    def create_picked_cell_mapper(self, picked_cell):
        picked_cell_mapper = vtkPolyDataMapper()

        picked_cell_mapper.SetInputConnection(picked_cell.GetOutputPort())

        return picked_cell_mapper

    def create_picked_cell_actor(self, picked_cell_mapper):
        picked_cell_actor = vtkActor()

        picked_cell_actor.SetMapper(picked_cell_mapper)
        picked_cell_actor.GetProperty().SetColor(vtkNamedColors().GetColor3d("White"))
        picked_cell_actor.GetProperty().SetRepresentationToWireframe()
        picked_cell_actor.GetProperty().SetLineWidth(5)
        picked_cell_actor.GetProperty().LightingOff()

        return picked_cell_actor

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
            rgba = [*color_transfer_function.GetColor(float(value) / 256), 1.0]
            lookup_table.SetTableValue(value, rgba)
        
        return lookup_table

    def create_file_mapper(self, file: File, group_active_array, lookup_table):
        file_mapper = vtkDataSetMapper()
        
        file_mapper.SetInputConnection(file.reader.GetOutputPort())
        file_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        file_mapper.SetLookupTable(lookup_table)

        return file_mapper
    
    def create_file_actor(self, file_mapper):
        file_actor = vtkActor()
        
        file_actor.SetMapper(file_mapper)
        
        return file_actor
        
    def create_cube_axes_actor(self, file_actor, renderer):
        cube_axes_actor = vtkCubeAxesActor()
        
        cube_axes_actor.SetXTitle("X")
        cube_axes_actor.SetYTitle("Y")
        cube_axes_actor.SetZTitle("Z")
        
        cube_axes_actor.GetXAxesLinesProperty().SetColor(*const.AXES_COLOR)
        cube_axes_actor.GetYAxesLinesProperty().SetColor(*const.AXES_COLOR)
        cube_axes_actor.GetZAxesLinesProperty().SetColor(*const.AXES_COLOR)
        
        for i in range(3):
            cube_axes_actor.GetTitleTextProperty(i).SetColor(*const.AXES_COLOR)
            cube_axes_actor.GetLabelTextProperty(i).SetColor(*const.AXES_COLOR)
        
        cube_axes_actor.SetBounds(file_actor.GetBounds())
        cube_axes_actor.SetCamera(renderer.GetActiveCamera())
        
        return cube_axes_actor

    def create_slice(self, file: File):
        slice = vtkExtractVOI()
        
        image_data = file.reader.GetOutput()
        slice.SetInputData(image_data)
        
        return slice

    def create_slice_mapper(self, file: File, slice, group_active_array, lookup_table):
        slice_mapper = vtkPolyDataMapper()
        
        slice_mapper.SetInputConnection(slice.GetOutputPort())
        slice_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        slice_mapper.SetLookupTable(lookup_table)
        
        return slice_mapper

    def create_slice_actor(self, slice_mapper):
        slice_actor = vtkActor()

        slice_actor.SetMapper(slice_mapper)
        slice_actor.GetProperty().LightingOff()
        
        return slice_actor
