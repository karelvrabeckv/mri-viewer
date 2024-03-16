==========
MRI Viewer
==========

A web application for visualizing and viewing MRI outputs

* Free software: MIT License

Installing
----------

Install the application:

.. code-block:: console

    pip install -e .

Run the application:

.. code-block:: console

    mri-viewer
    mri-viewer --app
    jupyter-lab

Features
--------

* TBA

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

3. Open the application in your web browser: http://localhost:8080
