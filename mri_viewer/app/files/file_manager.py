import re, requests

from trame.app.file_upload import ClientFile

from vtkmodules.vtkIOXML import vtkXMLImageDataReader

from .file_group import FileGroup
from .file import File

class FileManager:
    def __init__(self):
        self.__file_to_show = None
        self.__groups = []
        self.__file_to_group_mapping = {}

    @property
    def file_to_show(self):
        return self.__file_to_show

    def load_files_from_pc(self, files_from_pc):
        self.validate_file_group(files_from_pc)

        for index, file_from_pc in enumerate(files_from_pc):
            self.load_file_from_pc(index, file_from_pc)

    def validate_file_group(self, files_from_pc):
        if len(files_from_pc) == 0:
            raise Exception("NO-FILES-TO-UPLOAD")
        elif len(files_from_pc) > 10:
            raise Exception("TOO-MANY-FILES-TO-UPLOAD")

    def load_file_from_pc(self, index, file_from_pc):
        raw_file = ClientFile(file_from_pc)
        self.validate_file(raw_file.name, raw_file.content, raw_file.size)
        
        if index == 0:
            self.__file_to_show = raw_file.name

        reader = self.create_new_reader(raw_file.content)
        file = self.create_new_file(raw_file.name, reader)
        self.assign_file_to_group(file)
        
    def load_file_from_url(self, url):
        try:
            response = requests.get(url)
        except:
            raise Exception("INVALID-URL")

        content_disposition, content_length, content = self.validate_request(response)

        file_name = ""
        occurrences = re.findall("filename=\"(.+)\"", content_disposition)
        if len(occurrences) != 0:
            file_name = occurrences[0]

        file_content = content
        file_size = int(content_length)
        
        self.validate_file(file_name, file_content, file_size)
        
        self.__file_to_show = file_name
        
        reader = self.create_new_reader(response.content)
        file = self.create_new_file(file_name, reader)
        self.assign_file_to_group(file)

    def validate_request(self, response):
        headers = response.headers
        if not headers:
            raise Exception("MISSING-HEADERS")

        content_disposition = headers.get("content-disposition")
        if not content_disposition:
            raise Exception("MISSING-CONTENT-DISPOSITION-HEADER")

        content_length = headers.get("content-length")
        if not content_length:
            raise Exception("MISSING-CONTENT-LENGTH-HEADER")

        content = response.content
        if not content:
            raise Exception("MISSING-CONTENT")

        return content_disposition, content_length, content

    def validate_file(self, file_name: str, file_content: bytes, file_size: int):
        if not file_name.endswith(".vti"):
            raise Exception("WRONG-FILE-EXTENSION")
        elif len(file_content) == 0:
            raise Exception("EMPTY-FILE")
        elif file_size > 100_000_000:
            raise Exception("FILE-IS-TOO-LARGE")

    def create_new_reader(self, file_content):
        reader = vtkXMLImageDataReader()
        
        reader.ReadFromInputStringOn()
        reader.SetInputString(file_content)
        reader.Update()
        
        return reader

    def create_new_file(self, name, reader):
        image_data = reader.GetOutput()
        if image_data is None:
            raise Exception("NO-IMAGE-DATA")

        extent = image_data.GetExtent()
        point_data, cell_data = image_data.GetPointData(), image_data.GetCellData()
        num_of_point_arrays, num_of_cell_arrays = point_data.GetNumberOfArrays(), cell_data.GetNumberOfArrays()
        
        if num_of_point_arrays:
            data = point_data
            data_arrays = [point_data.GetArray(i).GetName() for i in range(num_of_point_arrays)]
            
            scalars = point_data.GetScalars()
            data_array = scalars.GetName() if scalars else data_arrays[0]
        elif num_of_cell_arrays:
            data = cell_data
            data_arrays = [cell_data.GetArray(i).GetName() for i in range(num_of_cell_arrays)]
            
            scalars = cell_data.GetScalars()
            data_array = scalars.GetName() if scalars else data_arrays[0]
        else:
            raise Exception("NO-POINT-NOR-CELL-DATA")
        
        return File(name, reader, extent, data, data_array, data_arrays)
 
    def assign_file_to_group(self, file):
        if self.add_to_matching_group(file) is False:
            self.add_to_new_group(file)
 
    def add_to_matching_group(self, file: File):
        if not self.any_group():
            return False
        
        for index, group in enumerate(self.__groups):
            if self.are_equal(file.data_arrays, group.data_arrays) and self.same_extent(file.extent, group.extent):
                group.add_file(file)
                self.__file_to_group_mapping[file.name] = index
                
                return True
        return False

    def any_group(self):
        return len(self.__groups)

    def are_equal(self, file_data_arrays, group_data_arrays):
        if len(file_data_arrays) != len(group_data_arrays):
            return False
        
        file_data_arrays.sort()
        group_data_arrays.sort()
        
        for i in range(len(file_data_arrays)):
            if file_data_arrays[i] != group_data_arrays[i]:
                return False
        return True

    def same_extent(self, file_extent, group_extent):
        return file_extent == group_extent

    def add_to_new_group(self, file: File):
        group = FileGroup(file)
        group.add_file(file)
        
        self.__file_to_group_mapping[file.name] = len(self.__groups)        
        self.__groups.append(group)

    def get_all_file_names(self):
        file_names = []
        if self.any_group():
            for group in self.__groups:
                file_names += group.get_all_file_names()

        return file_names

    def get_file(self, file_name) -> tuple[File, int, FileGroup, int]:
        if self.any_group():
            group_index = self.__file_to_group_mapping[file_name]
            group = self.__groups[group_index]
            file_index = group.get_all_file_names().index(file_name)
            file = group.files[file_name]

            return file, file_index, group, group_index
        return None
