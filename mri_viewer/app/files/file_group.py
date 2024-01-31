from .file import File
from ..constants import DEFAULT_REPRESENTATION

class FileGroup:
    def __init__(self, file: File):
        self._files = dict()
        
        self._active_array = file.default_array
        self._data_arrays = file.data_arrays
        self._active_representation = DEFAULT_REPRESENTATION

    @property
    def files(self):
        return self._files

    @property
    def active_array(self):
        return self._active_array

    @active_array.setter
    def active_array(self, active_array): 
        self._active_array = active_array

    @property
    def data_arrays(self):
        return self._data_arrays

    @data_arrays.setter
    def data_arrays(self, data_arrays): 
        self._data_arrays = data_arrays

    @property
    def active_representation(self):
        return self._active_representation
    
    @active_representation.setter
    def active_representation(self, active_representation): 
        self._active_representation = active_representation

    def get_num_of_files(self):
        return len(self._files)
    
    def get_all_file_names(self):
        return list(self._files.keys())

    def add_file(self, file: File):
        self._files[file.name] = file
