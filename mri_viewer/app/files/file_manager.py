import re, requests

from vtkmodules.vtkIOXML import vtkXMLImageDataReader

from .file_group import FileGroup
from .file import File

class FileManager:
    def __init__(self):
        self._latest = None
        self._groups = []
        self._file_to_group_mapping = dict()

    @property
    def latest(self):
        return self._latest

    def load_files_from_pc(self, input_raw_files):
        if not input_raw_files:
            return False
        
        for position, input_raw_file in enumerate(input_raw_files):
            if not self.load_file_from_pc(position, input_raw_file):
                return False
        return True

    def load_file_from_pc(self, position, input_raw_file):
        file = self.get_file_from_pc(input_raw_file)
        if not file:
            return False
        
        if position == 0:
            self._latest = file.name
        self.assign_file_to_group(file)
        return True

    def load_file_from_url(self, url):
        file = self.get_file_from_url(url)
        if not file:
            return False
        
        self._latest = file.name
        self.assign_file_to_group(file)
        return True

    def assign_file_to_group(self, file):
        if self.add_to_matching_group(file) is False:
            self.add_to_new_group(file)

    def get_file_from_pc(self, input_raw_file):
        file_name = input_raw_file.get("name")
        if not str(file_name).endswith(".vti"):
            return False
        
        file_reader = self.create_new_reader(input_raw_file.get("content"))
        if not file_reader:
            return False
        
        return self.create_new_file(file_name, file_reader)

    def get_file_from_url(self, url):
        try:
            response = requests.get(url)
        except:
            return False
        
        occurrences = re.findall("filename=\"(.+)\"", response.headers.get("content-disposition") or "")
        file_name = occurrences[0] if len(occurrences) else ""
        if not str(file_name).endswith(".vti"):
            return False
        
        file_reader = self.create_new_reader(response.text)
        if not file_reader:
            return False

        return self.create_new_file(file_name, file_reader)
        
    def create_new_reader(self, file_content):
        reader = vtkXMLImageDataReader()
        reader.ReadFromInputStringOn()
        
        data = file_content
        data_type = type(file_content)
        
        if data_type is str or (isinstance(data, list) and all(isinstance(i, str) for i in data)):
            reader.SetInputString("".join(data))
        elif data_type is bytes or (isinstance(data, list) and all(isinstance(i, bytes) for i in data)):
            reader.SetInputString(b"".join(data))
        else:
            return False
        
        reader.Update()
        
        return reader
        
    def create_new_file(self, file_name, file_reader):
        file = File()
        file.name = file_name
        file.reader = file_reader
        
        image_data = file_reader.GetOutput()
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
