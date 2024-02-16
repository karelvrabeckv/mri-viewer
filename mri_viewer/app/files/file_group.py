from .file import File

import mri_viewer.app.constants as const

class FileGroup:
    def __init__(self, file: File):
        self._files = dict()
        
        self._default_view = None
        self._current_view = None
        
        self._data_array = file.data_array
        self._data_arrays = file.data_arrays
        
        self._representation = const.DEFAULT_REPRESENTATION
        
        self._slice_orientation = const.DEFAULT_SLICE_ORIENTATION
        self._slice_position = const.DEFAULT_SLICE_POSITION

    @property
    def files(self):
        return self._files

    @property
    def default_view(self):
        return self._default_view
    
    @default_view.setter 
    def default_view(self, default_view): 
        self._default_view = default_view

    @property
    def current_view(self):
        return self._current_view
    
    @current_view.setter 
    def current_view(self, current_view): 
        self._current_view = current_view

    @property
    def data_array(self):
        return self._data_array

    @data_array.setter
    def data_array(self, data_array): 
        self._data_array = data_array

    @property
    def data_arrays(self):
        return self._data_arrays

    @data_arrays.setter
    def data_arrays(self, data_arrays): 
        self._data_arrays = data_arrays

    @property
    def representation(self):
        return self._representation
    
    @representation.setter
    def representation(self, representation): 
        self._representation = representation

    @property
    def slice_orientation(self):
        return self._slice_orientation
    
    @slice_orientation.setter
    def slice_orientation(self, slice_orientation): 
        self._slice_orientation = slice_orientation

    @property
    def slice_position(self):
        return self._slice_position
    
    @slice_position.setter
    def slice_position(self, slice_position): 
        self._slice_position = slice_position

    def get_num_of_files(self):
        return len(self._files)
    
    def get_all_file_names(self):
        return list(self._files.keys())

    def add_file(self, file: File):
        self._files[file.name] = file
