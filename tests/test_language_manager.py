from mri_viewer.app.localization import (
    LanguageManager,
    Czech,
    English,
)

import mri_viewer.app.constants as const

# ========================================

def get_language(language):
    language_manager = LanguageManager()
    language_manager.language = language

    return language_manager.get_language()

def test_get_language_0():
    assert(get_language(const.Languages.Czech) == Czech().words)

def test_get_language_1():
    assert(get_language(const.Languages.English) == English().words)

# ========================================

def get_user_guide_url(language):
    language_manager = LanguageManager()
    language_manager.language = language

    return language_manager.get_user_guide_url()

def test_get_user_guide_url_0():
    assert(get_user_guide_url(const.Languages.Czech) == const.CZ_USER_GUIDE_URL)

def test_get_user_guide_url_1():
    assert(get_user_guide_url(const.Languages.English) == const.EN_USER_GUIDE_URL)
