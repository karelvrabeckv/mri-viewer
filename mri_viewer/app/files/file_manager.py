import re, requests

from trame.app.file_upload import ClientFile

from vtkmodules.vtkIOXML import vtkXMLImageDataReader

from .file_group import FileGroup
from .file import File

import mri_viewer.app.constants as const

class FileManager:
    """Class representing manager of files."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            # Create only one instance of this class
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__file_to_show = None
        self.__file_to_group_mapping = {}
        self.__groups = []

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

    def upload_files_from_pc(self, files_from_pc):
        """Upload files from local computer."""

        self.validate_files(files_from_pc)

        for index, file_from_pc in enumerate(files_from_pc):
            self.upload_file_from_pc(index, file_from_pc)

    def upload_file_from_pc(self, index, file_from_pc):
        """Upload file from local computer."""

        raw_file = ClientFile(file_from_pc)
        self.validate_file(raw_file.name, raw_file.content, raw_file.size)

        if index == 0:
            self.__file_to_show = raw_file.name

        reader = self.create_new_reader(raw_file.content)
        self.save_file(raw_file.name, reader)
        
    def upload_file_from_url(self, url):
        """Upload file from remote server."""

        try:
            response = requests.get(url)
        except:
            raise Exception(const.ErrorCodes.InvalidURL)

        headers = response.headers
        content_disposition = headers.get("content-disposition")
        content_length = headers.get("content-length")
        content = response.content
    
        self.validate_response(headers, content_disposition, content_length, content)

        file_name = ""
        occurrences = re.findall("filename=\"(.+)\"", content_disposition)
        if len(occurrences) != 0:
            file_name = occurrences[0]

        file_content = content
        file_size = int(content_length)
        
        self.validate_file(file_name, file_content, file_size)
        
        self.__file_to_show = file_name
        
        reader = self.create_new_reader(file_content)
        self.save_file(file_name, reader)

    def validate_files(self, files_from_pc):
        """Validate files from local computer."""

        if len(files_from_pc) == 0:
            raise Exception(const.ErrorCodes.NoFilesToUpload)
        elif len(files_from_pc) > 10:
            raise Exception(const.ErrorCodes.TooManyFilesToUpload)

    def validate_file(self, file_name: str, file_content: bytes, file_size: int):
        """Validate file from local computer."""

        if not file_name.endswith(".vti"):
            raise Exception(const.ErrorCodes.WrongFileExtension)
        elif len(file_content) == 0:
            raise Exception(const.ErrorCodes.EmptyFile)
        elif file_size > 100_000_000:
            raise Exception(const.ErrorCodes.FileIsTooLarge)

    def validate_response(self, headers, content_disposition, content_length, content):
        """Validate response to request sent to particular URL."""

        if not headers:
            raise Exception(const.ErrorCodes.MissingHeaders)
        elif not content_disposition:
            raise Exception(const.ErrorCodes.MissingContentDispositionHeader)
        elif not content_length:
            raise Exception(const.ErrorCodes.MissingContentLengthHeader)
        elif not content:
            raise Exception(const.ErrorCodes.MissingContent)

    def create_new_reader(self, file_content):
        """Create reader for VTI files."""

        reader = vtkXMLImageDataReader()
        
        reader.ReadFromInputStringOn()
        reader.SetInputString(file_content)
        reader.Update()
        
        return reader

    def save_file(self, name, reader: vtkXMLImageDataReader):
        """Save file to particular group."""

        image_data = reader.GetOutput()
        if image_data is None:
            raise Exception(const.ErrorCodes.MissingImageData)

        extent, origin, spacing = image_data.GetExtent(), image_data.GetOrigin(), image_data.GetSpacing()
        point_data, cell_data = image_data.GetPointData(), image_data.GetCellData()
        num_of_point_arrays, num_of_cell_arrays = point_data.GetNumberOfArrays(), cell_data.GetNumberOfArrays()
        
        if num_of_cell_arrays:
            file = File(name, reader, cell_data)
            data_arrays = [cell_data.GetArray(i).GetName() for i in range(num_of_cell_arrays)]
            scalars = cell_data.GetScalars()
        elif num_of_point_arrays:
            file = File(name, reader, point_data)
            data_arrays = [point_data.GetArray(i).GetName() for i in range(num_of_point_arrays)]
            scalars = point_data.GetScalars()
        else:
            raise Exception(const.ErrorCodes.MissingPointAndCellData)
        
        data_array = scalars.GetName() if scalars else data_arrays[0]

        if not self.add_to_matching_group(file, extent, origin, spacing, data_arrays):
            self.add_to_new_group(file, extent, origin, spacing, data_array, data_arrays)

    def add_to_matching_group(self, file: File, extent, origin, spacing, data_arrays):
        """Add file to group of files with same properties."""

        if not self.any_group():
            return False

        for group in self.__groups:
            same_extent = extent == group.extent
            same_origin = origin == group.origin
            same_spacing = spacing == group.spacing
            same_data_arrays = self.are_equal(data_arrays, group.data_arrays)

            if same_extent and same_origin and same_spacing and same_data_arrays:
                group.add_file(file)
                self.__file_to_group_mapping[file.name] = group.id
            
                return True            

        return False

    def add_to_new_group(self, file: File, extent, origin, spacing, data_array, data_arrays):
        """Add file to new group."""

        group = FileGroup(extent, origin, spacing, data_array, data_arrays)
        group.add_file(file)
        
        self.__file_to_group_mapping[file.name] = group.id
        self.__groups.append(group)

    def any_group(self):
        """Return number of file groups."""

        return len(self.__groups)

    def are_equal(self, file_data_arrays, group_data_arrays):
        """Compare two arrays and return result."""

        if len(file_data_arrays) != len(group_data_arrays):
            return False
        
        for i in range(len(file_data_arrays)):
            if file_data_arrays[i] != group_data_arrays[i]:
                return False
    
        return True

    def update(self, file_name):
        """Update information about current file."""

        if not self.any_group():
            return

        self.__current_group_id = self.__file_to_group_mapping[file_name]
        self.__current_group = self.get_group(self.__current_group_id)
        self.__current_file_index = self.__current_group.get_all_file_names().index(file_name)
        self.__current_file = self.__current_group.files[file_name]

    def get_group(self, id):
        """Return particular group based on identificator."""

        for group in self.__groups:
            if group.id == id:
                return group

    def get_all_file_names(self):
        """Return sorted file names from all groups."""

        file_names = []
        for group in self.__groups:
            file_names += group.get_all_file_names()

        return sorted(file_names)

    def delete_file(self, file_name):
        """Delete particular file from particular group."""

        group_id = self.__file_to_group_mapping[file_name]
        group = self.get_group(group_id)

        group.delete_file(file_name)
        if group.get_num_of_files() == 0:
            self.__groups.remove(group)
