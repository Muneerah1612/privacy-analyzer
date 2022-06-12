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
        tx_input_script_type = fetch_transaction(transaction_ids, output_indexes)['address_type']
        for address in addresses:
            addr = [address for k, v in TESTNET_SCRIPT_TYPE.items() if address[0] == v and k == tx_input_script_type]
            address_type.extend(addr)
        response: str = f'{address_type[0]} seem like a change address, it has same script type as the transaction input'
        return response


def check_for_exact_payment_amount(tx_inputs, tx_outputs):
    if len(tx_inputs) > 1 and len(tx_outputs) == 1:
        response = 'This transaction is likely indicating that bitcoins did not move hand'
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


def check_for_largest_amount_address(outputs):
    largest_output = outputs[0]
    lowest_output = outputs[0]

    for output in outputs:
        if lowest_output['amount'] > output['amount']:
            lowest_output = output
        elif largest_output['amount'] < output['amount']:
            largest_output = output

    if 5 * lowest_output['amount'] < largest_output['amount']:
        possible_change = {largest_output['address']: largest_output['amount']}
        response = {"address": possible_change, "message": "this a likely a change address"}
    else:
        response = {}

    return response


def check_for_equal_output(inputs, outputs=None):
    if outputs is None:
        outputs = dict()
    input_address_total_amount = dict()
    count = 0
    for tx_input in inputs:
        if input_address_total_amount.get(tx_input['address']) is not None:
            input_address_total_amount[tx_input['address']] = input_address_total_amount.get(
                tx_input['address']) + tx_input['amount']
        else:
            input_address_total_amount.update(
                {tx_input['address']: tx_input['amount']})

    sorted_input_amount = sorted(input_address_total_amount.items(
    ), key=lambda input_amount: input_amount[1], reverse=True)

    sorted_output_amount = sorted(
        outputs, key=lambda output_amount: output_amount['amount'], reverse=True)

    possible_change_output = []
    for output_amount in sorted_output_amount:
        if 0.8 <= output_amount.get('amount') / sorted_input_amount[count][1] < 1:
            possible_change_output.append(output_amount)
        count = count + 1

        if count == len(sorted_input_amount):
            break

    return possible_change_output
