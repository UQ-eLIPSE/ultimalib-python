import unittest
import requests
from requests import Response
import mock
from ultima_lib import LTIValidator, LTIValidatorException

MOCK_REMOTE_ENDPOINT = "mock://validate/lti/"
MOCK_LTI_LAUNCH = "https://localhost:9000/lti/"
MOCK_APP_KEY = "1"
MOCK_INCOMING_LTI_REQUEST = {
    "oauth_consumer_key": "34",
    "oauth_timestamp": "213"
}

MOCK_DATA = {
    "appKey": MOCK_APP_KEY,
    "uri": MOCK_LTI_LAUNCH,
    "method": "POST",
    "payload": MOCK_INCOMING_LTI_REQUEST
}


class TestLTIValidator(unittest.TestCase):

    def test_good_request(self):
        return_value = Response()
        return_value.status_code = 200
        return_value.json = mock.MagicMock(return_value={
            "valid": True
        })

        requests.post = mock.MagicMock(return_value=return_value)

        validator = LTIValidator(MOCK_REMOTE_ENDPOINT, MOCK_APP_KEY)

        response_code, response_object = validator.validate_request(
            MOCK_LTI_LAUNCH, "POST", MOCK_INCOMING_LTI_REQUEST)
        requests.post.assert_called_with(
            MOCK_REMOTE_ENDPOINT, json=MOCK_DATA)

        self.assertEqual(response_code, 200)
        self.assertEqual(response_object, {
            "valid": True
        })

    def test_throws_json_value_error(self):
        with self.assertRaises(LTIValidatorException) as cm:
            return_value = Response()
            requests.post = mock.MagicMock(return_value=return_value)
            return_value.status_code = 400
            return_value.json = mock.side_effect = mock.Mock(
                side_effect=ValueError("no response in JSON body"))

            validator = LTIValidator(MOCK_REMOTE_ENDPOINT, MOCK_APP_KEY)

            response_code, response_object = validator.validate_request(
                MOCK_LTI_LAUNCH, "POST", MOCK_INCOMING_LTI_REQUEST)

        self.assertEqual("no response in JSON body", cm.exception.message)
        self.assertEqual(400, cm.exception.status_code)

    def test_throws_post_LTIException(self):
        with self.assertRaises(LTIValidatorException) as cm:
            return_value = Response()
            requests.post = mock.Mock(
                side_effect=LTIValidatorException(
                    ["Could not find endpoint", 400], {}))

            validator = LTIValidator(MOCK_REMOTE_ENDPOINT, MOCK_APP_KEY)

            response_code, response_object = validator.validate_request(
                MOCK_LTI_LAUNCH, "POST", MOCK_INCOMING_LTI_REQUEST)

        self.assertEqual("Could not find endpoint", cm.exception.message)
        self.assertEqual(400, cm.exception.status_code)

    def test_exception(self):
        with self.assertRaises(LTIValidatorException) as cm:
            return_value = Response()
            return_value.status_code = 400
            return_value.json = mock.MagicMock(return_value={
                "error": "Bad request",
                "valid": False
            })
            requests.post = mock.MagicMock(return_value=return_value)

            validator = LTIValidator(MOCK_REMOTE_ENDPOINT, MOCK_APP_KEY)

            response_code, response_object = validator.validate_request(
                MOCK_LTI_LAUNCH, "POST", MOCK_INCOMING_LTI_REQUEST)
            requests.post.assert_called_with(MOCK_REMOTE_ENDPOINT, json=MOCK_DATA)

        self.assertEqual("Bad request", cm.exception.message)
        self.assertEqual(400, cm.exception.status_code)

    def test_nonstandard_server(self):
        with self.assertRaises(LTIValidatorException) as cm:
            return_value = Response()
            return_value.status_code = 400
            return_value.json = mock.MagicMock(return_value={})
            requests.post = mock.MagicMock(return_value=return_value)

            validator = LTIValidator(MOCK_REMOTE_ENDPOINT, MOCK_APP_KEY)

            response_code, response_object = validator.validate_request(
                MOCK_LTI_LAUNCH, "POST", MOCK_INCOMING_LTI_REQUEST)
            requests.post.assert_called_with(MOCK_REMOTE_ENDPOINT, json=MOCK_DATA)

        self.assertEqual(
            "Server has not provided an error message", cm.exception.message)
        self.assertEqual(400, cm.exception.status_code)
