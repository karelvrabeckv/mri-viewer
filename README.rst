==========
MRI Viewer
==========

A web application for analyzing and visualizing VTI files.

Created for `the Institute for Clinical and Experimental Medicine <https://www.ikem.cz/en/>`_ in Prague, Czech Republic.

Powered by *Trame*, *VTK*, and *Vuetify*.

.. list-table::

   * - .. image:: assets/aorta.png
     - .. image:: assets/brain.png

Features
--------

* **Upload**, **manage**, and **render** *.vti* files
* **Slice** data in different orientations and positions
* **Pick** points and cells to see the values of data arrays in them
* **Zoom**, **translate**, and **rotate** data
* **Play** sequences of *.vti* files
* Switch between **files**
* Switch between **data arrays**
* Switch between **representations** (*points*, *slice*, *surface*, *surface with edges*, and *wireframe*)
* Switch between **color maps** (*cool to warm* and *grayscale*)
* Switch between **languages** (Czech and English only)
* Switch between **dark and light themes**
* Read the **user guide** directly in the web application
* and more...

Docs
----

*User documentation* is available `here <mri_viewer/app/docs/user_guide_en.pdf>`_.

*Technical documentation* is available `here <thesis.pdf>`_.

Installing
----------

1. Create a virtual environment:

.. code-block:: console

    python -m venv .venv

2. Activate the virtual environment:

.. code-block:: console

    source ./.venv/Scripts/activate

3. Install packages:

.. code-block:: console

    pip install -e .

Running
-------

1. Run as a web application:

.. code-block:: console

    mri-viewer

2. Run as a desktop application:

.. code-block:: console

    mri-viewer --app

3. Run in JupyterLab:

.. code-block:: console

    pip install -r ./jupyter/requirements.txt
    jupyter-lab

Docker
------

1. Build the image:

.. code-block:: console

    docker build -t mri-viewer .

2. Run the Docker container:

.. code-block:: console

    docker run -it --rm -p 8080:80 -v mri-viewer-deploy:/deploy mri-viewer

Instead of creating a named volume with ``-v mri-viewer-deploy:/deploy``, you
can mount the ``./docker`` directory from the git repository to ``/deploy`` in
the container using ``-v ./docker:/deploy``.

3. Open the web application in your browser: http://localhost:8080
