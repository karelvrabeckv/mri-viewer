from .language import Language

class English(Language):
    def __init__(self):
        super().__init__(
            load_files_title="Load files",
            load_files_text="Load files from your computer or by using a URL. The maximum number of uploaded files is restricted to 10. The currently supported format is VTI only. The maximum size of an uploaded file is capped at 100 MB.",
            load_files_from_pc="Load files from PC",
            load_files_from_pc_error="An error has occurred while reading the uploaded file(s). Please check if the format of the file(s) is correct and not corrupted. Error code:",
            load_file_from_url="Load file from URL",
            load_file_from_url_error="An error has occurred while fetching the remote file. Please check your internet connection and the URL provided. It is also possible that the format of the remote file is not correct or is corrupted. Error code:",
            load_file_button_title="Load",
            back_button_title="Back",
            cancel_button_title="Cancel",
            user_guide_button_title="User guide",
            previous_file_tooltip="Show previous file",
            player_tooltip="Play or pause player",
            next_file_tooltip="Show next file",
            picker_mode_points_tooltip="Turn on tooltip with info about POINTS after clicking on them",
            picker_mode_cells_tooltip="Turn on tooltip with info about CELLS after clicking on them",
            toggle_axes_info_tooltip="Toggle axes info with grid",
            reset_camera_tooltip="Reset view",
            change_theme_tooltip="Toggle light and dark themes",
            file_name_select_title="File",
            data_array_select_title="Data Array",
            representation_select_title="Representation",
            representation_select_item_points="Points",
            representation_select_item_slice="Slice",
            representation_select_item_surface="Surface",
            representation_select_item_surface_with_edges="Surface with Edges",
            representation_select_item_wireframe="Wireframe",
            point_info_title="Point Information",
            cell_info_title="Cell Information",
            section_slice_title="Slice",
            slice_orientation_select_title="Orientation",
            slice_position_slider_title="Position",
            section_zoom_title="Zoom",
            section_zoom_tooltip="You can also press RIGHT MOUSE BUTTON and MOVE for faster zooming",
            section_zoom_slider_title="Power",
            zoom_in_tooltip="Click to zoom in",
            zoom_out_tooltip="Click to zoom out",
            section_translation_title="Translation",
            section_translation_tooltip="You can also press MIDDLE MOUSE BUTTON and MOVE for faster translation",
            section_translation_slider_title="Step",
            translate_x_axis_plus_tooltip="Click to move forward along X",
            translate_x_axis_minus_tooltip="Click to move backward along X",
            translate_y_axis_plus_tooltip="Click to move forward along Y",
            translate_y_axis_minus_tooltip="Click to move backward along Y",
            translate_z_axis_plus_tooltip="Click to move forward along Z",
            translate_z_axis_minus_tooltip="Click to move backward along Z",
            section_rotation_title="Rotation",
            section_rotation_tooltip="You can also press LEFT MOUSE BUTTON and MOVE for faster rotation",
            section_rotation_slider_title="Angle",
            rotate_x_axis_plus_tooltip="Click to rotate clockwise around X",
            rotate_x_axis_minus_tooltip="Click to rotate counter-clockwise around X",
            rotate_y_axis_plus_tooltip="Click to rotate clockwise around Y",
            rotate_y_axis_minus_tooltip="Click to rotate counter-clockwise around Y",
            rotate_z_axis_plus_tooltip="Click to rotate clockwise around Z",
            rotate_z_axis_minus_tooltip="Click to rotate counter-clockwise around Z",
        )
