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
        tx_input_script_type = fetch(transaction_ids, output_indexes)['address_type']
        for address in addresses:
            addr=[address for k,v in TESTNET_SCRIPT_TYPE.items() if address[0] ==v and k==tx_input_script_type]
            address_type.extend(addr)
        response: str = f'{address_type[0]} seem like a change address, it has same script type as the transaction input'
        return response

def check_for_exact_payment_amount(tx_inputs, tx_outputs):
    if len(tx_inputs) > 1 and len(tx_outputs) == 1:
        response = 'This transaction is likely indicating that bitcoins did not move hand'
        return response
