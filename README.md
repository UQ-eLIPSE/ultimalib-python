# ULTIMA Python Bindings
This module contains a thin wrapper around the ULTIMA service which allows for
cross-platform LTI validation.

## Dependencies
* [requests](https://github.com/requests/requests)

## Usage
`pip install https://github.com/UQ-eLIPSE/ultimalib-python/archive/v1.0.0.zip`

To track the package in your `requirements.txt` file; simply paste the github archive URL in it like so:

```bash
cat requirements.txt
urllib3==1.22
https://github.com/UQ-eLIPSE/ultimalib-python/archive/v1.0.0.zip
beautifulsoup4==4.6.0
```

## Tests
`tox` is used as a test runner for this library. It is configured to run tests for py27, py35 and py36.

```
pip install tox
tox
```

## Usage
```
from ultima_lib import LTIValidator, LTIValidatorException

LTI_LISTEN_LOCATION = "https://localhost:8000/lti"

def handle_request(request):
    """
        request contains some LTI payload you just received in your application
    """

    app_key = "some_long_unique_string_unique_to_this_application"
    ultima_service_uri = "https://location_of_ultima_service.net/"

    lti_validator = LTIValidator(ultima_service_uri, app_key)

    http_method = request.method # Will be "POST", since we are only listening on the POST endpoint
    try:
        status, result = lti_validator.validate_request(LTI_LISTEN_LOCATION, http_method, request.POST)
        return print("Request is valid and can be trusted")
    except LTIValidatorException as e:
        return print("Request failed:", e.message, "|", e.status_code)

# router is an imaginary application router.
#   For purposes of this is makes the handle_lti_request function handle all POST requests which are directed at LTI_LISTEN_LOCATION
router.on(LTI_LISTEN_LOCATION, "POST", handle_lti_request)
```

## Architecture
This module is fairly straightforward, it forwards any LTI request to a secure endpoint which contains a record of the `oauth_consumer_key` and the `secret_key`. This remote endpoint then validates the request, and returns a simple response indicating its validity.

`LTIValidator`
A class which handles the plumbing of the LTI validation. It is given a ULTIMA service URI and an `app_key`. The user then only needs to call the `validate_request` method with a forwarded LTI payload to determine the validity of it.

`LTIValidatorException`
An exception thrown when the server returns a not-good error code about the LTI response. The exception exposes the following data:

    * message<string> - The error message the ULTIMA server responded with
    * status_code<int> - The HTTP status code the ULTIMA server responded with
    * errors<dict> - The response body the ULTIMA service responded with


## Developing
To make improvements to this package, the following is required:

    * A python environment
    * [pandoc](https://pandoc.org/installing.html) is used to convert this README.md into `reStructuredText` when publishing to pypi
        1. First: pip install pypandoc
        2. Second: Download installer from pandoc website
