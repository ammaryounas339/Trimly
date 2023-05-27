# from django.core.validators import URLValidator
# from django.core.exceptions import ValidationError
# from django.test import TestCase
# #Test Cases

# def valid_url(to_validate:str) -> bool:
#     validator = URLValidator()
#     try:
#         validator(to_validate)
#         # url is valid here
#         # do something, such as:
#         return True
#     except ValidationError as exception:
#         # URL is NOT valid here.
#         # handle exception..
#         print(exception)
#         return False

from django.test import TestCase
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.test.client import Client
import urllib.request

class TrimlyTestCase(TestCase):
    
    def test_link_shortening(self):
        # Test case for link shortening functionality
        client = Client()
        response = client.post(reverse('shorten_url'), {'url': 'https://www.example.com/this-is-a-long-url-that-needs-to-be-shortened'})
        self.assertEqual(response.status_code, 200)
        # Verify that a shortened URL is generated and is valid
        self.assertTrue(response.content.decode().startswith('http'))
        self.assertIsNone(self.validate_url(response.content.decode()))

    def test_error_handling(self):
        # Test case for error handling
        client = Client()
        response = client.post(reverse('shorten_url'), {'url': 'httttttp://www.example.com'})
        self.assertEqual(response.status_code, 400)
        # Verify that an error message is displayed indicating that the URL is invalid or malformed
        self.assertEqual(response.content.decode(), 'Invalid URL')

    def validate_url(self, url):
        # Helper function to validate a URL
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError:
            return ValidationError
        return None
