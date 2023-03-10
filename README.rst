###############################################################################
                            SIMPLE MESSAGE APPLICATION
###############################################################################

This is a training project.
This is done using the `Flask`_ framework and demonstrates its abilities.

.. _Python training course: https://github.com/shorodilov/python-course.git
.. _Flask: https://flask.palletsprojects.com/

Getting started
===============

#. Download the code base
#. Install the dependencies
#. Setup environment variables
#. Run the project

Preparing
===============
You may prefer to use virtual environment to separate the project's
dependencies from other packages you have installed on your local machine.
This project comes with dependencies files suitable both for `pip`_
Aditionaly you need to start `docker-compose`_ containers with `postgres`_ database, and make initialisation.

.. code-block::

    docker-compose up -d

To install the requirements use one of the commands below:

.. code-block::

    pip install -r requirements.txt

After docker starts:


.. code-block::

    flask db init
    flask db migrate -m "first start"
    flask db upgrade

.. _postgres: https://www.postgresql.org/docs/
.. _docker-compose: https://docs.docker.com/compose/
.. _pip: https://pypi.org/project/pip/

Environment variables
=====================
You need to set environment variables for database:

.. code-block::

    FLASK_DEBUG=0 (or 1 for debugging mode)
    DEVELOPMENT_DATABASE_URI=postgresql://user:password@localhost/
    PRODUCTION_DATABASE_URI=postgresql://user:password@localhost/
    SECRET_KEY=your_secret_key

You can find DB user,password and host from docker-compose.yaml