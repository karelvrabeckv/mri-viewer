from mri_viewer.app.files import File, FileGroup, FileManager

import mri_viewer.app.constants as const

# ========================================

def upload_file_from_url(url):
    return FileManager().upload_file_from_url(url)

def test_upload_file_from_url_0():
    try:
        upload_file_from_url("https://www.some-random-url.com/")
    except Exception as e:
        assert(str(e) == const.ErrorCodes.InvalidURL)

# ========================================

def validate_files(files_from_pc):
    return FileManager().validate_files(files_from_pc)

def test_validate_files_0():
    try:
        files_from_pc = []
        validate_files(files_from_pc)
    except Exception as e:
        assert(str(e) == const.ErrorCodes.NoFilesToUpload)

def test_validate_files_1():
    try:
        files_from_pc = []
        for i in range(11):
            files_from_pc.append(File("file_" + str(i) + ".vti", None, None))
        validate_files(files_from_pc)
    except Exception as e:
        assert(str(e) == const.ErrorCodes.TooManyFilesToUpload)

# ========================================

def validate_file(file_name, file_content, file_size):
    return FileManager().validate_file(file_name, file_content, file_size)

def test_validate_file_0():
    try:
        validate_file("test.txt", "text", 4)
    except Exception as e:
        assert(str(e) == const.ErrorCodes.WrongFileExtension)

def test_validate_file_1():
    try:
        validate_file("test.vti", "", 0)
    except Exception as e:
        assert(str(e) == const.ErrorCodes.EmptyFile)
    
def test_validate_file_2():
    try:
        validate_file("test.vti", "<very long text>", 100_000_001)
    except Exception as e:
        assert(str(e) == const.ErrorCodes.FileIsTooLarge)

# ========================================

def validate_response(headers, content_disposition, content_length, content):
    return FileManager().validate_response(headers, content_disposition, content_length, content)

def test_validate_response_0():
    try:
        validate_response({}, "", "", "")
    except Exception as e:
        assert(str(e) == const.ErrorCodes.MissingHeaders)

def test_validate_response_1():
    try:
        validate_response({"key1": "value1"}, "", "text", "text")
    except Exception as e:
        assert(str(e) == const.ErrorCodes.MissingContentDispositionHeader)

def test_validate_response_2():
    try:
        validate_response({"key1": "value1"}, "text", "", "text")
    except Exception as e:
        assert(str(e) == const.ErrorCodes.MissingContentLengthHeader)

def test_validate_response_3():
    try:
        validate_response({"key1": "value1"}, "text", "text", "")
    except Exception as e:
        assert(str(e) == const.ErrorCodes.MissingContent)

# ========================================

def add_to_matching_group(file_manager: FileManager, file, extent, origin, spacing, data_arrays):
    return file_manager.add_to_matching_group(file, extent, origin, spacing, data_arrays)

def test_add_to_matching_group_0():
    file_manager = FileManager()

    assert(add_to_matching_group(
        file_manager,
        File("file_0.vti", None, None),
        (0, 0, 0), (1, 1, 1), (2, 2, 2),
        ["data_array_0"]
    ) == False)

