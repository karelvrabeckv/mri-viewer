from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkRenderingCore import (
    vtkDataSetMapper,
    vtkColorTransferFunction,
    vtkActor,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from .constants import (
    Representation,
    COLD_TEMPERATURE_COLOR,
    LUKEWARM_TEMPERATURE_COLOR,
    HOT_TEMPERATURE_COLOR
)

class VTIPipeline:
    def __init__(self, representation):
        self.run(representation)
        
    @property
    def reader(self):
        return self._reader

    @property
    def data(self):
        return self._data
    
    @property
    def activeArray(self):
        return self._activeArray

    @property
    def dataArrays(self):
        return self._dataArrays

    @property
    def mapper(self):
        return self._mapper
    
    @property
    def actor(self):
        return self._actor
    
    @property
    def renderer(self):
        return self._renderer
    
    @property
    def renderWindow(self):
        return self._renderWindow
    
    @property
    def renderWindowInteractor(self):
        return self._renderWindowInteractor
    
    def run(self, representation):    
        # Read the source file
        self._reader = vtkXMLImageDataReader()
        self._reader.SetFileName("../data/data_time_0.vti") # Temporarily    
        self._reader.Update()

        # Add temperature colors
        ctf = vtkColorTransferFunction()
        ctf.SetColorSpaceToDiverging()

        ctf.AddRGBPoint(0.0, *COLD_TEMPERATURE_COLOR)
        ctf.AddRGBPoint(0.5, *LUKEWARM_TEMPERATURE_COLOR)
        ctf.AddRGBPoint(1.0, *HOT_TEMPERATURE_COLOR)

        # Create the lookup table
        lut = vtkLookupTable()
        lut.SetNumberOfTableValues(256)
        lut.Build()
        
        # Transfer the colors to the table
        for i in range(256):
            rgba = [*ctf.GetColor(float(i) / 256), 1]
            lut.SetTableValue(i, rgba)

        # Explore the data
        image_data = self._reader.GetOutput()
        
        point_data = image_data.GetPointData()
        cell_data = image_data.GetCellData()
        
        num_of_point_arrays = point_data.GetNumberOfArrays()
        num_of_cell_arrays = cell_data.GetNumberOfArrays()
        
        if num_of_point_arrays:
            self._data = point_data
            self._activeArray = point_data.GetScalars().GetName()
            self._dataArrays = [point_data.GetArray(x).GetName() for x in range(num_of_point_arrays)]
        elif num_of_cell_arrays:
            self._data = cell_data
            self._activeArray = cell_data.GetScalars().GetName()
            self._dataArrays = [cell_data.GetArray(x).GetName() for x in range(num_of_cell_arrays)]
        else:
            return

        # Create the mapper
        self._mapper = vtkDataSetMapper()
        self._mapper.SetInputConnection(self._reader.GetOutputPort())
        self._mapper.SetScalarRange(self._data.GetArray(self._activeArray).GetRange())
        self._mapper.SetLookupTable(lut)
        
        # Create the actor
        self._actor = vtkActor()
        self._actor.SetMapper(self._mapper)

        # Set the default representation
        self.set_representation(representation)

        # Create the renderer
        self._renderer = vtkRenderer()
        self._renderer.AddActor(self._actor)
        self._renderer.ResetCamera()
        self._renderer.SetBackground(vtkNamedColors().GetColor3d("Silver"))    

        # Create the render window
        self._renderWindow = vtkRenderWindow()
        self._renderWindow.AddRenderer(self._renderer)

        # Create the interactor
        self._renderWindowInteractor = vtkRenderWindowInteractor()
        self._renderWindowInteractor.SetRenderWindow(self._renderWindow)

    def set_representation(self, representation):
        property = self._actor.GetProperty()
        
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

    def set_data_array(self, data_array):
        self._data.SetActiveScalars(data_array)
        self._activeArray = data_array
        self._mapper.SetScalarRange(self._data.GetArray(data_array).GetRange())
