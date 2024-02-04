from trame.widgets import vuetify3

def toolbar_icons(self):
    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), click=self.on_axes_visibility):
        vuetify3.VIcon(v_if=("axes",), icon="mdi-axis", color="rgba(0, 0, 0, 1.0)")
        vuetify3.VIcon(v_else=("axes",), icon="mdi-axis", color="rgba(0, 0, 0, 0.25)")

    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), classes="mx-2", click=self.on_push_camera):
        vuetify3.VIcon("mdi-crop-free")
