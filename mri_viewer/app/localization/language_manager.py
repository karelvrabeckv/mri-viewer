from .czech import Czech
from .english import English

from ..constants import Languages, DEFAULT_LANGUAGE

class LanguageManager:
    def __init__(self):
        self._language = DEFAULT_LANGUAGE
        
        self._czech = Czech()
        self._english = English()

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language): 
        self._language = language

    def get_language(self):
        if self._language == Languages.Czech:
            return self._czech.words
        elif self._language == Languages.English:
            return self._english.words
        
        return None
