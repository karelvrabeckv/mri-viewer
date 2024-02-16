from trame.widgets import html, vuetify3

from mri_viewer.app.components import button

import mri_viewer.app.constants as const

def zoom_interaction(self):
    def zoom(direction):
        camera = self._pipeline.renderer.GetActiveCamera()
        
        if direction == const.Zoom.In:
            for _ in range(self.state.current_zoom_factor):
                camera.Zoom(1 + 0.1)
        elif direction == const.Zoom.Out:
            for _ in range(self.state.current_zoom_factor):
                camera.Zoom(1 - 0.1)
        
        self._pipeline.renderer.SetActiveCamera(camera)
        self._pipeline.render_window.Render()
        self.ctrl.push_camera()

        _, _, group, _ = self.current_file_information
        group.current_view = self._pipeline.get_camera_params()

    with vuetify3.VCard(disabled=("ui_off",), border=True, classes="ma-4"):
        with vuetify3.VCardTitle(
            "{{ language.section_zoom_title }}",
            classes="d-flex justify-space-between bg-grey-darken-2 py-2"
        ):
            button(
                icon="mdi-information-variant",
                size="x-small",
                tooltip=("language.section_zoom_tooltip",),
                tooltip_location="right",
            )
        
        with vuetify3.VCardText():
            with vuetify3.VRow(justify="center", classes="my-4"):
                button(
                    icon="mdi-plus",
                    tooltip=("language.zoom_in_tooltip",),
                    classes="mx-1",
                    click=(zoom, f"['{const.Zoom.In}']"),
                )
                button(
                    icon="mdi-minus",
                    tooltip=("language.zoom_out_tooltip",),
                    classes="mx-1",
                    click=(zoom, f"['{const.Zoom.Out}']"),
                )

            with vuetify3.VRow(justify="center", classes="px-2 pb-4"):
                vuetify3.VSlider(
                    label=("language.zoom_factor_slider_title",),
                    v_model="current_zoom_factor",
                    show_ticks="always",
                    min=const.MIN_ZOOM_FACTOR,
                    max=const.MAX_ZOOM_FACTOR,
                    step=const.ZOOM_STEP,
                    hide_details=True,
                )
                html.Span("{{ current_zoom_factor }}x", classes="d-flex align-center text-caption mx-2")
