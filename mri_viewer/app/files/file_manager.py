from functools import reduce

from vtkmodules.vtkIOXML import vtkXMLImageDataReader

from .file_group import FileGroup
from .file import File

class FileManager:
    def __init__(self):
        self._groups = []
        self._file_to_group_mapping = dict()

    def load_new_files(self, input_raw_files):
        for input_raw_file in input_raw_files:
            self.load_new_file(input_raw_file)

    def load_new_file(self, input_raw_file):
        file = self.create_new_file(input_raw_file)

        if self.add_to_matching_group(file) is False:
            self.add_to_new_group(file)

    def create_new_file(self, input_raw_file):
        reader = vtkXMLImageDataReader()
        reader.ReadFromInputStringOn()
        reader.SetInputString(reduce(lambda a, b: a + b, input_raw_file.get("content")))
        reader.Update()
        
        file = File()
        file.name = input_raw_file.get("name")
        file.reader = reader
        
        image_data = reader.GetOutput()
        point_data, cell_data = image_data.GetPointData(), image_data.GetCellData()
        num_of_point_arrays, num_of_cell_arrays = point_data.GetNumberOfArrays(), cell_data.GetNumberOfArrays()
        
        if num_of_point_arrays:
            file.data = point_data
            file.data_array = point_data.GetScalars().GetName()
            file.data_arrays = [point_data.GetArray(i).GetName() for i in range(num_of_point_arrays)]
        elif num_of_cell_arrays:
            file.data = cell_data
            file.data_array = cell_data.GetScalars().GetName()
            file.data_arrays = [cell_data.GetArray(i).GetName() for i in range(num_of_cell_arrays)]    

        return file
 
    def add_to_matching_group(self, file: File):
        if not self.any_group():
            # There are no groups
            return False
        
        for i, group in enumerate(self._groups):
            if self.are_equal(file.data_arrays, group.data_arrays):
                group.add_file(file)
                
                self._file_to_group_mapping[file.name] = i
                
                return True
        
        return False

    def any_group(self):
        return len(self._groups)

    def are_equal(self, file_data_arrays, group_data_arrays):
        # The lengths of data arrays differ
        if len(file_data_arrays) != len(group_data_arrays):
            return False
        
        for i in range(len(file_data_arrays)):
            if file_data_arrays[i] != group_data_arrays[i]:
                return False
        
        return True

    def add_to_new_group(self, file: File):
        group = FileGroup(file)
        group.add_file(file)
        
        self._file_to_group_mapping[file.name] = len(self._groups)        
        self._groups.append(group)
        
    def get_first_file_name(self):
        if self.any_group():
            return list(self._groups[0].files.keys())[0]
        return ""

    def get_all_file_names(self):
        if self.any_group():
            file_names = []
            for group in self._groups:
                file_names += group.get_all_file_names()

            return file_names
        return []

    def get_file(self, file_name) -> tuple[File, int, FileGroup, int]:
        if self.any_group():
            group_index = self._file_to_group_mapping[file_name]
            group = self._groups[group_index]
            file_index = group.get_all_file_names().index(file_name)
            file = group.files[file_name]

            return file, file_index, group, group_index
        return None
