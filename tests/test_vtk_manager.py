from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor, vtkScalarBarActor
from vtkmodules.vtkRenderingCore import vtkActor, vtkColorTransferFunction

from mri_viewer.app.vtk import VTKCreator, VTKManager

import mri_viewer.app.constants as const

# ========================================

def set_color_map_cool_to_warm(vtk_creator: VTKCreator, color_transfer_function: vtkColorTransferFunction):
    vtk_creator.set_color_map_cool_to_warm(color_transfer_function)

def test_set_color_map_cool_to_warm_0():
    vtk_creator = VTKCreator()
    color_transfer_function = vtkColorTransferFunction()

    set_color_map_cool_to_warm(vtk_creator, color_transfer_function)
    
    start_point = (
        round(color_transfer_function.GetRedValue(0.0), 3),
        round(color_transfer_function.GetGreenValue(0.0), 3),
        round(color_transfer_function.GetBlueValue(0.0), 3),
    )
    
    middle_point = (
        round(color_transfer_function.GetRedValue(0.5), 3),
        round(color_transfer_function.GetGreenValue(0.5), 3),
        round(color_transfer_function.GetBlueValue(0.5), 3),
    )
    
    end_point = (
        round(color_transfer_function.GetRedValue(1.0), 3),
        round(color_transfer_function.GetGreenValue(1.0), 3),
        round(color_transfer_function.GetBlueValue(1.0), 3),
    )

    assert(start_point == const.COOL_TO_WARM_COLOR_MAP[0.0])
    assert(middle_point == const.COOL_TO_WARM_COLOR_MAP[0.5])
    assert(end_point == const.COOL_TO_WARM_COLOR_MAP[1.0])

# ========================================

def set_color_map_grayscale(vtk_creator: VTKCreator, color_transfer_function: vtkColorTransferFunction):
    vtk_creator.set_color_map_grayscale(color_transfer_function)

def test_set_color_map_grayscale_0():
    vtk_creator = VTKCreator()
    color_transfer_function = vtkColorTransferFunction()

    set_color_map_grayscale(vtk_creator, color_transfer_function)
    
    start_point = (
        round(color_transfer_function.GetRedValue(0.0), 3),
        round(color_transfer_function.GetGreenValue(0.0), 3),
        round(color_transfer_function.GetBlueValue(0.0), 3),
    )
    
    end_point = (
        round(color_transfer_function.GetRedValue(1.0), 3),
        round(color_transfer_function.GetGreenValue(1.0), 3),
        round(color_transfer_function.GetBlueValue(1.0), 3),
    )

    assert(start_point == const.GRAYSCALE_COLOR_MAP[0.0])
    assert(end_point == const.GRAYSCALE_COLOR_MAP[1.0])

# ========================================

def set_cube_axes_actor_colors(vtk_creator: VTKCreator, cube_axes_actor: vtkCubeAxesActor, color):
    vtk_creator.set_cube_axes_actor_colors(cube_axes_actor, color)

def test_set_cube_axes_actor_colors_0():
    vtk_creator = VTKCreator()
    cube_axes_actor = vtkCubeAxesActor()

    set_cube_axes_actor_colors(vtk_creator, cube_axes_actor, const.Theme.WhiteColor)

    assert(cube_axes_actor.GetXAxesLinesProperty().GetColor() == const.Theme.WhiteColor)
    assert(cube_axes_actor.GetYAxesLinesProperty().GetColor() == const.Theme.WhiteColor)
    assert(cube_axes_actor.GetZAxesLinesProperty().GetColor() == const.Theme.WhiteColor)

    for i in range(3):
        assert(cube_axes_actor.GetTitleTextProperty(i).GetColor() == const.Theme.WhiteColor)
        assert(cube_axes_actor.GetLabelTextProperty(i).GetColor() == const.Theme.WhiteColor)

# ========================================

def set_scalar_bar_actor_colors(vtk_creator: VTKCreator, scalar_bar: vtkScalarBarActor, color):
    vtk_creator.set_scalar_bar_actor_colors(scalar_bar, color)

def test_set_scalar_bar_actor_colors_0():
    vtk_creator = VTKCreator()
    scalar_bar = vtkScalarBarActor()

    set_scalar_bar_actor_colors(vtk_creator, scalar_bar, const.Theme.WhiteColor)

    assert(scalar_bar.GetTitleTextProperty().GetColor() == const.Theme.WhiteColor)
    assert(scalar_bar.GetLabelTextProperty().GetColor() == const.Theme.WhiteColor)

# ========================================

def set_visibility(vtk_manager, visibility, actor):
    vtk_manager.set_visibility(visibility, actor)

def test_set_visibility_0():
    vtk_manager = VTKManager()
    actor = vtkActor()

    set_visibility(vtk_manager, False, actor)

    assert(actor.GetVisibility() == False)

# ========================================

def add_actors(vtk_manager, actor):
    vtk_manager.add_actors(actor)

def test_add_actors_0():
    vtk_manager = VTKManager()
    actor = vtkActor()

    add_actors(vtk_manager, actor)

    render_window = vtk_manager.render_window
    renderer = render_window.GetRenderers().GetFirstRenderer()

    assert(renderer.GetActors().GetLastActor() == actor)

# ========================================

def add_2d_actors(vtk_manager, actor):
    vtk_manager.add_2d_actors(actor)

def test_add_2d_actors_0():
    vtk_manager = VTKManager()
    actor = vtkScalarBarActor()

    add_2d_actors(vtk_manager, actor)

    render_window = vtk_manager.render_window
    renderer = render_window.GetRenderers().GetFirstRenderer()

    assert(renderer.GetActors2D().GetLastActor2D() == actor)

# ========================================

def resize_window(vtk_manager, content_size):
    vtk_manager.resize_window(content_size)

def test_resize_window_0():
    vtk_manager = VTKManager()
    content_size = { "size": { "width": 500, "height": 400 }, "pixelRatio": 1.25 }

    resize_window(vtk_manager, content_size)

    render_window = vtk_manager.render_window

    assert(render_window.GetSize() == (625, 500))

# ========================================

def get_theme_color(vtk_manager, theme):
    return vtk_manager.get_theme_color(theme)

def test_get_theme_color_0():
    vtk_manager = VTKManager()

    assert(get_theme_color(vtk_manager, const.Theme.Light) == const.Theme.BlackColor)
    assert(get_theme_color(vtk_manager, const.Theme.Dark) == const.Theme.WhiteColor)

# ========================================

def get_theme_background(vtk_manager, theme):
    return vtk_manager.get_theme_background(theme)

def test_get_theme_background_0():
    vtk_manager = VTKManager()

    assert(get_theme_background(vtk_manager, const.Theme.Light) == const.Theme.LightBackground)
    assert(get_theme_background(vtk_manager, const.Theme.Dark) == const.Theme.DarkBackground)
