import requests

TESTNET_URL = 'https://blockstream.info/testnet/api'


def fetch_transaction(transaction_ids, output_indexes, network='testnet'):
    network_url = ''
    if network == 'testnet':
        network_url = TESTNET_URL

    transactions = []
    for index, txn_id in enumerate(transaction_ids):
        transaction_request = requests.Session().get(
            url=f"{network_url}/tx/{txn_id}")

        vout = transaction_request.json()["vout"]

        vout_info = {"address": vout[output_indexes[index]]['scriptpubkey_address'],
                     "address_type": vout[output_indexes[index]]['scriptpubkey_type']}

        transactions.append(vout_info)

    return transactions


def get_address_transaction_count(address, network='testnet'):
    network_url = ''
    if network == 'testnet':
        network_url = TESTNET_URL

    address_info = requests.Session().get(
        url=f"{network_url}/address/{address}")

    address_tx_count = address_info.json()['chain_stats']['tx_count'] + address_info.json()['mempool_stats'][
        'tx_count']

    return address_tx_count
