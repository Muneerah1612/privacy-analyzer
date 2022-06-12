from unittest import TestCase

from analyzer import *
from privacy_analyzer_helper import fetch_transaction, get_address_transaction_count


class HelperTest(TestCase):
    def test_fetch_transactions(self):

        tx_id = ['fa8afe02a725a16ba5fc262a9136bb7a84b5c2b35f8e6b5d8a4e110f49d88b1b']
        input_indexes = [1]

        want = [{'address': '2N6dM8W9Ri7nZnHzMWkEEw8goxwVFvJU19L', 'address_type': 'p2sh'}]

        self.assertEqual(fetch_transaction(tx_id, input_indexes), want)

    def test_round_number(self):
        tx_outputs = [{'address': "213456", "amount": 2000}, {"address": "23ert", 'amount': 13456}]
        want = "23ert seem like a change address, it violates the round number privacy."
        self.assertEqual(check_for_round_number(tx_outputs), want)

    def test_get_address_transaction_count(self):
        address = '2N6dM8W9Ri7nZnHzMWkEEw8goxwVFvJU19L'
        want = 3
        self.assertEqual(get_address_transaction_count(address), want)

