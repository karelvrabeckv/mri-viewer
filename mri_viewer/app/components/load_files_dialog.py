from trame.widgets import html, vuetify3

import mri_viewer.app.constants as const

def load_files_dialog(self):
    def close_dialog():
        self.state.dialog_on = False

    with vuetify3.VDialog(v_model=("dialog_on",), width=500):
        # Button
        with vuetify3.Template(v_slot_activator="{ props }"):
            vuetify3.VDivider(vertical=True)
            
            with vuetify3.VBtnGroup(v_bind="props", classes="mx-2"):
                vuetify3.VBtn(text=("language.load_files_title",), color=const.IKEM_COLOR)
            
            vuetify3.VDivider(vertical=True)
        
        # Dialog
        with vuetify3.Template(v_slot_default="{ props }"):
            with vuetify3.VCard(title=("language.load_files_title",)):
                vuetify3.VDivider()
                
                with vuetify3.VCardText(classes="py-2"):
                    with vuetify3.VRow(classes="my-4 mx-0"):
                        html.Span("{{ language.load_files_text }}", classes="text-caption")

                    vuetify3.VDivider(classes="my-6")

                    with vuetify3.VRow(classes="my-4 mx-0"):
                        vuetify3.VFileInput(
                            variant="outlined",
                            prepend_icon="mdi-monitor",
                            label=("language.load_files_from_pc",),
                            v_model=("files_from_pc", None),
                            density="comfortable",
                            clearable=False,
                            multiple=True,
                            chips=True,
                            show_size=True,
                            accept=".vti",
                            __properties=["accept"],
                            hide_details="auto",
                            error_messages=("files_from_pc_error_message", None),
                            mouseup=self.clear_files_from_pc_error_message,
                        )
                        
                    vuetify3.VDivider(classes="my-6")
                    
                    with vuetify3.VRow(classes="my-4 mx-0"):
                        with vuetify3.VCol(cols="10", classes="pa-0 pr-2"):
                            vuetify3.VTextField(
                                variant="outlined",
                                prepend_icon="mdi-server",
                                label=("language.load_file_from_url",),
                                v_model=("file_from_url", None),
                                density="comfortable",
                                placeholder="https://...",
                                hide_details="auto",
                                error_messages=("file_from_url_error_message", None),
                            )
                        
                        with vuetify3.VCol(cols="2", classes="pa-0"):
                            with vuetify3.VBtnGroup():
                                vuetify3.VBtn(
                                    text=("language.load_file_button_title",),
                                    color=const.IKEM_COLOR,
                                    click=self.on_file_from_url_load,
                                )
                        
                vuetify3.VDivider()
                
                with vuetify3.VCardActions(classes="py-2"):
                    vuetify3.VSpacer()
                    
                    with vuetify3.VBtnGroup(v_bind="props", border=True):
                        vuetify3.VBtn(text=("language.cancel_button_title",), click=close_dialog)
