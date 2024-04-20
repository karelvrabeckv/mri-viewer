import re, requests

from trame.app.file_upload import ClientFile

from vtkmodules.vtkIOXML import vtkXMLImageDataReader

from .file_group import FileGroup
from .file import File

import mri_viewer.app.constants as const

class FileManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__file_to_show = None
        self.__groups = []
        self.__file_to_group_mapping = {}

        self.__current_file = None
        self.__current_file_index = None
        self.__current_group = None
        self.__current_group_id = None
        
    @property
    def file_to_show(self):
        return self.__file_to_show

    @property
    def current_file(self):
        return self.__current_file

    @property
    def current_file_index(self):
        return self.__current_file_index

    @property
    def current_group(self):
        return self.__current_group

    @property
    def current_group_id(self):
        return self.__current_group_id

    def set_as_current(self, file_name):
        if not self.any_group():
            return

        self.__current_group_id = self.__file_to_group_mapping[file_name]
        self.__current_group = self.get_group(self.__current_group_id)
        self.__current_file_index = self.__current_group.get_all_file_names().index(file_name)
        self.__current_file = self.__current_group.files[file_name]

    def get_group(self, id):
        for group in self.__groups:
            if group.id == id:
                return group

    def upload_files_from_pc(self, files_from_pc):
        self.validate_file_group(files_from_pc)

        for index, file_from_pc in enumerate(files_from_pc):
            self.upload_file_from_pc(index, file_from_pc)

    def validate_file_group(self, files_from_pc):
        if len(files_from_pc) == 0:
            raise Exception(const.ErrorCodes.NoFilesToUpload)
        elif len(files_from_pc) > 10:
            raise Exception(const.ErrorCodes.TooManyFilesToUpload)

    def upload_file_from_pc(self, index, file_from_pc):
        raw_file = ClientFile(file_from_pc)
        self.validate_file(raw_file.name, raw_file.content, raw_file.size)
        
        if index == 0:
            self.__file_to_show = raw_file.name

        reader = self.create_new_reader(raw_file.content)
        file = self.create_new_file(raw_file.name, reader)
        self.assign_file_to_group(file)
        
    def upload_file_from_url(self, url):
        try:
            response = requests.get(url)
        except:
            raise Exception(const.ErrorCodes.InvalidURL)

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
            raise Exception(const.ErrorCodes.MissingHeaders)

        content_disposition = headers.get("content-disposition")
        if not content_disposition:
            raise Exception(const.ErrorCodes.MissingContentDispositionHeader)

        content_length = headers.get("content-length")
        if not content_length:
            raise Exception(const.ErrorCodes.MissingContentLengthHeader)

        content = response.content
        if not content:
            raise Exception(const.ErrorCodes.MissingContent)

        return content_disposition, content_length, content

    def validate_file(self, file_name: str, file_content: bytes, file_size: int):
        if not file_name.endswith(".vti"):
            raise Exception(const.ErrorCodes.WrongFileExtension)
        elif len(file_content) == 0:
            raise Exception(const.ErrorCodes.EmptyFile)
        elif file_size > 100_000_000:
            raise Exception(const.ErrorCodes.FileIsTooLarge)

    def create_new_reader(self, file_content):
        reader = vtkXMLImageDataReader()
        
        reader.ReadFromInputStringOn()
        reader.SetInputString(file_content)
        reader.Update()
        
        return reader

    def create_new_file(self, name, reader):
        image_data = reader.GetOutput()
        if image_data is None:
            raise Exception(const.ErrorCodes.MissingImageData)

        extent, origin, spacing = image_data.GetExtent(), image_data.GetOrigin(), image_data.GetSpacing()
        point_data, cell_data = image_data.GetPointData(), image_data.GetCellData()
        num_of_point_arrays, num_of_cell_arrays = point_data.GetNumberOfArrays(), cell_data.GetNumberOfArrays()
        
        if num_of_cell_arrays:
            data = cell_data
            data_arrays = [cell_data.GetArray(i).GetName() for i in range(num_of_cell_arrays)]
            
            scalars = cell_data.GetScalars()
            data_array = scalars.GetName() if scalars else data_arrays[0]
        elif num_of_point_arrays:
            data = point_data
            data_arrays = [point_data.GetArray(i).GetName() for i in range(num_of_point_arrays)]
            
            scalars = point_data.GetScalars()
            data_array = scalars.GetName() if scalars else data_arrays[0]
        else:
            raise Exception(const.ErrorCodes.MissingPointAndCellData)
        
        return File(name, reader, extent, origin, spacing, data, data_array, data_arrays)
 
    def assign_file_to_group(self, file):
        if self.add_to_matching_group(file) is False:
            self.add_to_new_group(file)
 
    def add_to_matching_group(self, file: File):
        if not self.any_group():
            return False
        
        for group in self.__groups:
            are_equal = self.are_equal(file.data_arrays, group.data_arrays)
            same_extent = file.extent == group.extent
            same_origin = file.origin == group.origin
            same_spacing = file.spacing == group.spacing

            if are_equal and same_extent and same_origin and same_spacing:
                group.add_file(file)
                self.__file_to_group_mapping[file.name] = group.id
                
                return True
        return False

    def any_group(self):
        return len(self.__groups)

    def are_equal(self, file_data_arrays, group_data_arrays):
        if len(file_data_arrays) != len(group_data_arrays):
            return False
        
        for i in range(len(file_data_arrays)):
            if file_data_arrays[i] != group_data_arrays[i]:
                return False
        return True

    def add_to_new_group(self, file: File):
        group = FileGroup(file)
        group.add_file(file)
        
        self.__file_to_group_mapping[file.name] = group.id
        self.__groups.append(group)

    def get_all_file_names(self):
        file_names = []
        if self.any_group():
            for group in self.__groups:
                file_names += group.get_all_file_names()

        return sorted(file_names)

    def delete_file(self, file_name):
        group_id = self.__file_to_group_mapping[file_name]
        group = self.get_group(group_id)

        group.delete_file(file_name)
        if group.get_num_of_files() == 0:
            self.__groups.remove(group)
