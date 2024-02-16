APPLICATION_NAME = "MRI Viewer"

class Theme:
    Light = "light"
    Dark = "dark"

DEFAULT_THEME = Theme.Light

VUETIFY_CONFIG = {
    "theme": {
        "themes": {
            Theme.Light: {
                "dark": False,
            },
            Theme.Dark: {
                "dark": True,
            }
        }
    }
}

IKEM_COLOR = "#e2001a"
AXES_COLOR = (0.0, 0.0, 0.0)
BACKGROUND_COLOR = "Gainsboro"

COLD_TEMPERATURE_COLOR = (0.230, 0.299, 0.754)
LUKEWARM_TEMPERATURE_COLOR = (0.865, 0.865, 0.865)
HOT_TEMPERATURE_COLOR = (0.706, 0.016, 0.15)

class Zoom:
    In = "0"
    Out = "1"

class Directions:
    XAxisPlus = "0"
    XAxisMinus = "1"
    YAxisPlus = "2"
    YAxisMinus = "3"
    ZAxisPlus = "4"
    ZAxisMinus = "5"

ZOOM_STEP = 1
DEFAULT_ZOOM_FACTOR = 1
MIN_ZOOM_FACTOR = 1
MAX_ZOOM_FACTOR = 9

TRANSLATION_STEP = 10
DEFAULT_TRANSLATION_FACTOR = 10
MIN_TRANSLATION_FACTOR = 10
MAX_TRANSLATION_FACTOR = 90

ROTATION_STEP = 10
DEFAULT_ROTATION_FACTOR = 30
MIN_ROTATION_FACTOR = 10
MAX_ROTATION_FACTOR = 350

class Languages:
    Czech = "CZ"
    English = "EN"
    
DEFAULT_LANGUAGE = Languages.English

class Representation:
    Points = "0"
    Slice = "1"
    Surface = "2"
    SurfaceWithEdges = "3"
    Wireframe = "4"

DEFAULT_REPRESENTATION = Representation.Surface

class Planes:
    XY = "0"
    YZ = "1"
    XZ = "2"

DEFAULT_SLICE_POSITION = 0
DEFAULT_SLICE_ORIENTATION = Planes.XY

class PickerModes:
    Off = "0"
    Points = "1"
    Cells = "2"

DEFAULT_PICKER_MODE = PickerModes.Off

class CameraParams:
    Position = "position"
    FocalPoint = "focal_point"
    ViewUp = "view_up"
    ViewAngle = "view_angle"
