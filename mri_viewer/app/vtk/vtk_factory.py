from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersSources import (
    vtkSphereSource,
    vtkCubeSource,
)
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import (
    vtkAxesActor,
    vtkCubeAxesActor,
    vtkScalarBarActor,
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

from mri_viewer.app.files import File, FileGroup

import mri_viewer.app.constants as const

class VTKFactory:
    def create_renderer(self):
        renderer = vtkRenderer()
        
        renderer.SetBackground(vtkNamedColors().GetColor3d(const.DEFAULT_BACKGROUND_COLOR))
        
        return renderer
         
    def create_render_window(self, renderer: vtkRenderer):
        render_window = vtkRenderWindow()
        
        render_window.OffScreenRenderingOn()
        render_window.AddRenderer(renderer)
        
        return render_window

    def create_render_window_interactor(self, render_window: vtkRenderWindow):
        render_window_interactor = vtkRenderWindowInteractor()
        
        render_window_interactor.SetRenderWindow(render_window)
        
        return render_window_interactor

    def create_picker(self):
        return vtkCellPicker()

    def create_picked_point(self, position):
        picked_point = vtkSphereSource()

        self.set_picked_point_properties(picked_point, position)

        return picked_point

    def set_picked_point_properties(self, picked_point: vtkSphereSource, position):
        picked_point.SetCenter(position)
        picked_point.SetRadius(0.25)
        picked_point.SetPhiResolution(100)
        picked_point.SetThetaResolution(100)

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

        self.set_picked_cell_properties(picked_cell, bounds)

        return picked_cell

    def set_picked_cell_properties(self, picked_cell: vtkCubeSource, bounds):
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
        axes_widget.SetViewport(0.0, 0.0, 0.3, 0.3)
        
        axes_widget.EnabledOn()
        
        return axes_widget

    def create_color_transfer_function(self, group: FileGroup):
        color_transfer_function = vtkColorTransferFunction()
        
        if group.color_map == const.ColorMaps.CoolToWarm:
            self.set_color_map_cool_to_warm(color_transfer_function)
        elif group.color_map == const.ColorMaps.Grayscale:
            self.set_color_map_grayscale(color_transfer_function)
        
        return color_transfer_function

    def set_color_map_cool_to_warm(self, color_transfer_function: vtkColorTransferFunction):
        color_transfer_function.SetColorSpaceToDiverging()

        for point in const.COOL_TO_WARM_COLOR_MAP:
            color_transfer_function.AddRGBPoint(point, *const.COOL_TO_WARM_COLOR_MAP[point])

    def set_color_map_grayscale(self, color_transfer_function: vtkColorTransferFunction):
        color_transfer_function.SetColorSpaceToRGB()

        for point in const.GRAYSCALE_COLOR_MAP:
            color_transfer_function.AddRGBPoint(point, *const.GRAYSCALE_COLOR_MAP[point])

    def create_lookup_table(self, color_transfer_function: vtkColorTransferFunction):
        lookup_table = vtkLookupTable()
        
        lookup_table.SetNumberOfTableValues(256)
        lookup_table.Build()
        
        self.set_lookup_table_values(color_transfer_function, lookup_table)
        
        return lookup_table

    def set_lookup_table_values(self, color_transfer_function: vtkColorTransferFunction, lookup_table: vtkLookupTable):
        for value in range(256):
            rgba = [*color_transfer_function.GetColor(float(value) / 256), 1.0]
            lookup_table.SetTableValue(value, rgba)

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
        
        cube_axes_actor.SetXTitle(const.Axis.X)
        cube_axes_actor.SetYTitle(const.Axis.Y)
        cube_axes_actor.SetZTitle(const.Axis.Z)
        
        cube_axes_actor.GetXAxesLinesProperty().SetColor(*const.DEFAULT_TEXT_COLOR)
        cube_axes_actor.GetYAxesLinesProperty().SetColor(*const.DEFAULT_TEXT_COLOR)
        cube_axes_actor.GetZAxesLinesProperty().SetColor(*const.DEFAULT_TEXT_COLOR)
        
        for i in range(3):
            cube_axes_actor.GetTitleTextProperty(i).SetColor(*const.DEFAULT_TEXT_COLOR)
            cube_axes_actor.GetLabelTextProperty(i).SetColor(*const.DEFAULT_TEXT_COLOR)
        
        cube_axes_actor.SetBounds(file_actor.GetBounds())
        cube_axes_actor.SetCamera(renderer.GetActiveCamera())
        cube_axes_actor.SetFlyModeToOuterEdges()
        
        return cube_axes_actor

    def create_scalar_bar_actor(self, file: File, lookup_table):
        scalar_bar = vtkScalarBarActor()

        scalar_bar.SetTitle(file.data_array)
        scalar_bar.SetLookupTable(lookup_table)

        scalar_bar.GetTitleTextProperty().SetColor(*const.DEFAULT_TEXT_COLOR)
        scalar_bar.GetLabelTextProperty().SetColor(*const.DEFAULT_TEXT_COLOR)

        return scalar_bar

    def create_slice(self, file: File):
        slice = vtkExtractVOI()
        
        image_data = file.reader.GetOutput()
        slice.SetInputData(image_data)
        
        return slice

    def create_slice_mapper(self, file: File, slice, group_active_array, lookup_table):
        slice_mapper = vtkDataSetMapper()
        
        slice_mapper.SetInputConnection(slice.GetOutputPort())
        slice_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        slice_mapper.SetLookupTable(lookup_table)
        
        return slice_mapper

    def create_slice_actor(self, slice_mapper):
        slice_actor = vtkActor()

        slice_actor.SetMapper(slice_mapper)
        slice_actor.GetProperty().LightingOff()
        
        return slice_actor
