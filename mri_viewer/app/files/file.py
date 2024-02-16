class File:
    @property
    def name(self):
        return self._name

    @name.setter 
    def name(self, name): 
        self._name = name

    @property
    def reader(self):
        return self._reader

    @reader.setter 
    def reader(self, reader): 
        self._reader = reader

    @property
    def data(self):
        return self._data 

    @data.setter 
    def data(self, data): 
        self._data = data

    @property
    def data_array(self):
        return self._data_array

    @data_array.setter 
    def data_array(self, data_array): 
        self._data_array = data_array

    @property
    def data_arrays(self):
        return self._data_arrays
    
    @data_arrays.setter 
    def data_arrays(self, data_arrays): 
        self._data_arrays = data_arrays 
