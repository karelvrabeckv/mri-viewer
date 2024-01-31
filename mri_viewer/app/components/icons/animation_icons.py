from trame.widgets import vuetify3

def animation_icons(self):
    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), click=self.on_previous_file):
        vuetify3.VIcon("mdi-skip-previous")
    
    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), classes="mx-2", click=self.on_toggle_player):
        vuetify3.VIcon(v_if=("is_playing",), icon="mdi-pause")
        vuetify3.VIcon(v_else=("is_playing",), icon="mdi-play")

    with vuetify3.VBtn(icon=True, disabled=("ui_disabled", True), click=self.on_next_file):
        vuetify3.VIcon("mdi-skip-next")
