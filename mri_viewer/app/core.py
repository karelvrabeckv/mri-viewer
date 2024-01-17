
from trame.app import get_server
from trame.decorators import TrameApp, change, controller, life_cycle
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3, vtk


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------

@TrameApp()
class MyTrameApp:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.ui = self._build_ui()

        # Set state variable
        self.state.trame__title = "MRI Viewer"
        self.state.resolution = 6

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @controller.set("reset_resolution")
    def reset_resolution(self):
        self.state.resolution = 6

    @change("resolution")
    def on_resolution_change(self, resolution, **kwargs):
        print(f">>> ENGINE(a): Slider updating resolution to {resolution}")

    @life_cycle.server_reload
    def _build_ui(self, **kwargs):
        with SinglePageLayout(self.server) as layout:
            # Toolbar
            layout.title.set_text("Trame / vtk.js")
            with layout.toolbar:
                vuetify3.VSpacer()
                vuetify3.VSlider(                    # Add slider
                    v_model=("resolution", 6),      # bind variable with an initial value of 6
                    min=3, max=60,                  # slider range
                    dense=True, hide_details=True,  # presentation setup
                )
                with vuetify3.VBtn(icon=True, click=self.ctrl.reset_camera):
                    vuetify3.VIcon("mdi-crop-free")
                with vuetify3.VBtn(icon=True, click=self.reset_resolution):
                    vuetify3.VIcon("mdi-undo")

            # Main content
            with layout.content:
                with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    with vtk.VtkView() as vtk_view:                # vtk.js view for local rendering
                        self.ctrl.reset_camera = vtk_view.reset_camera  # Bind method to controller
                        with vtk.VtkGeometryRepresentation():      # Add representation to vtk.js view
                            vtk.VtkAlgorithm(                      # Add ConeSource to representation
                                vtk_class="vtkConeSource",          # Set attribute value with no JS eval
                                state=("{ resolution }",)          # Set attribute value with JS eval
                            )

            # Footer
            # layout.footer.hide()

            return layout
