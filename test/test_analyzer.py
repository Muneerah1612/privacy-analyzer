import unittest

from analyzer import check_for_address_reuse


class MyTestCase(unittest.TestCase):
    def test_check_for_address_reuse(self):
        addresses = ['2N6dM8W9Ri7nZnHzMWkEEw8goxwVFvJU19L', '2NAsC4tV82TVznBS8F6kkJDkGuWhn1vxXRS']
        network = 'testnet'
        want = [
            {
                '2N6dM8W9Ri7nZnHzMWkEEw8goxwVFvJU19L': f"this address has been reused for 3 transactions",
                'recommendation': 'it is preferred not to use this address for privacy concerns'
            },
            {
                '2NAsC4tV82TVznBS8F6kkJDkGuWhn1vxXRS': f"this address has been reused for 5 transactions",
                'recommendation': 'it is preferred not to use this address for privacy concerns'
            }
        ]

        self.assertEqual(check_for_address_reuse(addresses, network), want)
