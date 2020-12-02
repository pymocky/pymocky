.. image:: https://github.com/pymocky/pymocky/raw/master/extras/images/logo.png
   :target: https://github.com/pymocky/pymocky
   :alt: PyMocky
   :height: 100

|

.. image:: https://github.com/pymocky/pymocky/workflows/Python%20package/badge.svg
   :target: https://github.com/pymocky/pymocky/workflows/Python%20package/badge.svg
   :alt: Python package



.. image:: https://codecov.io/gh/pymocky/pymocky/branch/master/graph/badge.svg?token=XCJ4YCAC5D
   :target: https://codecov.io/gh/pymocky/pymocky
   :alt: codecov

|  

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
         url: .*pymocky_hello_world.*
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
         body_python: files/dummy.py


You can use "body_raw", "body_file", "body_json", "body_image" or "body_python" as response type.

.. code-block::

   body_raw: Raw text as response
   body_file: File content with mimetype discovery by extension
   body_json: Json as YAML object or string
   body_image: Image file with mimetype discovery by extension
   body_python: Python file to be executed


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


To install locally during development:

.. code-block::

   python setup.py install


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

.. image:: https://az743702.vo.msecnd.net/cdn/kofi1.png?v=2
   :target: https://ko-fi.com/paulocoutinho
   :alt: Buy Me a Coffee at ko-fi.com
   :height: 40


Supported By Jetbrains IntelliJ IDEA
------------------------------------

.. image:: https://github.com/pymocky/pymocky/raw/master/extras/images/jetbrains-logo.png
   :target: https://www.jetbrains.com/
   :alt: Supported By Jetbrains IntelliJ IDEA


License
-------

`MIT <http://opensource.org/licenses/MIT>`_

Copyright (c) 2020-present, Paulo Coutinho
