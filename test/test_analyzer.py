import unittest
import warnings

from analyzer import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

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

    def test_check_equal_amount(self):
        outputs = [
            {
                'address': 'add1',
                'amount': 10000
            },
            {
                'address': 'add2',
                'amount': 20000
            },
            {
                'address': 'add3',
                'amount': 40000
            },
            {
                'address': 'add4',
                'amount': 90000
            },
        ]

        inputs = [
            {
                'address': 'add_1',
                'amount': 20000,
                'txn_id': 'id1'
            },
            {
                'address': 'add_1',
                'amount': 50000,
                'txn_id': 'id2'
            },
            {
                'address': 'add_1',
                'amount': 30000,
                'txn_id': 'id1'
            },
            {
                'address': 'add_2',
                'amount': 30000,
                'txn_id': 'id3',
            },
            {
                'address': 'add_2',
                'amount': 20000,
                'txn_id': 'id3'

            },
            {
                'address': 'add_3',
                'amount': 10000,
                'txn_id': 'id1'
            },
        ]
        want = [{'address': 'add4', 'amount': 90000}, {'address': 'add3', 'amount': 40000}]
        self.assertEqual(check_for_equal_output(inputs, outputs), want)

    def test_check_inputs_from_same_transaction(self):
        inputs = [
            {
                'address': 'add_1',
                'amount': 20000,
                'txn_id': 'id1'
            },
            {
                'address': 'add_2',
                'amount': 50000,
                'txn_id': 'id2'
            },
            {
                'address': 'add_3',
                'amount': 30000,
                'txn_id': 'id1'
            },
            {
                'address': 'add_4',
                'amount': 30000,
                'txn_id': 'id3',
            },
            {
                'address': 'add_5',
                'amount': 20000,
                'txn_id': 'id3'

            },
            {
                'address': 'add_6',
                'amount': 10000,
                'txn_id': 'id1'
            },
        ]

        want = [
            {
                'address': 'add_1',
                'amount': 20000,
                'txn_id': 'id1'
            },
            {
                'address': 'add_3',
                'amount': 30000,
                'txn_id': 'id1'
            },
            {
                'address': 'add_4',
                'amount': 30000,
                'txn_id': 'id3',
            },
            {
                'address': 'add_5',
                'amount': 20000,
                'txn_id': 'id3'

            },
            {
                'address': 'add_6',
                'amount': 10000,
                'txn_id': 'id1'
            },
        ]

        self.assertEqual(want, check_inputs_from_same_transaction(inputs))

    def test_round_number(self):
        tx_outputs = [{'address': "213456", "amount": 2000}, {"address": "23ert", 'amount': 13456}]
        want = "23ert seem like a change address, it violates the round number privacy."
        self.assertEqual(check_for_round_number(tx_outputs), want)
