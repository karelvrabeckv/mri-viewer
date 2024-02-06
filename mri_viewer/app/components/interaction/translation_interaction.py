from trame.widgets import vuetify3

from ...constants import Translation

def translation_interaction(self):
    with vuetify3.VCard(v_show=f"current_vti_file != None", classes="ma-4"): 
        # Title
        vuetify3.VCardTitle(
            "{{ language.section_translation_title }}",
            classes="text-white bg-grey-darken-1 py-1"
        )
        
        # Content
        with vuetify3.VCardText(classes="py-2"):
            # Row (X-Axis)
            with vuetify3.VRow(classes="py-2", justify="center", dense=True):
                # Label (X-Axis)
                vuetify3.VBannerText("X:", classes="d-flex align-center text-body-1")
                
                # Plus button (X-Axis)
                with vuetify3.VTooltip(
                    text=("language.translate_x_axis_plus_tooltip",),
                    location="bottom"
                ):
                    with vuetify3.Template(v_slot_activator="{ props }"):
                        with vuetify3.VBtn(
                            v_bind="props",
                            variant="flat",
                            icon=True,
                            border=True,
                            classes="mx-1",
                            click=(self.translate, f"['{Translation.XAxisPlus}']"),
                        ):
                            vuetify3.VIcon(icon="mdi-plus")
                
                # Minus button (X-Axis)
                with vuetify3.VTooltip(
                    text=("language.translate_x_axis_minus_tooltip",),
                    location="bottom"
                ):
                    with vuetify3.Template(v_slot_activator="{ props }"):
                        with vuetify3.VBtn(
                            v_bind="props",
                            variant="flat",
                            icon=True,
                            border=True,
                            classes="mx-1",
                            click=(self.translate, f"['{Translation.XAxisMinus}']"),
                        ):
                            vuetify3.VIcon(icon="mdi-minus")

            # Row (Y-Axis)
            with vuetify3.VRow(classes="py-2", justify="center", dense=True):
                # Label (Y-Axis)
                vuetify3.VBannerText("Y:", classes="d-flex align-center text-body-1")
                
                # Plus button (Y-Axis)
                with vuetify3.VTooltip(
                    text=("language.translate_y_axis_plus_tooltip",),
                    location="bottom"
                ):
                    with vuetify3.Template(v_slot_activator="{ props }"):
                        with vuetify3.VBtn(
                            v_bind="props",
                            variant="flat",
                            icon=True,
                            border=True,
                            classes="mx-1",
                            click=(self.translate, f"['{Translation.YAxisPlus}']"),
                        ):
                            vuetify3.VIcon(icon="mdi-plus")
                
                # Minus button (Y-Axis)
                with vuetify3.VTooltip(
                    text=("language.translate_y_axis_minus_tooltip",),
                    location="bottom"
                ):
                    with vuetify3.Template(v_slot_activator="{ props }"):
                        with vuetify3.VBtn(
                            v_bind="props",
                            variant="flat",
                            icon=True,
                            border=True,
                            classes="mx-1",
                            click=(self.translate, f"['{Translation.YAxisMinus}']"),
                        ):
                            vuetify3.VIcon(icon="mdi-minus")

            # Row (Z-Axis)
            with vuetify3.VRow(classes="py-2", justify="center", dense=True):
                # Label (Z-Axis)
                vuetify3.VBannerText("Z:", classes="d-flex align-center text-body-1")
                
                # Plus button (Z-Axis)
                with vuetify3.VTooltip(
                    text=("language.translate_z_axis_plus_tooltip",),
                    location="bottom"
                ):
                    with vuetify3.Template(v_slot_activator="{ props }"):
                        with vuetify3.VBtn(
                            v_bind="props",
                            variant="flat",
                            icon=True,
                            border=True,
                            classes="mx-1",
                            click=(self.translate, f"['{Translation.ZAxisPlus}']"),
                        ):
                            vuetify3.VIcon(icon="mdi-plus")
                
                # Minus button (Z-Axis)
                with vuetify3.VTooltip(
                    text=("language.translate_z_axis_minus_tooltip",),
                    location="bottom"
                ):
                    with vuetify3.Template(v_slot_activator="{ props }"):
                        with vuetify3.VBtn(
                            v_bind="props",
                            variant="flat",
                            icon=True,
                            border=True,
                            classes="mx-1",
                            click=(self.translate, f"['{Translation.ZAxisMinus}']"),
                        ):
                            vuetify3.VIcon(icon="mdi-minus")
