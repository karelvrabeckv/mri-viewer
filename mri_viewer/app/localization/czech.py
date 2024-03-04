from .language import Language

class Czech(Language):
    def __init__(self):
        super().__init__(
            load_files_title="Nahrát soubory",
            load_files_from_pc="Nahrát soubory z PC",
            load_files_from_pc_error="Při čtení nahraného souboru (souborů) došlo k chybě. Zkontrolujte prosím, zda je formát souboru (souborů) správný a zda není poškozen.",
            load_file_from_url="Nahrát soubor z URL",
            load_file_from_url_error="Při načítání vzdáleného souboru došlo k chybě. Zkontrolujte prosím své internetové připojení a zadanou URL adresu. Je také možné, že formát vzdáleného souboru není správný nebo je poškozen.",
            supported_file_formats="Podporované formáty: .vti",
            load_file_button_title="Načíst",
            cancel_button_title="Zavřít",
            previous_file_tooltip="Zobrazit předchozí snímek",
            player_tooltip="Přehrát či pozastavit sekvenci snímků",
            next_file_tooltip="Zobrazit následující snímek",
            picker_mode_points_tooltip="Zapnout zobrazování informací o BODECH po kliknutí na ně",
            picker_mode_cells_tooltip="Zapnout zobrazování informací o BUŇKÁCH po kliknutí na ně",
            toggle_axes_tooltip="Zobrazit informace o osách",
            reset_camera_tooltip="Obnovit původní zobrazení",
            change_theme_tooltip="Přepnout mezi světlým a tmavým režimem",
            file_name_select_title="Soubor",
            data_array_select_title="Datová složka",
            representation_select_title="Reprezentace",
            representation_select_item_points="Body",
            representation_select_item_slice="Řez",
            representation_select_item_surface="Povrch",
            representation_select_item_surface_with_edges="Povrch s hranami",
            representation_select_item_wireframe="Mřížka",
            point_information_title="Informace o bodě",
            cell_information_title="Informace o buňce",
            section_slice_title="Řez",
            slice_orientation_select_title="Orientace",
            slice_position_slider_title="Pozice",
            factor_slider_title="Faktor",
            section_zoom_title="Přiblížení",
            section_zoom_tooltip="Pro rychlejší přibližování použijte KOLEČKO MYŠI",
            zoom_in_tooltip="Klikněte pro přiblížení",
            zoom_out_tooltip="Klikněte pro oddálení",
            section_translation_title="Posun",
            section_translation_tooltip="Pro rychlejší posun použijte ALT + LEVÉ TLAČÍTKO MYŠI a pohybujte do různých směrů",
            translate_x_axis_plus_tooltip="Klikněte pro posun vpřed po ose X",
            translate_x_axis_minus_tooltip="Klikněte pro posun vzad po ose X",
            translate_y_axis_plus_tooltip="Klikněte pro posun vpřed po ose Y",
            translate_y_axis_minus_tooltip="Klikněte pro posun vzad po ose Y",
            translate_z_axis_plus_tooltip="Klikněte pro posun vpřed po ose Z",
            translate_z_axis_minus_tooltip="Klikněte pro posun vzad po ose Z",
            section_rotation_title="Rotace",
            section_rotation_tooltip="Pro rychlejší rotaci použijte LEVÉ TLAČÍTKO MYŠI a pohybujte do různých směrů",
            rotate_x_axis_plus_tooltip="Klikněte pro rotaci ve směru hodinových ručiček kolem osy X",
            rotate_x_axis_minus_tooltip="Klikněte pro rotaci proti směru hodinových ručiček kolem osy X",
            rotate_y_axis_plus_tooltip="Klikněte pro rotaci ve směru hodinových ručiček kolem osy Y",
            rotate_y_axis_minus_tooltip="Klikněte pro rotaci proti směru hodinových ručiček kolem osy Y",
            rotate_z_axis_plus_tooltip="Klikněte pro rotaci ve směru hodinových ručiček kolem osy Z",
            rotate_z_axis_minus_tooltip="Klikněte pro rotaci proti směru hodinových ručiček kolem osy Z",
        )
