import unittest
from alexamd_upload import app
import requests
import bs4
from test_base import TestAlexaMDUploadBase

class TestIndex(TestAlexaMDUploadBase):
    def test_default(self):
        ids = [1, 2, 3, 4]
        names = ['w, alyssa', 's, anthony', 'y, derek', 'w, mike']
        self.index(ids, names)

    def test_select(self):
        response = self.app.post('/', data=dict(patient=2))
        self.assertEqual(response.status_code, 200)

        ids = [1, 2, 3, 4]
        names = ['w, alyssa', 's, anthony', 'y, derek', 'w, mike']
        self.index(ids, names, selected=2)
