from trame.widgets import vuetify3

def upload_vti_files():
    vuetify3.VFileInput(
        v_model=("current_vti_files", None),
        label="Upload VTI Files",
        multiple=True,
        accept=".vti",
        __properties=["accept"],
        variant="outlined",
        hide_details=True,
        classes="ma-4",
    )
