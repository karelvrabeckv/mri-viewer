from mri_viewer.app.engine import MRIViewerApp

# ========================================

def close_upload_files_dialog():
    app = MRIViewerApp()
    app.state.upload_files_dialog_on = True

    app.ctrl.close_upload_files_dialog()

    return app.state.upload_files_dialog_on

def test_close_upload_files_dialog():
    assert(close_upload_files_dialog() == False)
