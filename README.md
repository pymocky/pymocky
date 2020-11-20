# PyMocky

![Python package](https://github.com/pymocky/pymocky/workflows/Python%20package/badge.svg)
[![codecov](https://codecov.io/gh/pymocky/pymocky/branch/master/graph/badge.svg?token=XCJ4YCAC5D)](https://codecov.io/gh/pymocky/pymocky)

Mock server to return static response.

## Install 

```
pip install pymocky
```

Check with command:

```
pymocky -h
```

## How to use 

```
pymocky -p extras/sample/
```

Test with command (need curl):

```
curl http://localhost:9000/login
```

To change from default scenario to other use (server need be running):

```
pymocky --update-scenario "login-error"
```

Test again with command (need curl):

```
curl http://localhost:9000/login
```

## Example of YAML file

```yaml
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
          errors: [ ]
      body_image: images/image1.png      
``` 

You can use "body_raw", "body_file", "body_json" or "body_image" as response type.

```
body_raw: Raw text as response
body_file: File content with mimetype discovery by extension
body_json: Json as YAML object or string
body_image: Image file with mimetype discovery by extension
```

## Change scenario

To change from default scenario to other use (server need be running):

```
pymocky --update-scenario "login-error"
```

## Testing 

You need install test dependencies with the command:

```
pip install -r requirements_tests.txt
```

To execute all tests use the command:

```
python -m pytest tests
```

To coverage test use the command:

```
python -m pytest --cov=. --cov-report=xml --cov-report=html tests
```

## Packaging 

To package and upload for distribution on PyPi server use:

```
python setup.py upload
```

## Contributing

- Fork the project and clone locally.
- Create a new branch for what you're going to work on.
- Push to your origin repository.
- Create a new pull request in GitHub.

## Buy me a coffee

<a href='https://ko-fi.com/paulocoutinho' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi1.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## Supported By Jetbrains IntelliJ IDEA

![Supported By Jetbrains IntelliJ IDEA](extras/images/jetbrains-logo.png "Supported By Jetbrains IntelliJ IDEA")

## License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2020-present, Paulo Coutinho
