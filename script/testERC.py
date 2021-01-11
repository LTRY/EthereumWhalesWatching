from web3 import Web3
from pprint import pprint
import json
import time

abi = [
    {"constant":True,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},
    {"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},
    {"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":False,"type":"function"},
    {"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},
    {"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":False,"type":"function"},
    {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},
    {"constant":False,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},
    {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},
    {"constant":True,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"type":"function"},
    {"constant":False,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},
    {"constant":False,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},
    {"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},
    {"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},
    {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":False,"type":"function"},
    {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},
    {"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":False,"type":"function"},
    {"constant":False,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":False,"type":"function"},
    {"anonymous":False,"inputs":[{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},
    {"anonymous":False,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":False,"inputs":[],"name":"Pause","type":"event"},
    {"anonymous":False,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"owner","type":"address"},{"indexed":True,"name":"spender","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}
]

_ERC = {
    # '0x07597255910a51509CA469568B048F2597E72504': '1UP',
    '0x6B175474E89094C44Da98b954EedeAC495271d0F': 'DAI',
    # '0xdAC17F958D2ee523a2206206994597C13D831ec7': 'USDT',
    '0xB8c77482e45F1F44dE1745F52C74426C631bDD52': 'BNB',
    '0x514910771AF9Ca656af840dff83E8264EcF986CA': 'LINK',
    # '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48': 'USDC',
    '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': 'UNI',
    '0xc00e94Cb662C3520282E6f5717214004A7f26888': 'COMP',
    '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2': 'MKR'
}


def ERCprocess():

    for block in range(11000020, 11000100):

        block_range = len(w3.eth.getBlock(block)['transactions'])

        for itr in range(block_range):
            _tx = w3.eth.getTransactionByBlock(block, itr)
            if _tx['to'] in list(_ERC.keys()):
                contract = w3.eth.contract(address=_tx['to'], abi=abi)
                c = str(contract.decode_function_input(_tx['input']))
                if c.find('transferFrom') != -1:
                    d = json.loads(c[c.find('{'):][:-1].replace("'", '\"'))
                    d['_token'] = _ERC[_tx['to']]
                    pprint(d)

                elif c.find('transfer') != -1:
                    d = json.loads(c[c.find('{'):][:-1].replace("'", '\"'))
                    d['_from'] = _tx['from']
                    d['_token'] = _ERC[_tx['to']]

                    pprint(d)


if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    t = time.time()
    ERCprocess()
    print(time.time() - t)



