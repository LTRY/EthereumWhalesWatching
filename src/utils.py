from os import system
import datetime
import time
from enum import Enum
from sys import stdout
from time import sleep


class Color(Enum):
    CEND = '\033[0m'
    CRED = '\033[91m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'


def getABI():
    return [
        {"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":False,"type":"function"},
        {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":False,"type":"function"},
    ]


def get_ERC():
    return {
        '0x6B175474E89094C44Da98b954EedeAC495271d0F': {'token': 'DAI', 'valueFlag': 1, 'dec': 18, 'color': Color.CYELLOW.value},
        '0xdAC17F958D2ee523a2206206994597C13D831ec7': {'token': 'USDT', 'valueFlag': 1, 'dec': 6, 'color': Color.CGREEN.value},
        '0xB8c77482e45F1F44dE1745F52C74426C631bDD52': {'token': 'BNB', 'valueFlag': 1, 'dec': 18, 'color': Color.CYELLOW.value},
        '0x514910771AF9Ca656af840dff83E8264EcF986CA': {'token': 'LINK', 'valueFlag': 1, 'dec': 18, 'color': Color.CBLUE.value},
        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48': {'token': 'USDC', 'valueFlag': 1, 'dec': 6, 'color': Color.CBLUE.value},
        '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {'token': 'UNI', 'valueFlag': 1, 'dec': 18, 'color': Color.CVIOLET.value},
        '0xc00e94cb662c3520282e6f5717214004a7f26888': {'token': 'COMP', 'valueFlag': 1, 'dec': 18, 'color': Color.CGREEN.value},
        '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2': {'token': 'MKR', 'valueFlag': 1, 'dec': 18, 'color': Color.CRED.value},
    }


def displayLogs(tx):
    """ print tx logs in color according to there size """

    system(
        f'echo {start_logs(tx["block"])}'
        f'{tx["from"]} send'
        f'{tx["color"]} {tx["value"]} {tx["token"]} {Color.CEND.value}'
        f'to {tx["to"]}')


def giveMeFive(msg):
    """ Countdown logs method"""

    for i in range(6):
        stdout.write(f"\r{msg}, retrying in {5 - i} ")
        stdout.flush()
        sleep(1)


def start_logs(block):
    return f'{Color.CGREEN.value}[{datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y %H:%M:%S")} ' \
           f' "|" block no. {block}]: {Color.CEND.value}'
