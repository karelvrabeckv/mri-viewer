from mri_viewer.app.files import FileManager

import mri_viewer.app.constants as const

# ========================================

def are_equal(first_list, second_list):
    return FileManager().are_equal(first_list, second_list)

def test_are_equal_0():
    assert(are_equal(["one", "two", "three", "four"], ["one", "two", "three"]) == False)

def test_are_equal_1():
    assert(are_equal(["one", "two", "three", "four"], ["five", "three", "two", "one"]) == False)

def test_are_equal_2():
    assert(are_equal(["one", "two", "three", "four"], ["four", "three", "two", "one"]) == True)

# ========================================

def validate_file(file_name, file_content, file_size):
    return FileManager().validate_file(file_name, file_content, file_size)

def test_validate_file_0():
    try:
        validate_file("test.txt", "text", 4)
    except Exception as e:
        assert(str(e) == const.ErrorCodes.WrongFileExtension)
    else:
        assert False

def test_validate_file_1():
    try:
        validate_file("test.vti", "", 0)
    except Exception as e:
        assert(str(e) == const.ErrorCodes.EmptyFile)
    else:
        assert False
    
def test_validate_file_2():
    try:
        validate_file("test.vti", "<very long text>", 100_000_001)
    except Exception as e:
        assert(str(e) == const.ErrorCodes.FileIsTooLarge)
    else:
        assert False
