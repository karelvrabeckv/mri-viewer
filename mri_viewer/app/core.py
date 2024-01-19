from trame.app import get_server
from trame.decorators import TrameApp, change, controller, life_cycle
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vuetify3, vtk

from .constants import (
    APPLICATION_NAME,
    Representation,
    DEFAULT_REPRESENTATION,
)
from .pipeline import VTIPipeline

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------

@TrameApp()
class MRIViewerApp:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.state.trame__title = APPLICATION_NAME
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
        self.pipeline.set_representation(representation)
        self.ctrl.view_update()

    @change("data_array")
    def on_data_array_change(self, data_array, **kwargs):
        self.pipeline.set_data_array(data_array)
        self.ctrl.view_update()

    @life_cycle.server_reload
    def _build_ui(self, **kwargs):
        with SinglePageWithDrawerLayout(self.server) as layout:
            # Toolbar
            layout.title.set_text(APPLICATION_NAME)
            with layout.toolbar:
                pass

            # Sidebar
            with layout.drawer:
                # Data arrays
                vuetify3.VSelect(
                    v_model=("data_array", self.pipeline.activeArray),
                    label="Data Array",
                    items=(
                        [
                            {"title": x, "value": x} for x in self.pipeline.dataArrays
                        ],
                    ),
                    variant="outlined",
                    density="compact",
                    hide_details=True,
                    classes="ma-4",
                )
                                
                vuetify3.VDivider()
                
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

            # Content
            with layout.content:
                with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    view = vtk.VtkLocalView(self.pipeline.renderWindow)
                    self.ctrl.view_update = view.update

            return layout
