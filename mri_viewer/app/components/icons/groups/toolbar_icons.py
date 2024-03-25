from trame.decorators import hot_reload

from mri_viewer.app.components.icons import icon

@hot_reload
def toolbar_icons(ctrl):
    """Icons for the rest of the toolbar tools."""

    icon(
        key="mdi-axis-arrow-info",
        disabled=("ui_off",),
        border=False,
        tooltip=("language.toggle_axes_info_tooltip",),
        tooltip_location="bottom",
        classes="mx-2",
        click=ctrl.on_toggle_axes_info,
    )

    icon(
        key="mdi-cube-scan",
        disabled=("ui_off",),
        border=False,
        tooltip=("language.reset_camera_tooltip",),
        tooltip_location="bottom",
        click=ctrl.on_reset_camera,
    )
    
    icon(
        key="mdi-theme-light-dark",
        border=False,
        tooltip=("language.change_theme_tooltip",),
        tooltip_location="bottom",
        classes="mx-2",
        click=ctrl.on_change_theme,
    )
