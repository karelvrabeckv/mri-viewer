APPLICATION_NAME = "MRI Viewer"
DEVELOPER_MODE = False

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
DEFAULT_TEXT_COLOR = (0.0, 0.0, 0.0)
DEFAULT_BACKGROUND_COLOR = "Gainsboro"

COLD_TEMPERATURE_COLOR = (0.230, 0.299, 0.754)
LUKEWARM_TEMPERATURE_COLOR = (0.865, 0.865, 0.865)
HOT_TEMPERATURE_COLOR = (0.706, 0.016, 0.15)

PICKED_CELL_OFFSET = 0.01

ID = "ID"

class Axis:
    X = "X"
    Y = "Y"
    Z = "Z"

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

class ZoomParams:
    Default = 3
    Min = 1
    Max = 10
    Step = 1

class TranslationParams:
    Default = 50
    Min = 10
    Max = 300
    Step = 10

class RotationParams:
    Default = 90
    Min = 10
    Max = 180
    Step = 10

class LoadingOptions:
    Default = "0"
    PC = "1"
    URL = "2"

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
    ScalarBarActor = "scalar_bar_actor"
    Slice = "slice"
    SliceMapper = "slice_mapper"
    SliceActor = "slice_actor"
    PickedPoint = "picked_point"
    PickedPointMapper = "picked_point_mapper"
    PickedPointActor = "picked_point_actor"
    PickedCell = "picked_cell"
    PickedCellMapper = "picked_cell_mapper"
    PickedCellActor = "picked_cell_actor"

class ErrorCodes:
    NoFilesToUpload = "NO-FILES-TO-UPLOAD"
    TooManyFilesToUpload = "TOO-MANY-FILES-TO-UPLOAD"
    EmptyFile = "EMPTY-FILE"
    WrongFileExtension = "WRONG-FILE-EXTENSION"
    FileIsTooLarge = "FILE-IS-TOO-LARGE"
    InvalidURL = "INVALID-URL"
    MissingHeaders = "MISSING-HEADERS"
    MissingContentDispositionHeader = "MISSING-CONTENT-DISPOSITION-HEADER"
    MissingContentLengthHeader = "MISSING-CONTENT-LENGTH-HEADER"
    MissingContent = "MISSING-CONTENT"
    MissingImageData = "MISSING-IMAGE-DATA"
    MissingPointAndCellData = "MISSING-POINT-AND-CELL-DATA"
