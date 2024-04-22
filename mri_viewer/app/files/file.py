class File:
    """Class representing single file."""

    def __init__(self, name, reader, data):
        self.__name = name
        self.__reader = reader
        self.__data = data
    
    @property
    def name(self):
        return self.__name

    @property
    def reader(self):
        return self.__reader

    @property
    def data(self):
        return self.__data 
