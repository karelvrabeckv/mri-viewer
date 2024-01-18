from trame.app import get_server
from trame.decorators import TrameApp, change, controller, life_cycle
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vuetify3, vtk

from .callbacks import set_representation
from .constants import Representation, DEFAULT_REPRESENTATION
from .pipelines import VTIPipeline

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------

@TrameApp()
class MRIViewerApp:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.pipeline = VTIPipeline(DEFAULT_REPRESENTATION)
        self.ui = self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    # @controller.set("reset_resolution")
    # def reset_resolution(self):
    #     self.state.resolution = 6

    @change("representation")
    def on_representation_change(self, representation, **kwargs):
        set_representation(self.pipeline.actor, representation)
        self.ctrl.view_update()

    @life_cycle.server_reload
    def _build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self.server) as layout:
            # Toolbar
            layout.title.set_text("MRI Viewer")
            with layout.toolbar:
                pass

            # Sidebar
            with layout.drawer:
                # Representation
                vuetify3.VSelect(
                    v_model=("representation", DEFAULT_REPRESENTATION),
                    label="Representation",
                    items=(
                        [
                            {"title": "Points", "value": Representation.Points},
                            {"title": "Surface", "value": Representation.Surface},
                            {"title": "Surface With Edges", "value": Representation.SurfaceWithEdges},
                            {"title": "Wireframe", "value": Representation.Wireframe},
                        ],
                    ),
                    variant="outlined",
                    density="compact",
                    hide_details=True,
                    classes="ma-4",
                )
                vuetify3.VDivider()

            # Content
            with layout.content:
                with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    view = vtk.VtkLocalView(self.pipeline.renderWindow)
                    self.ctrl.view_update = view.update

            return layout
