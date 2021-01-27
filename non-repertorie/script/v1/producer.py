from time import sleep
from json import dumps
from kafka import KafkaProducer
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from web3 import Web3
from pprint import pprint
from sys import stdout
from requests import get


def giveMeFive(msg):
    for i in range(6):
        stdout.write(f"\r{msg}, retrying in {5-i} ")
        stdout.flush()
        sleep(1)


def queryQL(START_BLOCK, END_BLOCK):

    transport = AIOHTTPTransport(url="http://127.0.0.1:8545/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=100)
    query = gql(
        """
            {
                blocks(from: """ + str(START_BLOCK) + """ , to: """ + str(END_BLOCK) + """) {
                    number
                    timestamp
                    transactions {
                        value
                        from {
                            address 
                        }
                        to {
                            address 
                        }
                    }
                }
            }
        """
    )
    return client.execute(query)


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
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))
    sec = 0

    while True:
        try:
            w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/"))
            break
        except:
            giveMeFive("geth not started yet...")


    while True:
        if w3.eth.is_syncing():
            lastBlock = w3.eth.syncing['currentBlock']
            break
        else:
            giveMeFive("geth not syncing yet...")

    while True:
        first_block = lastBlock
        lastBlock = w3.eth.syncing['currentBlock']

        if first_block == lastBlock:
            display = ['/', '-', '\\']
            stdout.write(f'\rno new block, stuck at {lastBlock} for {sec}s {display[sec % 3]}  ')
            stdout.flush()
            sec += 1

        else:
            sec = 0
            print(f'\rnew blocks found, from {first_block} to {lastBlock}')

            while True:
                # ne marche pas tres bien
                try:
                    data = queryQL(first_block, lastBlock)  # Query 1
                    break
                except:
                    giveMeFive("GraphQL struggeling...")

            unix = [int(block['timestamp'], 16) for block in data['blocks']]
            prices = queryBinance(min(unix) * 1000 - 100000, max(unix) * 1000 + 100000)  # Query 2

            for block in data['blocks']:
                for tx in block['transactions']:
                    if int(tx['value'], 16) / 1e+18 > 100:
                        if tx['to'] is None:
                            _to = 'missing'
                        else:
                            _to = tx['to']['address']

                        TX = {
                            'value': tx['value'],
                            'from': tx['from']['address'],
                            'to': _to,
                            'block': block['number'],
                            'price': isBetween(int(block['timestamp'], 16), prices)
                        }

                        producer.send('Tx', value=TX)

        sleep(1)
