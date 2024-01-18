from .constants import Representation

def set_representation(actor, representation):
    property = actor.GetProperty()
    
    if representation == Representation.Points:
        property.SetRepresentationToPoints()
        property.SetPointSize(3)
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
