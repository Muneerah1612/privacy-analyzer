from unittest import TestCase

from privacy_analyzer_helper import fetch


class HelperTest(TestCase):
    def test_fetch(self):
        tx_id = ['fa8afe02a725a16ba5fc262a9136bb7a84b5c2b35f8e6b5d8a4e110f49d88b1b']
        input_indexes = [1]

        want = [{'address': '2N6dM8W9Ri7nZnHzMWkEEw8goxwVFvJU19L', 'address_type': 'p2sh'}]
        self.assertEqual(fetch(tx_id, input_indexes), want)
