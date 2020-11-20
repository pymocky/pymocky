.. role:: raw-html-m2r(raw)
   :format: html

PyMocky
=======

.. image:: https://github.com/pymocky/pymocky/workflows/Python%20package/badge.svg
   :target: https://github.com/pymocky/pymocky/workflows/Python%20package/badge.svg
   :alt: Python package



.. image:: https://codecov.io/gh/pymocky/pymocky/branch/master/graph/badge.svg?token=XCJ4YCAC5D
   :target: https://codecov.io/gh/pymocky/pymocky
   :alt: codecov



Mock server to return static response.

Install
-------

.. code-block::

   pip install pymocky


Check with command:

.. code-block::

   pymocky -h


How to use
----------

.. code-block::

   pymocky -p extras/sample/


Test with command (need curl):

.. code-block::

   curl http://localhost:9000/login


To change from default scenario to other use (server need be running):

.. code-block::

   pymocky --update-scenario "login-error"


Test again with command (need curl):

.. code-block::

   curl http://localhost:9000/login


Example of YAML file
--------------------

.. code-block::

   mappings:
   - id: hello_world
      scenario: login-success
      request:
         url: .*pymock_hello_world.*
         method: post
         query_string: .*param1=value&param2=value2
         form_fields:
         username: .*demo
         password: .*12345
         headers:
         "Content-Type": "application/json"
         body: .*Hello World.*
      response:
         headers:
         "Content-Type": "application/json"
         body_raw: Hello world from pymocky!
         body_file: files/dummy.xml
         body_json:
         success: false
         data:
            errors: []
         body_image: images/image1.png


You can use "body_raw", "body_file", "body_json" or "body_image" as response type.

.. code-block::

   body_raw: Raw text as response
   body_file: File content with mimetype discovery by extension
   body_json: Json as YAML object or string
   body_image: Image file with mimetype discovery by extension


Change scenario
---------------

To change from default scenario to other use (server need be running):

.. code-block::

   pymocky --update-scenario "login-error"


Testing
-------

You need install test dependencies with the command:

.. code-block::

   pip install -r requirements_tests.txt


To execute all tests use the command:

.. code-block::

   python -m pytest tests


To coverage test use the command:

.. code-block::

   python -m pytest --cov=. --cov-report=xml --cov-report=html tests


Packaging
---------

To package and upload for distribution on PyPi server use:

.. code-block::

   python setup.py upload


Contributing
------------


* Fork the project and clone locally.
* Create a new branch for what you're going to work on.
* Push to your origin repository.
* Create a new pull request in GitHub.

Buy me a coffee
---------------

:raw-html-m2r:`<a href='https://ko-fi.com/paulocoutinho' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi1.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>`

Supported By Jetbrains IntelliJ IDEA
------------------------------------

.. image:: extras/images/jetbrains-logo.png
   :target: extras/images/jetbrains-logo.png
   :alt: Supported By Jetbrains IntelliJ IDEA



License
-------

`MIT <http://opensource.org/licenses/MIT>`_

Copyright (c) 2020-present, Paulo Coutinho
