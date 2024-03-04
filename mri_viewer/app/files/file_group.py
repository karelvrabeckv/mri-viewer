from .file import File

import mri_viewer.app.constants as const

class FileGroup:
    def __init__(self, file: File):
        self.__files = dict()
        
        self.__default_view = None
        self.__current_view = None
        
        self.__extent = file.extent
        
        self.__data_array = file.data_array
        self.__data_arrays = file.data_arrays
        
        self.__representation = const.DEFAULT_REPRESENTATION
        
        self.__slice_orientation = const.DEFAULT_SLICE_ORIENTATION
        self.__slice_position = {
            const.Planes.XY: self.deduce_min_slice_position(const.Planes.XY),
            const.Planes.YZ: self.deduce_min_slice_position(const.Planes.YZ),
            const.Planes.XZ: self.deduce_min_slice_position(const.Planes.XZ),
        }

    @property
    def files(self):
        return self.__files

    @property
    def default_view(self):
        return self.__default_view
    
    @default_view.setter 
    def default_view(self, default_view): 
        self.__default_view = default_view

    @property
    def current_view(self):
        return self.__current_view
    
    @current_view.setter 
    def current_view(self, current_view): 
        self.__current_view = current_view

    @property
    def extent(self):
        return self.__extent

    @extent.setter
    def extent(self, extent): 
        self.__extent = extent

    @property
    def data_array(self):
        return self.__data_array

    @data_array.setter
    def data_array(self, data_array): 
        self.__data_array = data_array

    @property
    def data_arrays(self):
        return self.__data_arrays

    @data_arrays.setter
    def data_arrays(self, data_arrays): 
        self.__data_arrays = data_arrays

    @property
    def representation(self):
        return self.__representation
    
    @representation.setter
    def representation(self, representation): 
        self.__representation = representation

    @property
    def slice_orientation(self):
        return self.__slice_orientation
    
    @slice_orientation.setter
    def slice_orientation(self, slice_orientation): 
        self.__slice_orientation = slice_orientation

    @property
    def slice_position(self):
        return self.__slice_position
    
    def get_num_of_files(self):
        return len(self.__files)
    
    def get_all_file_names(self):
        return list(self.__files)

    def add_file(self, file: File):
        self.__files[file.name] = file

    def deduce_min_slice_position(self, orientation: const.Planes):
        min_x, _, min_y, _, min_z, _ = self.__extent
        
        if orientation == const.Planes.XY:
            return min_z
        elif orientation == const.Planes.YZ:
            return min_x
        elif orientation == const.Planes.XZ:
            return min_y

    def deduce_max_slice_position(self, orientation: const.Planes):
        _, max_x, _, max_y, _, max_z = self.__extent
        
        if orientation == const.Planes.XY:
            return max_z
        elif orientation == const.Planes.YZ:
            return max_x
        elif orientation == const.Planes.XZ:
            return max_y
