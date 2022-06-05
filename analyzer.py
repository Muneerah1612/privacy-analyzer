from requests import *
from privacy_analyzer_helper import *

MAINNET_SCRIPT_TYPE={
    'P2PKH':'1',
    'P2SH':'3',
    'P2WPKH':'bc1q',
    'P2WSH':'bc1q',
    'P2TR':'tb1p'
}
TESTNET_SCRIPT_TYPE={
    'P2PKH':'m',
    'P2SH':'2',
    'P2WPKH':'tb1q',
    'P2WSH':'tb1q',
    'P2TR':'tb1p'
}


def check_for_round_number(txoutputs):
    addresses=[]
    amounts=[]
    for output in txoutputs:
        addresses.append(output['address'])
        amounts.append(output['amount'])
    if len(amounts) > 1:
        for amnt in amounts:
            if int(amnt) % 10 != 0:
                index=amounts.index(amnt)
                response = f"{addresses[index]} seem like a change address, it violates the round number privacy."
                return response
    else:
        pass



def check_for_scripttype(address,transaction_ids,output_indexes):
    if address[0][0]==address[1][0]:
        pass
    else:
        address_type=[]
        for add in address:
            for i in TESTNET_SCRIPT_TYPE:
                if add[0]==TESTNET_SCRIPT_TYPE.get(i):
                    address_type.append(i)
        txinput_scripttype=fetch(transaction_ids,output_indexes)
        for type in address_type:
            if type == txinput_scripttype['address_type']:
                response=f'{add} seem like a change address, it has same script type as the transaction input'
                return response