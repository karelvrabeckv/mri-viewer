python -m PyInstaller ^
  --hidden-import pkgutil ^
  --windowed ^
  --collect-data trame_vuetify ^
  --collect-data trame_vtk ^
  --collect-data trame_client ^
  .\run.py
