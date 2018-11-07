import unittest
from alexamd_upload import app
import requests
import bs4

class TestAlexaMDUploadBase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def index(self, ids, names, selected=None):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        soup = bs4.BeautifulSoup(response.data, "html.parser")
        for idx, option in enumerate(soup.find_all('option')):
            self.assertEqual(option.text, names[idx])
            self.assertEqual(int(option.get('value')), ids[idx])

        if selected:
            selected_options = soup.find_all('option', selected=True)
            self.assertEqual(len(selected_options), 1)
            self.assertEqual(int(selected_options[0].get('value')), selected)
