from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from functools import reduce

from ..constants import DEFAULT_REPRESENTATION
from .vti_file import VTIFile

class FileManager:
    def __init__(self):
        self._files = dict()
        self._group_active_array = ""
        self._group_data_arrays = []
        self._group_active_representation = DEFAULT_REPRESENTATION

    @property
    def files(self):
        return self._files
        
    @property
    def group_active_array(self):
        return self._group_active_array

    @group_active_array.setter
    def group_active_array(self, group_active_array): 
        self._group_active_array = group_active_array

    @property
    def group_data_arrays(self):
        return self._group_data_arrays

    @group_data_arrays.setter
    def group_data_arrays(self, group_data_arrays): 
        self._group_data_arrays = group_data_arrays

    @property
    def group_active_representation(self):
        return self._group_active_representation
    
    @group_active_representation.setter
    def group_active_representation(self, group_active_representation): 
        self._group_active_representation = group_active_representation
    
    def any_files(self):
        return len(self._files)
    
    def get_first_file_name(self):
        if self.any_files():
            return list(self._files.keys())[0]
        return None

    def get_all_file_names(self):
        if self.any_files():
            return list(self._files.keys())
        return None

    def get_file(self, file_name):
        if self.any_files():
            return self._files[file_name]
        return None
    
    def load_input_files(self, input_files):
        for input_file in input_files:
            self.load_input_file(input_file)
        
        first_file_name = self.get_first_file_name()
        first_file = self.get_file(first_file_name)
        
        self._group_active_array = first_file.active_array
        self._group_data_arrays = first_file.data_arrays
    
    def load_input_file(self, input_file):
        reader = vtkXMLImageDataReader()
        reader.ReadFromInputStringOn()
        reader.SetInputString(reduce(lambda a, b: a + b, input_file.get("content")))
        reader.Update()
        
        file = VTIFile()
        file.name = input_file.get("name")
        file.reader = reader
        
        image_data = reader.GetOutput()
        point_data, cell_data = image_data.GetPointData(), image_data.GetCellData()
        num_of_point_arrays, num_of_cell_arrays = point_data.GetNumberOfArrays(), cell_data.GetNumberOfArrays()
        
        if num_of_point_arrays:
            file.data = point_data
            file.active_array = point_data.GetScalars().GetName()
            file.data_arrays = [point_data.GetArray(i).GetName() for i in range(num_of_point_arrays)]
        elif num_of_cell_arrays:
            file.data = cell_data
            file.active_array = cell_data.GetScalars().GetName()
            file.data_arrays = [cell_data.GetArray(i).GetName() for i in range(num_of_cell_arrays)]

        self._files[file.name] = file
