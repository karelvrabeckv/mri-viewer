from trame.decorators import hot_reload

from mri_viewer.app.components.icons import icon, toggle_icon

@hot_reload
def player_icons(ctrl):
    """Icons for controlling the player."""

    icon(
        key="mdi-skip-previous",
        disabled=("ui_player_off",),
        border=False,
        tooltip=("language.previous_file_tooltip",),
        tooltip_location="bottom",
        click=ctrl.on_previous_file,
    )

    toggle_icon(
        condition=("player_on",),
        if_key="mdi-pause",
        else_key="mdi-play",
        disabled=("ui_player_off",),
        border=False,
        tooltip=("language.player_tooltip",),
        tooltip_location="bottom",
        classes="mx-2",
        click=ctrl.on_toggle_player,
    )

    icon(
        key="mdi-skip-next",
        disabled=("ui_player_off",),
        border=False,
        tooltip=("language.next_file_tooltip",),
        tooltip_location="bottom",
        click=ctrl.on_next_file,
    )
