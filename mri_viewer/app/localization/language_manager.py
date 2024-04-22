from .czech import Czech
from .english import English

import mri_viewer.app.constants as const

class LanguageManager:
    """Class representing manager of languages."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            # Create only one instance of this class
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__language = const.DEFAULT_LANGUAGE
        
        self.__czech = Czech()
        self.__english = English()

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, language): 
        self.__language = language

    def get_language(self):
        """Return vocabulary of particular language."""

        if self.__language == const.Languages.Czech:
            return self.__czech.words
        elif self.__language == const.Languages.English:
            return self.__english.words

    def get_user_guide_url(self):
        """Return user guide of particular language."""

        if self.__language == const.Languages.Czech:
            return const.USER_GUIDE_CZ_URL
        elif self.__language == const.Languages.English:
            return const.USER_GUIDE_EN_URL
