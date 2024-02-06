from ..constants import Representation

class Language:
    def __init__(
        self,
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
    ):
        self._words = {
            "upload_vti_files_title": upload_vti_files_title,
            "vti_file_select_title": vti_file_select_title,
            "data_array_select_title": data_array_select_title,
            "representation_select_title": representation_select_title,
            "representation_select_items": [
                {
                    "title": representation_select_item_points,
                    "value": Representation.Points,
                },
                {
                    "title": representation_select_item_slice,
                    "value": Representation.Slice,
                },
                {
                    "title": representation_select_item_surface,
                    "value": Representation.Surface,
                },
                {
                    "title": representation_select_item_surface_with_edges,
                    "value": Representation.SurfaceWithEdges,
                },
                {
                    "title": representation_select_item_wireframe,
                    "value": Representation.Wireframe,
                },
            ],
            "slice_orientation_select_title": slice_orientation_select_title,
            "slice_position_slider_title": slice_position_slider_title,
            "point_information_title": point_information_title,
            "cell_information_title": cell_information_title,
            "x_axis_title": x_axis_title,
            "y_axis_title": y_axis_title,
            "z_axis_title": z_axis_title,
            "section_zoom_title": section_zoom_title,
            "zoom_in_tooltip": zoom_in_tooltip,
            "zoom_out_tooltip": zoom_out_tooltip,
            "section_translation_title": section_translation_title,
            "translate_x_axis_plus_tooltip": translate_x_axis_plus_tooltip,
            "translate_x_axis_minus_tooltip": translate_x_axis_minus_tooltip,
            "translate_y_axis_plus_tooltip": translate_y_axis_plus_tooltip,
            "translate_y_axis_minus_tooltip": translate_y_axis_minus_tooltip,
            "translate_z_axis_plus_tooltip": translate_z_axis_plus_tooltip,
            "translate_z_axis_minus_tooltip": translate_z_axis_minus_tooltip,
        }

    @property
    def words(self):
        return self._words
