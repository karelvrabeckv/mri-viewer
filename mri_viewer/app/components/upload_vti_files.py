from trame.widgets import vuetify3

def upload_vti_files():
    vuetify3.VFileInput(
        label=("language.upload_vti_files_title",),
        v_model=("current_vti_files", None),
        multiple=True,
        accept=".vti",
        __properties=["accept"],
        variant="outlined",
        hide_details=True,
        classes="ma-4",
    )
    vuetify3.VDivider()
