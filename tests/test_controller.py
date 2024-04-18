from mri_viewer.app.engine import MRIViewerApp

# ========================================

def close_dialog():
    app = MRIViewerApp()
    app.state.dialog_on = True

    app.ctrl.close_dialog()

    return app.state.dialog_on

def test_close_dialog():
    assert(close_dialog() == False)
