class File:
    @property
    def name(self):
        return self.__name

    @name.setter 
    def name(self, name): 
        self.__name = name

    @property
    def reader(self):
        return self.__reader

    @reader.setter 
    def reader(self, reader): 
        self.__reader = reader

    @property
    def data(self):
        return self.__data 

    @data.setter 
    def data(self, data): 
        self.__data = data

    @property
    def data_array(self):
        return self.__data_array

    @data_array.setter 
    def data_array(self, data_array): 
        self.__data_array = data_array

    @property
    def data_arrays(self):
        return self.__data_arrays
    
    @data_arrays.setter 
    def data_arrays(self, data_arrays): 
        self.__data_arrays = data_arrays 
