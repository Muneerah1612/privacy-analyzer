from requests import *
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


def check_for_script_type(addresses, transaction_ids, output_indexes):
    if addresses[0][0] == addresses[1][0]:
        pass
    else:
        address_type = []
        for address in addresses:
            for i in TESTNET_SCRIPT_TYPE:
                if address[0] == TESTNET_SCRIPT_TYPE.get(i):
                    address_type.append(i)
        tx_input_script_type = fetch(transaction_ids, output_indexes)
        for script_type in address_type:
            if script_type == tx_input_script_type['address_type']:
                response: str = f'{address} seem like a change address, it has same script type as the transaction input'
                return response


