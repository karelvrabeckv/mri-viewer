from trame.widgets import vuetify3

import mri_viewer.app.constants as const

def load_files_dialog(self):
    def close_dialog():
        self.state.dialog_on = False

    with vuetify3.VDialog(v_model=("dialog_on",), width=500):
        # Button
        with vuetify3.Template(v_slot_activator="{ props }"):
            vuetify3.VDivider(vertical=True)
            
            with vuetify3.VBtnGroup(v_bind="props", border=True, classes="mx-2"):
                vuetify3.VBtn(text=("language.load_files_title",))
            
            vuetify3.VDivider(vertical=True)
        
        # Dialog
        with vuetify3.Template(v_slot_default="{ props }"):
            with vuetify3.VCard(title=("language.load_files_title",)):
                vuetify3.VDivider()
                
                with vuetify3.VCardText(classes="py-2"):
                    with vuetify3.VRow(classes="my-4 mx-0"):
                        vuetify3.VFileInput(
                            variant="outlined",
                            label=("language.load_files_from_pc",),
                            v_model=("uploaded_files", None),
                            hint=("language.supported_file_formats",),
                            persistent_hint=True,
                            clearable=False,
                            multiple=True,
                            chips=True,
                            show_size=True,
                            accept=".vti",
                            __properties=["accept"],
                        )
                    
                    vuetify3.VDivider(classes="my-6")
                    
                    with vuetify3.VRow(classes="d-flex align-center my-4 mx-0"):
                        vuetify3.VTextField(
                            variant="outlined",
                            label=("language.load_file_from_url",),
                            hide_details=True,
                        )
                        
                        vuetify3.VBtn(
                            variant="tonal",
                            text=("language.load_file_button_title",),
                            border=True,
                            classes="ml-4",
                            click=close_dialog,
                        )
                        
                vuetify3.VDivider()
                
                with vuetify3.VCardActions(classes="py-2"):
                    vuetify3.VSpacer()
                    
                    with vuetify3.VBtnGroup(v_bind="props", border=True):
                        vuetify3.VBtn(
                            text=("language.cancel_button_title",),
                            color=const.IKEM_COLOR,
                            click=close_dialog,
                        )
