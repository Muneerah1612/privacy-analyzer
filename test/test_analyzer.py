import unittest

from analyzer import check_for_address_reuse, check_for_largest_amount_address, check_for_round_number


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

    def test_check_largest_input_address(self):
        outputs = [
            {
                'address': 'add1',
                'amount': 903
            },
            {
                'address': 'add2',
                'amount': 800
            },
            {
                'address': 'add3',
                'amount': 570
            },
            {
                'address': 'add4',
                'amount': 9000
            },
            {
                'address': 'add5',
                'amount': 876
            },
        ]
        want = {'address': {'add4': 9000}, 'message': 'this a likely a change address'}
        self.assertEqual(check_for_largest_amount_address(outputs), want)

    def test_round_number(self):
        tx_outputs = [{'address': "213456", "amount": 2000}, {"address": "23ert", 'amount': 13456}]
        want = "23ert seem like a change address, it violates the round number privacy."
        self.assertEqual(check_for_round_number(tx_outputs), want)
