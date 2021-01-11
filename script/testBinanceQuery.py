import time
import curses
from requests import get
import pandas as pd
from pprint import pprint


dic = {"blocks": [
      {
        "timestamp": "0x5eb01705"
      },
      {
        "timestamp": "0x5eb01708"
      },
      {
        "timestamp": "0x5eb0170d"
      },
      {
        "timestamp": "0x5eb0172b"
      },
      {
        "timestamp": "0x5eb01733"
      },
      {
        "timestamp": "0x5eb01748"
      },
      {
        "timestamp": "0x5eb01760"
      },
      {
        "timestamp": "0x5eb0176b"
      },
      {
        "timestamp": "0x5eb01770"
      },
      {
        "timestamp": "0x5eb0177c"
      },
      {
        "timestamp": "0x5eb01792"
      },
      {
        "timestamp": "0x5eb017bc"
      },
      {
        "timestamp": "0x5eb017e4"
      },
      {
        "timestamp": "0x5eb017fc"
      },
      {
        "timestamp": "0x5eb0181c"
      },
      {
        "timestamp": "0x5eb01831"
      },
      {
        "timestamp": "0x5eb01839"
      },
      {
        "timestamp": "0x5eb01848"
      },
      {
        "timestamp": "0x5eb01850"
      },
      {
        "timestamp": "0x5eb0186a"
      },
      {
        "timestamp": "0x5eb01870"
      },
      {
        "timestamp": "0x5eb01874"
      },
      {
        "timestamp": "0x5eb01875"
      },
      {
        "timestamp": "0x5eb01881"
      },
      {
        "timestamp": "0x5eb01888"
      },
      {
        "timestamp": "0x5eb01890"
      },
      {
        "timestamp": "0x5eb0189f"
      },
      {
        "timestamp": "0x5eb018b7"
      },
      {
        "timestamp": "0x5eb018be"
      },
      {
        "timestamp": "0x5eb018d5"
      },
      {
        "timestamp": "0x5eb018de"
      },
      {
        "timestamp": "0x5eb018e2"
      },
      {
        "timestamp": "0x5eb01900"
      },
      {
        "timestamp": "0x5eb01914"
      },
      {
        "timestamp": "0x5eb0192b"
      },
      {
        "timestamp": "0x5eb0193d"
      },
      {
        "timestamp": "0x5eb01943"
      },
      {
        "timestamp": "0x5eb01952"
      },
      {
        "timestamp": "0x5eb01958"
      },
      {
        "timestamp": "0x5eb01959"
      },
      {
        "timestamp": "0x5eb01989"
      },
      {
        "timestamp": "0x5eb0198f"
      },
      {
        "timestamp": "0x5eb019bb"
      },
      {
        "timestamp": "0x5eb019d7"
      },
      {
        "timestamp": "0x5eb019da"
      },
      {
        "timestamp": "0x5eb019e2"
      },
      {
        "timestamp": "0x5eb019e5"
      },
      {
        "timestamp": "0x5eb019ed"
      },
      {
        "timestamp": "0x5eb019f8"
      },
      {
        "timestamp": "0x5eb01a03"
      },
      {
        "timestamp": "0x5eb01a1b"
      },
      {
        "timestamp": "0x5eb01a24"
      },
      {
        "timestamp": "0x5eb01a27"
      },
      {
        "timestamp": "0x5eb01a28"
      },
      {
        "timestamp": "0x5eb01a36"
      },
      {
        "timestamp": "0x5eb01a40"
      },
      {
        "timestamp": "0x5eb01a41"
      },
      {
        "timestamp": "0x5eb01a4e"
      },
      {
        "timestamp": "0x5eb01a51"
      },
      {
        "timestamp": "0x5eb01a78"
      },
      {
        "timestamp": "0x5eb01a96"
      },
      {
        "timestamp": "0x5eb01ab3"
      },
      {
        "timestamp": "0x5eb01ac2"
      },
      {
        "timestamp": "0x5eb01ac9"
      },
      {
        "timestamp": "0x5eb01ae1"
      },
      {
        "timestamp": "0x5eb01afa"
      },
      {
        "timestamp": "0x5eb01aff"
      },
      {
        "timestamp": "0x5eb01b17"
      },
      {
        "timestamp": "0x5eb01b20"
      },
      {
        "timestamp": "0x5eb01b22"
      },
      {
        "timestamp": "0x5eb01b45"
      },
      {
        "timestamp": "0x5eb01b52"
      },
      {
        "timestamp": "0x5eb01b55"
      },
      {
        "timestamp": "0x5eb01b63"
      },
      {
        "timestamp": "0x5eb01b6d"
      },
      {
        "timestamp": "0x5eb01b71"
      },
      {
        "timestamp": "0x5eb01b72"
      },
      {
        "timestamp": "0x5eb01b77"
      },
      {
        "timestamp": "0x5eb01b78"
      },
      {
        "timestamp": "0x5eb01b96"
      },
      {
        "timestamp": "0x5eb01ba8"
      },
      {
        "timestamp": "0x5eb01bb0"
      },
      {
        "timestamp": "0x5eb01bc3"
      },
      {
        "timestamp": "0x5eb01bcb"
      },
      {
        "timestamp": "0x5eb01bcf"
      },
      {
        "timestamp": "0x5eb01bd1"
      },
      {
        "timestamp": "0x5eb01bd7"
      },
      {
        "timestamp": "0x5eb01bd9"
      },
      {
        "timestamp": "0x5eb01bf1"
      },
      {
        "timestamp": "0x5eb01bf7"
      },
      {
        "timestamp": "0x5eb01bfe"
      },
      {
        "timestamp": "0x5eb01c06"
      },
      {
        "timestamp": "0x5eb01c13"
      },
      {
        "timestamp": "0x5eb01c19"
      },
      {
        "timestamp": "0x5eb01c2b"
      },
      {
        "timestamp": "0x5eb01c2f"
      },
      {
        "timestamp": "0x5eb01c31"
      },
      {
        "timestamp": "0x5eb01c63"
      },
      {
        "timestamp": "0x5eb01c6a"
      },
      {
        "timestamp": "0x5eb01c6f"
      },
      {
        "timestamp": "0x5eb01c7b"
      }
    ]
}


def queryBinance(startTime, endTime):
    _params = {
        'symbol': 'ETHUSDT',
        'interval': '1m',
        'startTime': startTime,
        'endTime': endTime
    }
    return get('https://api.binance.com/api/v3/klines', params=_params).json()


def isBetween(timestamp, prices):
    for i in range(len(prices)-1):
        if prices[i][0] < timestamp * 1000 < prices[i+1][0]:
            return (float(prices[i][4]) + float(prices[i+1][4])) / 2

    return 0


if __name__ == '__main__':

    unix = pd.Series([int(timestamp["timestamp"], 16) for timestamp in dic["blocks"]])
    prices = queryBinance(min(unix) * 1000 - 100000, max(unix) * 1000 + 100000)
    for time in unix:
        print(f'ETH is worth {isBetween(time, prices)} at {time}')