import requests


# d
def fetch(transaction_ids, output_indexes):
    transactions = []

    for index, txn_id in enumerate(transaction_ids):
        transaction_request = requests.Session().get(
            url=f"https://blockstream.info/testnet/api/tx/{txn_id}")

        vout = transaction_request.json()["vout"]

        vout_info = {"address": vout[output_indexes[index]]['scriptpubkey_address'],
                     "address_type": vout[output_indexes[index]]['scriptpubkey_type']}

        transactions.append(vout_info)

    return transactions
