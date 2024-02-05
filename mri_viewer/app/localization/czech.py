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
        slice_orientation_select_title = "Orientace řezu"
        slice_position_slider_title = "Pozice řezu"
        point_information_title = "Informace o bodě"
        cell_information_title = "Informace o buňce"
        x_axis_title = "Osa X"
        y_axis_title = "Osa Y"
        z_axis_title = "Osa Z"
        
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
            slice_orientation_select_title,
            slice_position_slider_title,
            point_information_title,
            cell_information_title,
            x_axis_title,
            y_axis_title,
            z_axis_title,
        )
