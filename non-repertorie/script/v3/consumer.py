from kafka import KafkaConsumer
from json import loads
from pprint import pprint
from sys import stdout
from time import sleep
import math
import pymysql
from os import system
from enum import Enum
import datetime
import time


class Color(Enum):
    CEND = '\033[0m'
    CRED = '\033[91m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'


def displayLogs(tx):
    """ print tx logs in color according to there size """

    if 100 < int(tx['value'], 16) / 1e+18 < 1000:
        COLOR = Color.CVIOLET.value
    elif 1000 < int(tx['value'], 16) / 1e+18 < 10000:
        COLOR = Color.CYELLOW.value
    elif 10000 < int(tx['value'], 16) / 1e+18:
        COLOR = Color.CRED.value
    else:
        COLOR = Color.CBLUE.value

    system(
        f'echo {Color.CGREEN.value} [{datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y %H:%M:%S")} "|" '
        f'block no. {tx["block"]}]: {COLOR}{tx["from"]}send {COLOR} {int(tx["value"], 16) / math.pow(10, 18)} '
        f'ETH {Color.CEND.value}to {tx["to"]} ')


def giveMeFive(msg):
    """ Countdown logs method"""

    for i in range(6):
        stdout.write(f"\r{msg}, retrying in {5 - i} ")
        stdout.flush()
        sleep(1)


class PyConsumer:

    def __init__(self, local=False, logs=False):

        self.SQL_PWD = "pwd"
        self.logs = logs

        if local:
            self.SQL_HOST = "127.0.0.1"
            self.KAFKA_HOST = "localhost"
        else:
            self.SQL_HOST = "sql"
            self.KAFKA_HOST = "kafka-cluster"

        self.initSQL()
        while True:
            try:
                self.consumerTx = KafkaConsumer('Tx', bootstrap_servers=[f'{self.KAFKA_HOST}:9092'],
                                                auto_offset_reset='earliest',
                                                enable_auto_commit=True,
                                                group_id='my-group',
                                                value_deserializer=lambda x: loads(x.decode('utf-8')))
                break
            except:
                giveMeFive("Kafka sleeping... ")

        ''' Starting Loop and looking for Txs messages from kafka broker'''
        self.consuming()

    def initSQL(self):
        """ init ETH databses, make sure things are in place """

        tables = self.querySQL("show tables;")
        if len(tables) == 0:
            tables = [[]]
        # if 'iswhale' not in tables[0]:
        #    self.querySQL(
        #        "CREATE TABLE iswhale (`address` VARCHAR(42) PRIMARY KEY, `nameTag` VARCHAR(40), `whale` BOOL);")

        print(f'Tables found in ETH db: {self.querySQL("show tables;")[0]}')

    def querySQL(self, query):
        """ Query SQL databses """

        while True:
            try:
                conn = pymysql.connect(self.SQL_HOST, "root", self.SQL_PWD, "ETH")
                break
            except:
                giveMeFive("SQL sleeping... ")

        cur = conn.cursor()
        cur.execute(query)
        rep = [c for c in cur]
        conn.commit()
        cur.close()
        conn.close()
        return rep

    def registerWhale(self, addr, block):
        """" Register Whales into SQL database """

        self.querySQL(f"INSERT INTO iswhale (`address`, `whale`) VALUES ('{addr}', True);")
        system(f'echo {Color.CGREEN.value} [{datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y %H:%M:%S")}'
               f' "|" block no. {block}]:{Color.CEND.value} Whale {addr} registered!')

    def isWhales(self, addr, block):
        """" Research if addr is know as a Whale. If so, call registerWhale(self, addr) """

        rep = self.querySQL(f"SELECT nameTag FROM iswhale WHERE address = '{addr}';")
        if len(rep) == 0:
            self.registerWhale(addr, block)
            return f"{Color.CBLUE.value}New Unknown Whale{Color.CEND.value} "
        elif rep[0][0] is not None:
            return rep[0][0]
        else:
            return f"{Color.CBLUE.value}Known Whale{Color.CEND.value} "

    def dumpInSql(self, tx):
        """ TODO """
        self.querySQL(
            f"INSERT INTO suspect_tx (`from`, `value`, `to`, `blockNo`, `price`) VALUES ({tx['from']}, {int(tx['value'], 16) / math.pow(10, 18)}, {tx['to']}, {int(tx['block'], 16)}, {tx['price']});")
        print('...Tx stored into sql...')

    def consuming(self):
        """ Consuming the messages send from producer.py """

        system("\n echo waiting for messages... ")

        for message in self.consumerTx:
            tx = message.value

            '''Record the transaction if value > 10000'''
            # dumpInSql(tx)

            '''Check if `from` or `to` are known whale, if so, name them; if not take record of it'''
            tx['from'] = self.isWhales(tx['from'], tx['block'])
            tx['to'] = self.isWhales(tx['to'], tx['block'])

            '''display logs'''
            if self.logs:
                displayLogs(tx)


if __name__ == '__main__':
    consumer = PyConsumer(local=True, logs=True)
