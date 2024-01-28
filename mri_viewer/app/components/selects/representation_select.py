from trame.widgets import vuetify3

from ...constants import Representation

def representation_select():
    vuetify3.VSelect(
        v_model=("current_representation", None),
        label="Representation",
        items=(
            [
                {"title": "Points", "value": Representation.Points},
                {"title": "Slice", "value": Representation.Slice},
                {"title": "Surface", "value": Representation.Surface},
                {"title": "Surface With Edges", "value": Representation.SurfaceWithEdges},
                {"title": "Wireframe", "value": Representation.Wireframe},
            ],
        ),
        disabled=("ui_disabled", True),
        variant="outlined",
        hide_details=True,
        classes="ma-4",
    )
