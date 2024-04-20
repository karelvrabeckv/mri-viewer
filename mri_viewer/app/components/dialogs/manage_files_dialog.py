from trame.decorators import hot_reload
from trame.widgets import html, vuetify3

from mri_viewer.app.components.buttons import open_manage_files_dialog_button
from mri_viewer.app.constants import ManageFilesOptions, Theme

@hot_reload
def manage_files_dialog(ctrl):
    """A dialog for managing files."""

    with vuetify3.VDialog(v_model=("manage_files_dialog_on",), width=450):
        # Button
        with vuetify3.Template(v_slot_activator="{ props }"):
            open_manage_files_dialog_button()
        
        # Dialog
        with vuetify3.Template(v_slot_default="{ props }"):
            # Default
            with vuetify3.VCard(
                v_show=f"manage_files_option == {ManageFilesOptions.Default}",
                title=("language.manage_files_title",)
            ):
                vuetify3.VDivider()

                with vuetify3.VCardText(classes="py-2"):
                    with vuetify3.VContainer(classes="pa-0"):
                        with vuetify3.VRow(v_show="current_file_name_items.length === 0", classes="my-3 mx-0"):
                            html.Span("{{ language.no_uploaded_files_text }}", classes="text-caption")

                        with vuetify3.VContainer(v_show="current_file_name_items.length !== 0", classes="my-3 mx-0"):
                            with vuetify3.VRow(
                                v_for="(file_name, i) in current_file_name_items",
                                key="i",
                                align="center",
                                justify="space-between",
                            ):
                                html.Span("<b>{{ file_name }}</b>", classes="text-caption")
                                with vuetify3.VBtnGroup(classes="my-1", border=True):
                                    vuetify3.VBtn(
                                        v_show="current_file_name != file_name",
                                        prepend_icon="mdi-delete",
                                        text=("language.delete_button_title",),
                                        click=(ctrl.prepare_to_delete_file, "[file_name]"),
                                    )
                                    vuetify3.VBtn(
                                        v_show="current_file_name == file_name",
                                        text=("language.visualized_button_title",),
                                        disabled=True,
                                    )

                vuetify3.VDivider()
                
                with vuetify3.VCardActions(classes="py-2"):
                    vuetify3.VSpacer()

                    with vuetify3.VBtnGroup(v_bind="props", border=True):
                        vuetify3.VBtn(
                            text=("language.cancel_button_title",),
                            click=ctrl.close_manage_files_dialog,
                        )

            # Confirm
            with vuetify3.VCard(
                v_show=f"manage_files_option == {ManageFilesOptions.Confirm}",
                title=("language.confirm_title",),
            ):
                vuetify3.VDivider()

                with vuetify3.VCardText(classes="py-2"):
                    with vuetify3.VContainer(classes="pa-0"):
                        with vuetify3.VRow(classes="my-3 mx-0"):
                            html.Span("{{ language.confirm_text }} <b>{{ file_to_delete }}</b>?", classes="text-caption")

                vuetify3.VDivider()
                
                with vuetify3.VCardActions(classes="py-2"):
                    vuetify3.VSpacer()
                    
                    with vuetify3.VBtnGroup(classes="mr-2", border=True):
                        vuetify3.VBtn(
                            text=("language.yes_button_title",),
                            click=ctrl.delete_file,
                        )

                    with vuetify3.VBtnGroup(border=True):
                        vuetify3.VBtn(
                            text=("language.no_button_title",),
                            color=Theme.IKEMColor,
                            click=f"manage_files_option = {ManageFilesOptions.Default}",
                        )
