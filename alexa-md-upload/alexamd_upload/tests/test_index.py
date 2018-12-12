import unittest
from alexamd_upload import app
import requests
import bs4
from test_base import TestAlexaMDUploadBase
from mock import patch

class TestIndex(TestAlexaMDUploadBase):
    def test_default(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        list_values = [ 's, anthony',
                    'w, alyssa',
                    'w, mike',
                    'y, derek']

        soup = bs4.BeautifulSoup(response.data, "html.parser")
        list_items = soup.find_all('li')
        self.assertEqual(len(list_items), len(list_values))
        for li in list_items:
            name = li.text.strip().split('\n')
            self.assertTrue(len(name) > 1)
            self.assertIn(name[0], list_values)
