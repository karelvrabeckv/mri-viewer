import mri_viewer.app.constants as const

class Language:
    def __init__(
        self,
        load_files_title,
        load_files_text,
        load_files_from_pc,
        load_files_from_pc_error,
        load_file_from_url,
        load_file_from_url_error,
        load_file_button_title,
        cancel_button_title,
        previous_file_tooltip,
        player_tooltip,
        next_file_tooltip,
        picker_mode_points_tooltip,
        picker_mode_cells_tooltip,
        toggle_axes_tooltip,
        reset_camera_tooltip,
        change_theme_tooltip,
        file_name_select_title,
        data_array_select_title,
        representation_select_title,
        representation_select_item_points,
        representation_select_item_slice,
        representation_select_item_surface,
        representation_select_item_surface_with_edges,
        representation_select_item_wireframe,
        point_info_title,
        cell_info_title,
        section_slice_title,
        slice_orientation_select_title,
        slice_position_slider_title,
        factor_slider_title,
        section_zoom_title,
        section_zoom_tooltip,
        zoom_in_tooltip,
        zoom_out_tooltip,
        section_translation_title,
        section_translation_tooltip,
        translate_x_axis_plus_tooltip,
        translate_x_axis_minus_tooltip,
        translate_y_axis_plus_tooltip,
        translate_y_axis_minus_tooltip,
        translate_z_axis_plus_tooltip,
        translate_z_axis_minus_tooltip,
        section_rotation_title,
        section_rotation_tooltip,
        rotate_x_axis_plus_tooltip,
        rotate_x_axis_minus_tooltip,
        rotate_y_axis_plus_tooltip,
        rotate_y_axis_minus_tooltip,
        rotate_z_axis_plus_tooltip,
        rotate_z_axis_minus_tooltip,
    ):
        self.__words = {
            "load_files_title": load_files_title,
            "load_files_text": load_files_text,
            "load_files_from_pc": load_files_from_pc,
            "load_files_from_pc_error": load_files_from_pc_error,
            "load_file_from_url": load_file_from_url,
            "load_file_from_url_error": load_file_from_url_error,
            "load_file_button_title": load_file_button_title,
            "cancel_button_title": cancel_button_title,
            "previous_file_tooltip": previous_file_tooltip,
            "player_tooltip": player_tooltip,
            "next_file_tooltip": next_file_tooltip,
            "picker_mode_points_tooltip": picker_mode_points_tooltip,
            "picker_mode_cells_tooltip": picker_mode_cells_tooltip,
            "toggle_axes_tooltip": toggle_axes_tooltip,
            "reset_camera_tooltip": reset_camera_tooltip,
            "change_theme_tooltip": change_theme_tooltip,
            "file_name_select_title": file_name_select_title,
            "data_array_select_title": data_array_select_title,
            "representation_select_title": representation_select_title,
            "current_representation_items": [
                {
                    "title": representation_select_item_points,
                    "value": const.Representation.Points,
                },
                {
                    "title": representation_select_item_slice,
                    "value": const.Representation.Slice,
                },
                {
                    "title": representation_select_item_surface,
                    "value": const.Representation.Surface,
                },
                {
                    "title": representation_select_item_surface_with_edges,
                    "value": const.Representation.SurfaceWithEdges,
                },
                {
                    "title": representation_select_item_wireframe,
                    "value": const.Representation.Wireframe,
                },
            ],
            "point_info_title": point_info_title,
            "cell_info_title": cell_info_title,
            "section_slice_title": section_slice_title,
            "slice_orientation_select_title": slice_orientation_select_title,
            "slice_position_slider_title": slice_position_slider_title,
            "factor_slider_title": factor_slider_title,
            "section_zoom_title": section_zoom_title,
            "section_zoom_tooltip": section_zoom_tooltip,
            "zoom_in_tooltip": zoom_in_tooltip,
            "zoom_out_tooltip": zoom_out_tooltip,
            "section_translation_title": section_translation_title,
            "section_translation_tooltip": section_translation_tooltip,
            "translate_x_axis_plus_tooltip": translate_x_axis_plus_tooltip,
            "translate_x_axis_minus_tooltip": translate_x_axis_minus_tooltip,
            "translate_y_axis_plus_tooltip": translate_y_axis_plus_tooltip,
            "translate_y_axis_minus_tooltip": translate_y_axis_minus_tooltip,
            "translate_z_axis_plus_tooltip": translate_z_axis_plus_tooltip,
            "translate_z_axis_minus_tooltip": translate_z_axis_minus_tooltip,
            "section_rotation_title": section_rotation_title,
            "section_rotation_tooltip": section_rotation_tooltip,
            "rotate_x_axis_plus_tooltip": rotate_x_axis_plus_tooltip,
            "rotate_x_axis_minus_tooltip": rotate_x_axis_minus_tooltip,
            "rotate_y_axis_plus_tooltip": rotate_y_axis_plus_tooltip,
            "rotate_y_axis_minus_tooltip": rotate_y_axis_minus_tooltip,
            "rotate_z_axis_plus_tooltip": rotate_z_axis_plus_tooltip,
            "rotate_z_axis_minus_tooltip": rotate_z_axis_minus_tooltip,
        }

    @property
    def words(self):
        return self.__words
