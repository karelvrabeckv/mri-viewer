APPLICATION_NAME = "MRI Viewer"

class Representation:
    Points = 0
    Surface = 1
    SurfaceWithEdges = 2
    Wireframe = 3

DEFAULT_REPRESENTATION = Representation.Surface

COLD_TEMPERATURE_COLOR = (0.230, 0.299, 0.754)
LUKEWARM_TEMPERATURE_COLOR = (0.865, 0.865, 0.865)
HOT_TEMPERATURE_COLOR = (0.706, 0.016, 0.15)

BLACK_COLOR = (0.0, 0.0, 0.0)
