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

class VTKCreator:
    """Class for generating VTK objects."""

    def create_renderer(self, background):
        """Create renderer to control rendering process for objects."""

        renderer = vtkRenderer()
        
        renderer.SetBackground(background)
        
        return renderer
         
    def create_render_window(self, renderer: vtkRenderer):
        """Create window where renderers draw their images."""

        render_window = vtkRenderWindow()
        
        # Hides VTK window
        render_window.OffScreenRenderingOn()

        render_window.AddRenderer(renderer)
        
        return render_window

    def create_render_window_interactor(self, render_window: vtkRenderWindow):
        """Create interaction mechanism for mouse events."""

        render_window_interactor = vtkRenderWindowInteractor()
        
        render_window_interactor.SetRenderWindow(render_window)
        
        return render_window_interactor

    def create_picker(self):
        """Create picker to shoot rays into scene and return information about object hit."""
        
        return vtkCellPicker()

    def create_picked_point(self, position):
        """Create polygonal sphere as result of picking."""
        
        picked_point = vtkSphereSource()

        self.set_picked_point_properties(picked_point, position)

        return picked_point

    def set_picked_point_properties(self, picked_point: vtkSphereSource, position):
        """Set properties to polygonal sphere."""
        
        picked_point.SetCenter(position)
        picked_point.SetRadius(const.PickedParams.PointRadius)
        picked_point.SetPhiResolution(const.PickedParams.PointResolution)
        picked_point.SetThetaResolution(const.PickedParams.PointResolution)

    def create_picked_point_actor(self, picked_point_mapper):
        """Create object to represent point in scene."""
        
        picked_point_actor = vtkActor()

        picked_point_actor.SetMapper(picked_point_mapper)
    
        picked_point_actor.GetProperty().SetColor(const.Theme.WhiteColor)
        picked_point_actor.GetProperty().LightingOff()

        return picked_point_actor

    def create_picked_cell(self, bounds):
        """Create polygonal cube as result of picking."""
        
        picked_cell = vtkCubeSource()

        self.set_picked_cell_properties(picked_cell, bounds)

        return picked_cell

    def set_picked_cell_properties(self, picked_cell: vtkCubeSource, bounds):
        """Set properties to polygonal cube."""
        
        picked_cell.SetBounds(
            bounds[0] - const.PickedParams.CellOffset, bounds[1] + const.PickedParams.CellOffset,
            bounds[2] - const.PickedParams.CellOffset, bounds[3] + const.PickedParams.CellOffset,
            bounds[4] - const.PickedParams.CellOffset, bounds[5] + const.PickedParams.CellOffset,
        )
        picked_cell.SetCenter(
            (bounds[0] + bounds[1]) / 2,
            (bounds[2] + bounds[3]) / 2,
            (bounds[4] + bounds[5]) / 2,
        )

    def create_picked_cell_actor(self, picked_cell_mapper):
        """Create object to represent cell in scene."""
        
        picked_cell_actor = vtkActor()

        picked_cell_actor.SetMapper(picked_cell_mapper)

        picked_cell_actor.GetProperty().SetColor(const.Theme.WhiteColor)
        picked_cell_actor.GetProperty().SetRepresentationToWireframe()
        picked_cell_actor.GetProperty().SetLineWidth(const.PickedParams.CellLineWidth)
        picked_cell_actor.GetProperty().LightingOff()

        return picked_cell_actor

    def create_picked_primitive_mapper(self, picked_primitive):
        """Create object to map polygonal data to graphics primitives."""
        
        picked_primitive_mapper = vtkPolyDataMapper()

        picked_primitive_mapper.SetInputConnection(picked_primitive.GetOutputPort())

        return picked_primitive_mapper

    def create_axes_widget(self, render_window_interactor: vtkRenderWindowInteractor):
        """Create widget to represent 3D axes in scene."""
        
        axes_widget = vtkOrientationMarkerWidget()
        
        axes_widget.SetOrientationMarker(vtkAxesActor())
        axes_widget.SetInteractor(render_window_interactor)
        axes_widget.SetViewport(0.0, 0.0, 0.3, 0.3)
        
        axes_widget.EnabledOn()
        
        return axes_widget
    
    def create_color_transfer_function(self, group: FileGroup):
        """Create function for color mapping."""
        
        color_transfer_function = vtkColorTransferFunction()
        
        if group.color_map == const.ColorMaps.CoolToWarm:
            self.set_color_map_cool_to_warm(color_transfer_function)
        elif group.color_map == const.ColorMaps.Grayscale:
            self.set_color_map_grayscale(color_transfer_function)
        
        return color_transfer_function

    def set_color_map_cool_to_warm(self, color_transfer_function: vtkColorTransferFunction):
        """Set temperature colors to color mapping function."""
        
        color_transfer_function.SetColorSpaceToDiverging()

        for point in const.COOL_TO_WARM_COLOR_MAP:
            color_transfer_function.AddRGBPoint(point, *const.COOL_TO_WARM_COLOR_MAP[point])

    def set_color_map_grayscale(self, color_transfer_function: vtkColorTransferFunction):
        """Set grayscale colors to color mapping function."""
        
        color_transfer_function.SetColorSpaceToRGB()

        for point in const.GRAYSCALE_COLOR_MAP:
            color_transfer_function.AddRGBPoint(point, *const.GRAYSCALE_COLOR_MAP[point])

    def create_lookup_table(self, color_transfer_function: vtkColorTransferFunction):
        """Create table for mapping scalar values to colors."""
        
        lookup_table = vtkLookupTable()
        
        lookup_table.SetNumberOfTableValues(const.NUM_OF_LOOKUP_TABLE_VALUES)
        lookup_table.Build()
        
        self.set_lookup_table_values(color_transfer_function, lookup_table)
        
        return lookup_table

    def set_lookup_table_values(self, color_transfer_function: vtkColorTransferFunction, lookup_table: vtkLookupTable):
        """Set colors to table based on color mapping function."""

        for value in range(const.NUM_OF_LOOKUP_TABLE_VALUES):
            rgba = [*color_transfer_function.GetColor(float(value) / const.NUM_OF_LOOKUP_TABLE_VALUES), 1.0]
            lookup_table.SetTableValue(value, rgba)

    def create_file_mapper(self, file: File, group_active_array, lookup_table):
        """Create object to map data set to graphics primitives."""
        
        file_mapper = vtkDataSetMapper()
        
        file_mapper.SetInputConnection(file.reader.GetOutputPort())
        file_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        file_mapper.SetLookupTable(lookup_table)

        return file_mapper
    
    def create_file_actor(self, file_mapper):
        """Create object to represent file in scene."""
        
        file_actor = vtkActor()
        
        file_actor.SetMapper(file_mapper)
        
        return file_actor
        
    def create_cube_axes_actor(self, file_actor: vtkActor, color, renderer: vtkRenderer):
        """Create object to represent axes grid in scene."""
        
        cube_axes_actor = vtkCubeAxesActor()
        
        cube_axes_actor.SetXTitle(const.Axes.X)
        cube_axes_actor.SetYTitle(const.Axes.Y)
        cube_axes_actor.SetZTitle(const.Axes.Z)
        
        self.set_cube_axes_actor_colors(cube_axes_actor, color)
        
        cube_axes_actor.SetBounds(file_actor.GetBounds())
        cube_axes_actor.SetCamera(renderer.GetActiveCamera())

        # Display axes on outer edges 
        cube_axes_actor.SetFlyModeToOuterEdges()
        
        return cube_axes_actor

    def set_cube_axes_actor_colors(self, cube_axes_actor: vtkCubeAxesActor, color):
        """Set colors to axes grid."""
        
        cube_axes_actor.GetXAxesLinesProperty().SetColor(*color)
        cube_axes_actor.GetYAxesLinesProperty().SetColor(*color)
        cube_axes_actor.GetZAxesLinesProperty().SetColor(*color)
        
        for i in range(3):
            cube_axes_actor.GetTitleTextProperty(i).SetColor(*color)
            cube_axes_actor.GetLabelTextProperty(i).SetColor(*color)

    def create_scalar_bar_actor(self, group: FileGroup, lookup_table, color):
        """Create object to represent side scalar scale in scene."""
        
        scalar_bar = vtkScalarBarActor()

        scalar_bar.SetTitle(group.data_array)
        scalar_bar.SetLookupTable(lookup_table)

        self.set_scalar_bar_actor_colors(scalar_bar, color)

        return scalar_bar

    def set_scalar_bar_actor_colors(self, scalar_bar: vtkScalarBarActor, color):
        """Set colors to side scalar scale."""
        
        scalar_bar.GetTitleTextProperty().SetColor(*color)
        scalar_bar.GetLabelTextProperty().SetColor(*color)

    def create_slice(self, file: File):
        """Create filter to select volume of interest from data set."""
        
        slice = vtkExtractVOI()
        
        image_data = file.reader.GetOutput()
        slice.SetInputData(image_data)
        
        return slice

    def create_slice_mapper(self, file: File, slice: vtkExtractVOI, group_active_array, lookup_table):
        """Create object to map slice to graphics primitives."""
        
        slice_mapper = vtkDataSetMapper()
        
        slice_mapper.SetInputConnection(slice.GetOutputPort())
        slice_mapper.SetScalarRange(file.data.GetArray(group_active_array).GetRange())
        slice_mapper.SetLookupTable(lookup_table)
        
        return slice_mapper

    def create_slice_actor(self, slice_mapper):
        """Create object to represent slice in scene."""
        
        slice_actor = vtkActor()

        slice_actor.SetMapper(slice_mapper)
        slice_actor.GetProperty().LightingOff()
        
        return slice_actor
