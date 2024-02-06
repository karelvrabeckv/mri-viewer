APPLICATION_NAME = "MRI Viewer"

BACKGROUND_COLOR = "Gainsboro"
AXES_COLOR = (0.0, 0.0, 0.0)

COLD_TEMPERATURE_COLOR = (0.230, 0.299, 0.754)
LUKEWARM_TEMPERATURE_COLOR = (0.865, 0.865, 0.865)
HOT_TEMPERATURE_COLOR = (0.706, 0.016, 0.15)

class Zoom:
    In = "0"
    Out = "1"

ZOOM_FACTOR = 0.1

class Directions:
    XAxisPlus = "0"
    XAxisMinus = "1"
    YAxisPlus = "2"
    YAxisMinus = "3"
    ZAxisPlus = "4"
    ZAxisMinus = "5"

TRANSLATION_FACTOR = 10.0

class Languages:
    Czech = "CZ"
    English = "EN"
    
DEFAULT_LANGUAGE = Languages.English

class Representation:
    Points = 0
    Slice = 1
    Surface = 2
    SurfaceWithEdges = 3
    Wireframe = 4

DEFAULT_REPRESENTATION = Representation.Surface

class Planes:
    XY = 0
    XYNormal = (0.0, 0.0, 1.0)
    YZ = 1
    YZNormal = (1.0, 0.0, 0.0)
    XZ = 2
    XZNormal = (0.0, 1.0, 0.0)

DEFAULT_PLANE = Planes.XY
DEFAULT_PLANE_NORMAL = Planes.XYNormal

class PickerModes:
    Off = "0"
    Points = "1"
    Cells = "2"

DEFAULT_PICKER_MODE = PickerModes.Off
