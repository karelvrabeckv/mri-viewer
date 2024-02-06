from trame.widgets import vuetify3

from ...constants import Zoom

def zoom_interaction(self):
    with vuetify3.VCard(v_show=f"current_vti_file != None", classes="ma-4"): 
        # Title
        vuetify3.VCardTitle("{{ language.section_zoom_title }}", classes="text-white bg-grey-darken-1 py-1")
        
        # Content
        with vuetify3.VCardText(classes="py-2"):
            # Row
            with vuetify3.VRow(classes="py-2", justify="center", dense=True):
                # Button for zooming in
                with vuetify3.VTooltip(text=("language.zoom_in_tooltip",), location="bottom"):
                    with vuetify3.Template(v_slot_activator="{ props }"):
                        with vuetify3.VBtn(
                            v_bind="props",
                            variant="flat",
                            icon=True,
                            border=True,
                            classes="mx-1",
                            click=(self.zoom, f"['{Zoom.In}']"),
                        ):
                            vuetify3.VIcon(icon="mdi-plus")
                
                # Button for zooming out
                with vuetify3.VTooltip(text=("language.zoom_out_tooltip",), location="bottom"):
                    with vuetify3.Template(v_slot_activator="{ props }"):
                        with vuetify3.VBtn(
                            v_bind="props",
                            variant="flat",
                            icon=True,
                            border=True,
                            classes="mx-1",
                            click=(self.zoom, f"['{Zoom.Out}']"),
                        ):
                            vuetify3.VIcon(icon="mdi-minus")
