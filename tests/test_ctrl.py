from mri_viewer.app.engine import MRIViewerApp
from mri_viewer.app.files import File

# ========================================

def close_upload_files_dialog():
    app = MRIViewerApp()
    app.state.upload_files_dialog_on = True

    app.ctrl.close_upload_files_dialog()

    return app.state.upload_files_dialog_on

def test_close_upload_files_dialog_0():
    assert(close_upload_files_dialog() == False)

# ========================================

def close_manage_files_dialog():
    app = MRIViewerApp()
    app.state.manage_files_dialog_on = True

    app.ctrl.close_manage_files_dialog()

    return app.state.manage_files_dialog_on

def test_close_manage_files_dialog_0():
    assert(close_manage_files_dialog() == False)

# ========================================

def delete_file():
    app = MRIViewerApp()
    app.file_manager.add_to_new_group(
        File("file_0.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )
    app.file_manager.update("file_0.vti")
    app.state.file_to_delete = "file_0.vti"

    app.ctrl.delete_file()

    return len(app.file_manager.get_all_file_names())

def test_delete_file_0():
    assert(delete_file() == 0)

# ========================================

def toggle_player_ui(app):
    app.ctrl.toggle_player_ui()

    return app.state.ui_player_off

def test_toggle_player_ui_0():
    app = MRIViewerApp()
    app.file_manager.add_to_new_group(
        File("file_0.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )
    app.file_manager.update("file_0.vti")

    assert(toggle_player_ui(app) == True)

def test_toggle_player_ui_1():
    app = MRIViewerApp()
    app.file_manager.add_to_new_group(
        File("file_0.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        "data_array_0", ["data_array_0"],
    )
    app.file_manager.add_to_matching_group(
        File("file_1.vti", None, None),
        (0, 0, 0, 0, 0, 0), (1, 1, 1), (2, 2, 2),
        ["data_array_0"],
    )
    app.file_manager.update("file_0.vti")

    assert(toggle_player_ui(app) == False)
