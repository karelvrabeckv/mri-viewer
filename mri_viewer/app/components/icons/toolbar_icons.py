from mri_viewer.app.components import button

import mri_viewer.app.constants as const

def toolbar_icons(self):
    def on_toggle_axes():
        self.state.axes_on = not self.state.axes_on
        self.pipeline.render_axes(self.state.axes_on)
        
        _, _, group, _ = self.current_file_information
        self.update_client_camera(group)

    def on_reset_camera():
        _, _, group, _ = self.current_file_information
        group.current_view = group.default_view

        self.pipeline.set_camera_to_group_default_view(group)
        self.ctrl.push_camera()

    def on_change_theme():
        if self.state.theme == const.Theme.Light:
            self.state.theme = const.Theme.Dark
        else:
            self.state.theme = const.Theme.Light
    
    button(
        disabled=("ui_off",),
        icon="mdi-axis-arrow",
        border=False,
        tooltip=("language.toggle_axes_tooltip",),
        classes="mx-2",
        click=on_toggle_axes,
    )

    button(
        disabled=("ui_off",),
        icon="mdi-cube-scan",
        border=False,
        tooltip=("language.reset_camera_tooltip",),
        click=on_reset_camera,
    )
    
    button(
        icon="mdi-theme-light-dark",
        border=False,
        tooltip=("language.change_theme_tooltip",),
        classes="mx-2",
        click=on_change_theme,
    )
