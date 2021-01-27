from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from pprint import pprint
from sys import stdout
from time import sleep
import math
import pymysql

SQL_PWD = "pwd"

CEND = '\033[0m'
CRED = '\033[91m'
CGREEN = '\33[32m'
CYELLOW = '\33[33m'
CBLUE = '\33[34m'
CVIOLET = '\33[35m'


def registerWhale(addr):
    conn = pymysql.connect("127.0.0.1", "root", SQL_PWD, "ETH")
    cur = conn.cursor()
    _str = f"INSERT INTO iswhale (`address`, `whale`) VALUES ('{addr}', True);"
    cur.execute(_str)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Whale {addr} registered!")


def isWhales(addr):
    conn = pymysql.connect("127.0.0.1", "root", SQL_PWD, "ETH")
    cur = conn.cursor()
    _str = f"SELECT id FROM iswhale WHERE address = '{addr}';"
    cur.execute(_str)
    rep = [c for c in cur]
    cur.close()
    conn.close()
    if len(rep) == 0:
        print("..Unrecorded fish...Taking note of that one..")
        registerWhale(addr)
        return "New Unknown Whale"
    elif rep[0][0] is not None:
        return rep[0][0]
    else:
        return "Unknown Whale"


def logs(tx):
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


def dumpInSql(tx):
    conn = pymysql.connect("127.0.0.1", "root", SQL_PWD, "ETH")
    cur = conn.cursor()
    _str = f"INSERT INTO suspect_tx (`from`, `value`, `to`, `blockNo`, `price`) VALUES " \
           f"({tx['from']}, {int(tx['value'], 16) / math.pow(10, 18)}, {tx['to']}, {int(tx['block'], 16)}, {tx['price']});"
    cur.execute(_str)
    conn.commit()
    cur.close()
    conn.close()
    print('...Tx stored into sql...')


if __name__ == '__main__':
    consumerTx = KafkaConsumer('Tx', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest',
                              enable_auto_commit=True,
                              group_id='my-group', value_deserializer=lambda x: loads(x.decode('utf-8')))

    print("waiting for messages... ")

    for message in consumerTx:
        tx = message.value

        if int(tx['value'], 16) / 1e+18 > 10000:
            '''Record the transaction if value > 10000'''
            #dumpInSql(tx)

            '''Check if `from` or `to` are known whale, if so, name them; if not take record of it'''
            tx['from'] = isWhales(tx['from'])
            tx['to'] = isWhales(tx['to'])

            '''display logs'''
            logs(tx)

        else:
            print('\nnot interresting tx... Not recorded... Next...')
            logs(tx)



