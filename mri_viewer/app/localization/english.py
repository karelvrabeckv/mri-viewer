from .language import Language

class English(Language):
    def __init__(self):
        upload_vti_files_title = "Upload VTI Files"
        vti_file_select_title = "File"
        data_array_select_title = "Data Array"
        representation_select_title = "Representation"
        representation_select_item_points = "Points"
        representation_select_item_slice = "Slice"
        representation_select_item_surface = "Surface"
        representation_select_item_surface_with_edges = "Surface with Edges"
        representation_select_item_wireframe = "Wireframe"
        slice_orientation_select_title = "Slice Orientation"
        slice_position_slider_title = "Slice Position"
        point_information_title = "Point Information"
        cell_information_title = "Cell Information"
        x_axis_title = "X-Axis"
        y_axis_title = "Y-Axis"
        z_axis_title = "Z-Axis"
        
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
