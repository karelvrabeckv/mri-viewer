from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (
    vtkDataSetMapper,
    vtkActor,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

def vti_pipeline():    
    # Read the source file
    reader = vtkXMLImageDataReader()
    reader.SetFileName("../data/data_time_0.vti") # Temporarily    
    reader.Update()

    # Create the mapper
    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    
    # Create the actor
    actor = vtkActor()
    actor.SetMapper(mapper)

    # Set the default representation
    actor.GetProperty().SetRepresentationToSurface()

    # Create the renderer
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.ResetCamera()
    renderer.SetBackground(vtkNamedColors().GetColor3d("Silver"))    

    # Create the render window
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # Create the interactor
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()
    
    return renderWindow
