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

from .callbacks import set_representation
from .constants import (
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
            active_array = point_data.GetScalars()
        elif num_of_cell_arrays:
            active_array = cell_data.GetScalars()
        else:
            return

        # Create the mapper
        self._mapper = vtkDataSetMapper()
        self._mapper.SetInputConnection(self._reader.GetOutputPort())
        self._mapper.SetScalarRange(active_array.GetRange())
        self._mapper.SetLookupTable(lut)
        
        # Create the actor
        self._actor = vtkActor()
        self._actor.SetMapper(self._mapper)

        # Set the default representation
        set_representation(self._actor, representation)

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
        self._renderWindowInteractor.Initialize()
        self._renderWindowInteractor.Start()
