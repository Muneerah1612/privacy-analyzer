from privacy_analyzer_helper import *

MAINNET_SCRIPT_TYPE = {
    'P2PKH': '1',
    'P2SH': '3',
    'P2WPKH': 'bc1q',
    'P2WSH': 'bc1q',
    'P2TR': 'tb1p'
}
TESTNET_SCRIPT_TYPE = {
    'P2PKH': 'm',
    'P2SH': '2',
    'P2WPKH': 'tb1q',
    'P2WSH': 'tb1q',
    'P2TR': 'tb1p'
}


def check_for_round_number(tx_outputs):
    addresses = []
    amounts = []
    for output in tx_outputs:
        addresses.append(output['address'])
        amounts.append(output['amount'])
    if len(amounts) > 1:
        for amount in amounts:
            if int(amount) % 10 != 0:
                index = amounts.index(amount)
                response = f"{addresses[index]} seem like a change address, it violates the round number privacy."
                return response
    else:
        pass


def check_for_script_type(address, transaction_ids, output_indexes):
    if address[0][0] == address[1][0]:
        pass
    else:
        address_type = []
        for add in address:
            for i in TESTNET_SCRIPT_TYPE:
                if add[0] == TESTNET_SCRIPT_TYPE.get(i):
                    address_type.append(i)
        tx_input_script_type = fetch_translation(transaction_ids, output_indexes)
        for type in address_type:
            if type == tx_input_script_type['address_type']:
                response = f'{add} seem like a change address, it has same script type as the transaction input'
                return response


def check_for_address_reuse(addresses, network):
    message = []

    for address in addresses:
        txn_count = get_address_transaction_count(address, network)
        if txn_count > 0:
            response = {
                address: f"this address has been reused for {txn_count} transactions",
                'recommendation': 'it is preferred not to use this address for privacy concerns'
            }
            message.append(response)
    return message
