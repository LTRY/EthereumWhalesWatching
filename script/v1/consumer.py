from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from pprint import pprint
from sys import stdout
from time import sleep
import math


def isWhales(tx):
    cursor = collection.find({'from': {'address': tx['from']['address']}})
    for inventory in cursor:
        pprint(inventory)
    print(f'A whale have been stopped at block ... .'
          f'Addr {tx["from"]["address"]} send {int(tx["value"], 16)} to {tx["to"]["address"]}\n')


if __name__ == '__main__':
    consumerTx = KafkaConsumer('Tx', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest',
                              enable_auto_commit=True,
                              group_id='my-group', value_deserializer=lambda x: loads(x.decode('utf-8')))

    client = MongoClient('localhost:27017')
    collection = client.eth.tx
    
    CEND = '\033[0m'
    CRED = '\033[91m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'

    print("waiting for messages... ")

    for message in consumerTx:
        tx = message.value
        collection.insert_one(tx)

        if 100 < int(tx['value'], 16) / 1e+18 < 1000:
            COLOR = CGREEN
        elif 1000 < int(tx['value'], 16) / 1e+18 < 10000:
            COLOR = CBLUE
        elif 10000 < int(tx['value'], 16) / 1e+18:
            COLOR = CRED
        else:
            COLOR = CVIOLET

        print(f'{COLOR} transaction occured at block {int(tx["block"], 16)}, {tx["from"]} send {int(tx["value"], 16) / math.pow(10, 18)} '
              f'ETH priced at {tx["price"]} to {tx["to"]} {CEND}')
