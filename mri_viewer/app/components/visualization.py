from trame.decorators import hot_reload
from trame.widgets import vtk, vuetify3

@hot_reload
def visualization(ctrl, pipeline):
    """A view for visualizing the data."""

    with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
        view = vtk.VtkLocalView(
            pipeline.render_window,
            widgets=[pipeline.axes_widget],
            interactor_events=("events", ["LeftButtonPress", "EndAnimation"]),
            LeftButtonPress=(ctrl.on_picker, "[utils.vtk.event($event)]"),
            EndAnimation=(ctrl.on_interaction, "[$event.pokedRenderer.getActiveCamera().get()]")
        )
        ctrl.update = view.update
        ctrl.push_camera = view.push_camera
