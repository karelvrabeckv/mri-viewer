from trame.widgets import html, vuetify3

from mri_viewer.app.components.buttons import button

import mri_viewer.app.constants as const
import mri_viewer.app.styles as style

def zoom_interaction(self):
    def zoom(direction):
        camera = self.pipeline.camera
        
        if direction == const.Zoom.In:
            for _ in range(self.state.current_zoom_factor):
                camera.Zoom(1 + 0.1)
        elif direction == const.Zoom.Out:
            for _ in range(self.state.current_zoom_factor):
                camera.Zoom(1 - 0.1)
        
        self.pipeline.camera = camera
        self.pipeline.render()
        self.ctrl.push_camera()

        _, _, group, _ = self.current_file_info
        group.current_view = self.pipeline.get_camera_params()

    with vuetify3.VCard(border=True, classes="ma-4"):
        with vuetify3.VCardTitle(
            "{{ language.section_zoom_title }}",
            style=style.HEADER,
            classes="d-flex justify-space-between text-uppercase text-button font-weight-bold py-2"
        ):
            button(
                icon="mdi-information-variant",
                disabled=("ui_off",),
                size="x-small",
                tooltip=("language.section_zoom_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                button(
                    icon="mdi-minus",
                    disabled=("ui_off",),
                    tooltip=("language.zoom_out_tooltip",),
                    classes="mx-1",
                    click=(zoom, f"['{const.Zoom.Out}']"),
                )
                button(
                    icon="mdi-plus",
                    disabled=("ui_off",),
                    tooltip=("language.zoom_in_tooltip",),
                    classes="mx-1",
                    click=(zoom, f"['{const.Zoom.In}']"),
                )

            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                html.Span("{{ language.factor_slider_title }}", classes="d-flex align-center ml-2 mr-4")
                vuetify3.VSlider(
                    disabled=("ui_off",),
                    v_model="current_zoom_factor",
                    show_ticks="always",
                    min=const.MIN_ZOOM_FACTOR,
                    max=const.MAX_ZOOM_FACTOR,
                    step=const.ZOOM_STEP,
                    hide_details=True,
                )
                html.Span("{{ current_zoom_factor }}x", classes="d-flex align-center ml-4 mr-2")
