class File:
    def __init__(self, name, reader, extent, data, data_array, data_arrays):
        self.__name = name
        self.__reader = reader
        self.__extent = extent
        self.__data = data
        self.__data_array = data_array
        self.__data_arrays = data_arrays
    
    @property
    def name(self):
        return self.__name

    @property
    def reader(self):
        return self.__reader

    @property
    def extent(self):
        return self.__extent

    @property
    def data(self):
        return self.__data 

    @property
    def data_array(self):
        return self.__data_array

    @property
    def data_arrays(self):
        return self.__data_arrays
