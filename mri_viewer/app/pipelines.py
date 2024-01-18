from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (
    vtkDataSetMapper,
    vtkActor,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from .callbacks import set_representation

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

        # Create the mapper
        self._mapper = vtkDataSetMapper()
        self._mapper.SetInputConnection(self._reader.GetOutputPort())
        
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
