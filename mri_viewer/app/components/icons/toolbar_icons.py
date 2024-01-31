from trame.widgets import vuetify3

def toolbar_icons(self):
    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), click=self.on_axes_visibility):
        vuetify3.VIcon(v_if=("axes",), icon="mdi-cube-off-outline")
        vuetify3.VIcon(v_else=("axes",), icon="mdi-cube-outline")
                        
    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), classes="mx-2", click=self.on_push_camera):
        vuetify3.VIcon("mdi-crop-free")
