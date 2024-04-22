from .file import File

from collections import OrderedDict
from uuid import uuid4

import mri_viewer.app.constants as const

class FileGroup:
    """Class representing group of similar files."""

    def __init__(self, extent, origin, spacing, data_array, data_arrays):
        self.__id = uuid4()
        self.__files = dict()
        
        self.__default_view = None
        self.__current_view = None
        
        self.__extent = extent
        self.__origin = origin
        self.__spacing = spacing
        self.__data_array = data_array
        self.__data_arrays = data_arrays
        
        self.__representation = const.DEFAULT_REPRESENTATION
        self.__color_map = const.DEFAULT_COLOR_MAP
        
        self.__slice_orientation = const.DEFAULT_SLICE_ORIENTATION
        self.__slice_position = {
            const.Planes.XY: self.get_min_slice_position(const.Planes.XY),
            const.Planes.YZ: self.get_min_slice_position(const.Planes.YZ),
            const.Planes.XZ: self.get_min_slice_position(const.Planes.XZ),
        }

    @property
    def id(self):
        return self.__id

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

    @property
    def origin(self):
        return self.__origin

    @property
    def spacing(self):
        return self.__spacing

    @property
    def data_array(self):
        return self.__data_array

    @data_array.setter
    def data_array(self, data_array): 
        self.__data_array = data_array

    @property
    def data_arrays(self):
        return self.__data_arrays

    @property
    def representation(self):
        return self.__representation
    
    @representation.setter
    def representation(self, representation): 
        self.__representation = representation

    @property
    def color_map(self):
        return self.__color_map
    
    @color_map.setter
    def color_map(self, color_map): 
        self.__color_map = color_map

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
        """Return number of files in group."""

        return len(self.__files)
    
    def get_all_file_names(self):
        """Return names of files in group."""

        return list(self.__files)

    def get_min_slice_position(self, orientation):
        """Return minimum slice position for particular slice orientation."""

        min_x, _, min_y, _, min_z, _ = self.__extent
        origin_x, origin_y, origin_z = self.__origin
        space_x, space_y, space_z = self.__spacing
        
        if orientation == const.Planes.XY:
            return space_z * min_z + origin_z
        elif orientation == const.Planes.YZ:
            return space_x * min_x + origin_x
        elif orientation == const.Planes.XZ:
            return space_y * min_y + origin_y

    def get_max_slice_position(self, orientation):
        """Return maximum slice position for particular slice orientation."""

        _, max_x, _, max_y, _, max_z = self.__extent
        origin_x, origin_y, origin_z = self.__origin
        space_x, space_y, space_z = self.__spacing
        
        if orientation == const.Planes.XY:
            return space_z * max_z + origin_z
        elif orientation == const.Planes.YZ:
            return space_x * max_x + origin_x
        elif orientation == const.Planes.XZ:
            return space_y * max_y + origin_y

    def get_slice_step(self, orientation):
        """Return slice step for particular slice orientation."""

        space_x, space_y, space_z = self.__spacing
        
        if orientation == const.Planes.XY:
            return space_z
        elif orientation == const.Planes.YZ:
            return space_x
        elif orientation == const.Planes.XZ:
            return space_y

    def add_file(self, file: File):
        """Add new file to group."""

        self.__files[file.name] = file

        # Sort group for player
        self.__files = OrderedDict(sorted(self.__files.items()))

    def delete_file(self, file_name):
        """Delete file from group."""

        del self.__files[file_name]
