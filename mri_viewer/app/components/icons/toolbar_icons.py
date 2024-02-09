from trame.widgets import vuetify3

def toolbar_icons(self):
    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), classes="mx-2", click=self.on_axes_visibility):
        vuetify3.VIcon("mdi-axis")

    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), click=self.on_push_camera):
        vuetify3.VIcon("mdi-crop-free")

    with vuetify3.VBtn(icon=True, classes="mx-2", click=self.on_change_theme):
        vuetify3.VIcon("mdi-theme-light-dark")
