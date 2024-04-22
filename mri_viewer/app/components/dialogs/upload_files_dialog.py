from trame.decorators import hot_reload
from trame.widgets import html, vuetify3

from mri_viewer.app.components.buttons import open_upload_files_dialog_button
from mri_viewer.app.constants import UploadFilesOptions, Theme

@hot_reload
def upload_files_dialog(ctrl):
    """Dialog for uploading files."""

    with vuetify3.VDialog(v_model=("upload_files_dialog_on",), width=450):
        # Button
        with vuetify3.Template(v_slot_activator="{ props }"):
            open_upload_files_dialog_button()
        
        # Dialog
        with vuetify3.Template(v_slot_default="{ props }"):
            with vuetify3.VCard(title=("language.upload_files_title",), loading=("trame__busy",)):
                vuetify3.VDivider()

                with vuetify3.VCardText(classes="py-2"):
                    with vuetify3.VContainer(classes="pa-0"):
                        with vuetify3.VRow(classes="my-3 mx-0"):
                            html.Span("{{ language.upload_files_text }}", classes="text-caption")

                        vuetify3.VDivider(classes="my-5")

                        with vuetify3.VRow(
                            v_show=f"upload_files_option == {UploadFilesOptions.Default}",
                            justify="center",
                            classes="my-3 mx-0"
                        ):
                            with vuetify3.VBtnGroup(classes="my-1 px-1"):
                                vuetify3.VBtn(
                                    prepend_icon="mdi-monitor",
                                    text=("language.upload_files_from_pc",),
                                    color=Theme.IKEMColor,
                                    click=f"upload_files_option = {UploadFilesOptions.PC}",
                                )
                            with vuetify3.VBtnGroup(classes="my-1 px-1"):
                                vuetify3.VBtn(
                                    prepend_icon="mdi-server",
                                    text=("language.upload_file_from_url",),
                                    color=Theme.IKEMColor,
                                    click=f"upload_files_option = {UploadFilesOptions.URL}",
                                )
                        
                        with vuetify3.VRow(v_show=f"upload_files_option == {UploadFilesOptions.PC}", classes="my-3 mx-0"):
                            vuetify3.VFileInput(
                                variant="outlined",
                                prepend_icon="mdi-monitor",
                                label=("language.upload_files_from_pc",),
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
                                mouseup=ctrl.clear_files_from_pc_error_message,
                            )    
                        
                        with vuetify3.VRow(v_show=f"upload_files_option == {UploadFilesOptions.URL}", classes="my-3 mx-0"):
                            with vuetify3.VCol(cols="9", classes="pa-0 pr-2"):
                                vuetify3.VTextField(
                                    variant="outlined",
                                    prepend_icon="mdi-server",
                                    label=("language.upload_file_from_url",),
                                    v_model=("file_from_url", None),
                                    density="comfortable",
                                    placeholder="https://...",
                                    hide_details="auto",
                                    error_messages=("file_from_url_error_message", None),
                                )
                            
                            with vuetify3.VCol(cols="3", classes="pa-0"):
                                with vuetify3.VBtnGroup():
                                    vuetify3.VBtn(
                                        text=("language.upload_files_button_title",),
                                        color=Theme.IKEMColor,
                                        click=ctrl.on_file_from_url_upload,
                                    )
                        
                vuetify3.VDivider()
                
                with vuetify3.VCardActions(classes="py-2"):
                    vuetify3.VSpacer()
                    
                    with vuetify3.VBtnGroup(v_show=f"upload_files_option != {UploadFilesOptions.Default}", classes="mr-2", border=True):
                        vuetify3.VBtn(
                            text=("language.back_button_title",),
                            click=f"upload_files_option = {UploadFilesOptions.Default}",
                        )

                    with vuetify3.VBtnGroup(v_bind="props", border=True):
                        vuetify3.VBtn(
                            text=("language.cancel_button_title",),
                            click=ctrl.close_upload_files_dialog,
                        )
