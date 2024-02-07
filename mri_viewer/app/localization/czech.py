from .language import Language

class Czech(Language):
    def __init__(self):
        upload_vti_files_title = "Nahrát soubory VTI"
        vti_file_select_title = "Soubor"
        data_array_select_title = "Datová složka"
        representation_select_title = "Reprezentace"
        representation_select_item_points = "Body"
        representation_select_item_slice = "Řez"
        representation_select_item_surface = "Povrch"
        representation_select_item_surface_with_edges = "Povrch s hranami"
        representation_select_item_wireframe = "Mřížka"
        point_information_title = "Informace o bodě"
        cell_information_title = "Informace o buňce"
        x_axis_title = "Osa X"
        y_axis_title = "Osa Y"
        z_axis_title = "Osa Z"
        section_slice_title = "Řez"
        slice_orientation_select_title = "Orientace"
        slice_position_slider_title = "Pozice"
        section_zoom_title = "Přiblížení"
        zoom_in_tooltip = "Klikněte pro přiblížení"
        zoom_out_tooltip = "Klikněte pro oddálení"
        section_translation_title = "Posun"
        translate_x_axis_plus_tooltip = "Klikněte pro posun vpřed po ose X"
        translate_x_axis_minus_tooltip = "Klikněte pro posun vzad po ose X"
        translate_y_axis_plus_tooltip = "Klikněte pro posun vpřed po ose Y"
        translate_y_axis_minus_tooltip = "Klikněte pro posun vzad po ose Y"
        translate_z_axis_plus_tooltip = "Klikněte pro posun vpřed po ose Z"
        translate_z_axis_minus_tooltip = "Klikněte pro posun vzad po ose Z"
        section_rotation_title = "Rotace"
        rotate_x_axis_plus_tooltip = "Klikněte pro kladnou rotaci kolem osy X"
        rotate_x_axis_minus_tooltip = "Klikněte pro zápornou rotaci kolem osy X"
        rotate_y_axis_plus_tooltip = "Klikněte pro kladnou rotaci kolem osy Y"
        rotate_y_axis_minus_tooltip = "Klikněte pro zápornou rotaci kolem osy Y"
        rotate_z_axis_plus_tooltip = "Klikněte pro kladnou rotaci kolem osy Z"
        rotate_z_axis_minus_tooltip = "Klikněte pro zápornou rotaci kolem osy Z"
        
        super().__init__(
            upload_vti_files_title,
            vti_file_select_title,
            data_array_select_title,
            representation_select_title,
            representation_select_item_points,
            representation_select_item_slice,
            representation_select_item_surface,
            representation_select_item_surface_with_edges,
            representation_select_item_wireframe,
            point_information_title,
            cell_information_title,
            x_axis_title,
            y_axis_title,
            z_axis_title,
            section_slice_title,
            slice_orientation_select_title,
            slice_position_slider_title,
            section_zoom_title,
            zoom_in_tooltip,
            zoom_out_tooltip,
            section_translation_title,
            translate_x_axis_plus_tooltip,
            translate_x_axis_minus_tooltip,
            translate_y_axis_plus_tooltip,
            translate_y_axis_minus_tooltip,
            translate_z_axis_plus_tooltip,
            translate_z_axis_minus_tooltip,
            section_rotation_title,
            rotate_x_axis_plus_tooltip,
            rotate_x_axis_minus_tooltip,
            rotate_y_axis_plus_tooltip,
            rotate_y_axis_minus_tooltip,
            rotate_z_axis_plus_tooltip,
            rotate_z_axis_minus_tooltip,
        )
