from .file import File

import mri_viewer.app.constants as const

class FileGroup:
    def __init__(self, file: File):
        self.__files = dict()
        
        self.__default_view = None
        self.__current_view = None
        
        self.__data_array = file.data_array
        self.__data_arrays = file.data_arrays
        
        self.__representation = const.DEFAULT_REPRESENTATION
        
        self.__slice_orientation = const.DEFAULT_SLICE_ORIENTATION
        self.__slice_position = const.DEFAULT_SLICE_POSITION

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
    
    @slice_position.setter
    def slice_position(self, slice_position): 
        self.__slice_position = slice_position

    def get_num_of_files(self):
        return len(self.__files)
    
    def get_all_file_names(self):
        return list(self.__files.keys())

    def add_file(self, file: File):
        self.__files[file.name] = file
