APPLICATION_NAME = "MRI Viewer"
DEBUG_MODE = False

CZ_USER_GUIDE_URL = "docs/user_guide_cz.pdf"
EN_USER_GUIDE_URL = "docs/user_guide_en.pdf"

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
MAX_ZOOM_FACTOR = 10

TRANSLATION_STEP = 10
DEFAULT_TRANSLATION_FACTOR = 10
MIN_TRANSLATION_FACTOR = 10
MAX_TRANSLATION_FACTOR = 300

ROTATION_STEP = 10
DEFAULT_ROTATION_FACTOR = 90
MIN_ROTATION_FACTOR = 10
MAX_ROTATION_FACTOR = 180

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

class Objects:
    ColorTransferFunction = "color_transfer_function"
    LookupTable = "lookup_table"
    FileMapper = "file_mapper"
    FileActor = "file_actor"
    CubeAxesActor = "cube_axes_actor"
    Slice = "slice"
    SliceMapper = "slice_mapper"
    SliceActor = "slice_actor"
    PickedPoint = "picked_point"
    PickedPointMapper = "picked_point_mapper"
    PickedPointActor = "picked_point_actor"
    PickedCell = "picked_cell"
    PickedCellMapper = "picked_cell_mapper"
    PickedCellActor = "picked_cell_actor"
