from trame.widgets import vuetify3

from mri_viewer.app.components import button, toggle_button

def animation_icons(self):
    def on_previous_file():
        self.state.player_on = False
        self.toggle_picker_modes_ui()
        
        _, file_index, group, _ = self.current_file_info
        
        previous_file_index = file_index - 1
        if previous_file_index < 0:
            previous_file_index = group.get_num_of_files() - 1
        
        group_file_names = group.get_all_file_names() 
        self.state.current_file_name = group_file_names[previous_file_index]

    def on_toggle_player():
        self.state.player_on = not self.state.player_on
        self.toggle_picker_modes_ui()

    def on_next_file():
        self.state.player_on = False
        self.toggle_picker_modes_ui()
        
        _, file_index, group, _ = self.current_file_info
        
        next_file_index = file_index + 1
        if next_file_index >= group.get_num_of_files():
            next_file_index = 0
        
        group_file_names = group.get_all_file_names() 
        self.state.current_file_name = group_file_names[next_file_index]

    vuetify3.VSpacer()

    button(
        icon="mdi-skip-previous",
        disabled=("ui_player_off",),
        border=False,
        tooltip=("language.previous_file_tooltip",),
        click=on_previous_file,
    )

    toggle_button(
        condition=("player_on",),
        if_icon="mdi-pause",
        else_icon="mdi-play",
        disabled=("ui_player_off",),
        border=False,
        tooltip=("language.player_tooltip",),
        classes="mx-2",
        click=on_toggle_player,
    )

    button(
        icon="mdi-skip-next",
        disabled=("ui_player_off",),
        border=False,
        tooltip=("language.next_file_tooltip",),
        click=on_next_file,
    )

    vuetify3.VSpacer()
