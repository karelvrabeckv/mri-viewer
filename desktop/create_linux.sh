#!/bin/bash

python -m PyInstaller \
    --name "mri_viewer" \
    --icon icon.ico \
    --onefile \
    --clean \
    --noconfirm \
    --add-data "../mri_viewer/app/assets/logo.png:mri_viewer/app/assets" \
    --hidden-import vtkmodules.vtkCommonMath \
    --hidden-import vtkmodules.vtkCommonMisc \
    --hidden-import vtkmodules.vtkCommonExecutionModel \
    --hidden-import vtkmodules.vtkFiltersCore \
    --hidden-import vtkmodules.vtkFiltersGeneral \
    --hidden-import vtkmodules.vtkFiltersSources \
    --hidden-import vtkmodules.vtkRenderingContext2D \
    --hidden-import vtkmodules.vtkRenderingHyperTreeGrid \
    --hidden-import vtkmodules.vtkRenderingUI \
    --hidden-import vtkmodules.vtkIOImage \
    --hidden-import vtkmodules.vtkIOXMLParser \
    --collect-data trame_vtk \
    --collect-data trame_client \
    --collect-data trame_vuetify \
    --collect-data trame_components \
    ../run.py
