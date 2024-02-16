from .czech import Czech
from .english import English

import mri_viewer.app.constants as const

class LanguageManager:
    def __init__(self):
        self._language = const.DEFAULT_LANGUAGE
        
        self._czech = Czech()
        self._english = English()

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language): 
        self._language = language

    def get_language(self):
        if self._language == const.Languages.Czech:
            return self._czech.words
        elif self._language == const.Languages.English:
            return self._english.words
        
        return None