def test_add_to_matching_group_1():
    file_manager = FileManager()
    file_manager.add_to_new_group(
        File("file_0.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )

    assert(add_to_matching_group(
        file_manager,
        File("file_1.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        ["data_array_0"],
    ) == True)

def test_add_to_matching_group_2():
    file_manager = FileManager()
    file_manager.add_to_new_group(
        File("file_0.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )

    assert(add_to_matching_group(
        file_manager,
        File("file_1.vti", None, None),
        (0, 0, 0, 0, 0, 0), (0, 0, 0), (0, 0, 0),
        ["data_array_0"],
    ) == False)

# ========================================

def any_group(file_manager: FileManager):
    return file_manager.any_group()

def test_any_group_0():
    assert(any_group(FileManager()) == 0)

def test_any_group_1():
    file_manager = FileManager()
    file_manager.add_to_new_group(
        File("file_0.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )

    assert(any_group(file_manager) != 0)

# ========================================

def are_equal(first_list, second_list):
    return FileManager().are_equal(first_list, second_list)

def test_are_equal_0():
    assert(are_equal(["one", "two", "three", "four"], ["one", "two", "three"]) == False)

def test_are_equal_1():
    assert(are_equal(["one", "two", "three", "four"], ["five", "three", "two", "one"]) == False)

def test_are_equal_2():
    assert(are_equal(["one", "two", "three", "four"], ["one", "two", "three", "four"]) == True)

# ========================================

def update(file_manager: FileManager, file_name):
    return file_manager.update(file_name)

def test_update_0():
    file_manager = FileManager()
    file_manager.add_to_new_group(
        File("file_0.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )

    update(file_manager, "file_0.vti")

    assert(file_manager.current_file_index == 0)

# ========================================

def get_all_manager_file_names(file_manager: FileManager):
    return file_manager.get_all_file_names()

def test_get_all_manager_file_names_0():
    file_manager = FileManager()
    file_manager.add_to_new_group(
        File("some_file.vti", None, None),
        (0, 0, 0, 0, 0, 0), (0, 0, 0), (0, 0, 0),
        "data_array_0", ["data_array_0"],
    )
    file_manager.add_to_new_group(
        File("another_file.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )

    assert(get_all_manager_file_names(file_manager) == ["another_file.vti", "some_file.vti"])

# ========================================

def delete_manager_file(file_manager: FileManager, file_name):
    return file_manager.delete_file(file_name)

def test_delete_manager_file_0():
    file_manager = FileManager()
    file_manager.add_to_new_group(
        File("file_0.vti", None, None),
        (0, 0, 0, 0, 0, 0), (0, 0, 0), (0, 0, 0),
        "data_array_0", ["data_array_0"],
    )
    file_manager.add_to_new_group(
        File("file_1.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )

    delete_manager_file(file_manager, "file_1.vti")

    assert(file_manager.any_group() == 1)

# ========================================

def get_num_of_files(group: FileGroup):
    return group.get_num_of_files()

def test_get_num_of_files_0():
    group = FileGroup(
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"]
    )
    group.add_file(File("file_0.vti", None, None))

    assert(get_num_of_files(group) == 1)

# ========================================

def get_all_group_file_names(group: FileGroup):
    return group.get_all_file_names()

def test_get_all_group_file_names_0():
    group = FileGroup(
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"]
    )
    group.add_file(File("file_0.vti", None, None))

    assert(get_all_group_file_names(group) == ["file_0.vti"])

# ========================================

def get_min_slice_position(group: FileGroup, orientation):
    return group.get_min_slice_position(orientation)

def test_get_min_slice_position_0():
    group = FileGroup(
        (0, 1, 2, 3, 4, 5), (10, 11, 12), (20, 21, 22),
        "data_array_0", ["data_array_0"]
    )
    group.add_file(File("file_0.vti", None, None))

    assert(get_min_slice_position(group, const.Planes.XY) == 100)
    assert(get_min_slice_position(group, const.Planes.YZ) == 10)
    assert(get_min_slice_position(group, const.Planes.XZ) == 53)

# ========================================

def get_max_slice_position(group: FileGroup, orientation):
    return group.get_max_slice_position(orientation)

def test_get_max_slice_position_0():
    group = FileGroup(
        (0, 1, 2, 3, 4, 5), (10, 11, 12), (20, 21, 22),
        "data_array_0", ["data_array_0"]
    )
    group.add_file(File("file_0.vti", None, None))

    assert(get_max_slice_position(group, const.Planes.XY) == 122)
    assert(get_max_slice_position(group, const.Planes.YZ) == 30)
    assert(get_max_slice_position(group, const.Planes.XZ) == 74)

# ========================================

def get_slice_step(group: FileGroup, orientation):
    return group.get_slice_step(orientation)

def test_get_slice_step_0():
    group = FileGroup(
        (0, 1, 2, 3, 4, 5), (10, 11, 12), (20, 21, 22),
        "data_array_0", ["data_array_0"]
    )
    group.add_file(File("file_0.vti", None, None))

    assert(get_slice_step(group, const.Planes.XY) == 22)
    assert(get_slice_step(group, const.Planes.YZ) == 20)
    assert(get_slice_step(group, const.Planes.XZ) == 21)

# ========================================

def add_file(group: FileGroup, file):
    return group.add_file(file)

def test_add_file_0():
    group = FileGroup(
        (0, 1, 2, 3, 4, 5), (10, 11, 12), (20, 21, 22),
        "data_array_0", ["data_array_0"]
    )
    add_file(group, File("file_0.vti", None, None))

    assert(group.get_num_of_files() == 1)

# ========================================

def delete_group_file(group: FileGroup, file_name):
    return group.delete_file(file_name)

def test_delete_group_file_0():
    group = FileGroup(
        (0, 1, 2, 3, 4, 5), (10, 11, 12), (20, 21, 22),
        "data_array_0", ["data_array_0"]
    )
    add_file(group, File("file_0.vti", None, None))
    delete_group_file(group, "file_0.vti")

    assert(group.get_num_of_files() == 0)
