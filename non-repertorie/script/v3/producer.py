from time import sleep
from json import dumps
from kafka import KafkaProducer
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from web3 import Web3
from web3 import exceptions
from pprint import pprint
from sys import stdout
from requests import get
from os import popen
import pymysql


def giveMeFive(msg):
    """ Countdown logs method"""

    for i in range(6):
        stdout.write(f"\r{msg}, retrying in {5 - i} ")
        stdout.flush()
        sleep(1)


class PyProducer:

    def __init__(self, local=False, txTriggeringValue=10000, fromFlagBlock=False, fast=False):

        self.SQL_PWD = "pwd"
        self.fromFlagBlock = fromFlagBlock
        self.txTriggeringValue = txTriggeringValue
        self.fast = fast

        if local:
            self.HOST = "127.0.0.1"
            self.KAFKA_HOST = "localhost"
            self.SQL_HOST = "127.0.0.1"
        else:
            stream = popen("nslookup host.v2.internal | grep Address")
            output = stream.read()
            self.HOST = output.split(' ')[1][:-1]
            self.KAFKA_HOST = "kafka-cluster"
            self.SQL_HOST = "sql"

        self.initSQL()

        """ Wait for GETH to be started (Not working -> crashing)"""
        while True:
            self.w3 = Web3(Web3.HTTPProvider(f"http://{self.HOST}:8545/"))
            if self.w3.isConnected():
                break
            else:
                giveMeFive("geth not started yet...")

        """  Wait for GETH to be syncing is required """
        while True:
            if self.w3.eth.is_syncing() or self.fromFlagBlock:
                break
            else:
                giveMeFive("geth not syncing yet...")

        self.client = Client(transport=AIOHTTPTransport(url=f"http://{self.HOST}:8545/graphql"),
                             fetch_schema_from_transport=True,
                             execute_timeout=100)

        while True:
            try:
                self.producer = KafkaProducer(bootstrap_servers=[f'{self.KAFKA_HOST}:9092'],
                                              value_serializer=lambda x: dumps(x).encode('utf-8'))
                break
            except:
                giveMeFive("Kafka sleeping... ")

        ''' Starting Loop and looking for Txs '''
        self.producing()

    def initSQL(self):
        """ init ETH databses, make sure things are in place """

        tables = self.querySQL("show tables;")
        if len(tables) == 0:
            tables = [[]]
        if 'blockFlag' not in tables[0]:
            self.querySQL("CREATE TABLE blockFlag (`id` tinyint PRIMARY KEY, `flag` INT NOT NULL);")
            self.querySQL("REPLACE INTO blockFlag (`id`, `flag`) VALUES (1, 0);")

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

    def queryQL(self, block):
        query = gql(
            """
                {
                    block(number: """ + str(block) + """ ) {
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
        return self.client.execute(query)

    def queryFastQL(self, blockBegin, blockEnd):
        query = gql(
            """
                {
                    blocks(from: """ + str(blockBegin) + """, to: """ + str(blockEnd) + """ ) {
                        number
                        transactions {
                            value
                            from { address }
                            to { address }
                        }
                    }
                }
            """
        )
        return self.client.execute(query)

    def producing(self):
        """  Wait for GETH to receive blocks """

        if self.fromFlagBlock:
            # last_block = self.querySQL('SELECT flag FROM blockFlag WHERE id = 1;')[0][0]
            last_block = 4826621
        else:
            last_block = self.w3.eth.syncing['currentBlock']
        sec = 0
        while True:
            sleep(1)
            first_block = last_block
            if self.fromFlagBlock:
                last_block = first_block + 1000
            else:
                last_block = self.w3.eth.syncing['currentBlock']

            if first_block == last_block:
                display = ['/', '-', '\\']
                stdout.write(f'\rno new block, stuck at {last_block} for {sec}s {display[sec % 3]}  ')
                stdout.flush()
                sec += 1

            else:
                # self.querySQL(f"REPLACE INTO blockFlag (`id`, `flag`) VALUES (1, {last_block});")
                sec = 0
                if not self.fast:
                    print(f'\rnew blocks found, from {first_block} to {last_block}')
                    for block in range(first_block, last_block):

                        while True:
                            try:
                                query = self.queryQL(block)
                                for tx in query['block']['transactions']:
                                    if int(tx['value'], 16) / 1e+18 > self.txTriggeringValue:

                                        if tx['to'] is None:
                                            _to = 'missing'
                                        else:
                                            _to = tx['to']['address']

                                        TX = {
                                            'value': tx['value'],
                                            'from': tx['from']['address'],
                                            'to': _to,
                                            'block': block,
                                        }

                                        self.producer.send('Tx', value=TX)
                                break

                            except:
                                print("GraphQL struggling... trying with HTTP-RPC")

                                try:
                                    query = self.w3.eth.getBlockTransactionCount(block)
                                except exceptions.BlockNotFound as e:
                                    print(f"Can't do much about this exception, moving one... \n {e}")
                                    break

                                for itr in range(query):
                                    _tx = self.w3.eth.getTransactionFromBlock(block, itr)
                                    if _tx['value'] / 1e+18 > self.txTriggeringValue:

                                        TX = {
                                            'value': hex(_tx['value']),
                                            'from': _tx['from'],
                                            'to': _tx['to'],
                                            'block': block,
                                        }

                                        self.producer.send('Tx', value=TX)
                else:
                    query = self.queryFastQL(last_block, last_block)
                    for block in query['blocks']:
                        for tx in block['transactions']:
                            if int(tx['value'], 16) / 1e+18 > self.txTriggeringValue:

                                if tx['to'] is None:
                                    _to = 'missing'
                                else:
                                    _to = tx['to']['address']

                                TX = {
                                    'value': tx['value'],
                                    'from': tx['from']['address'],
                                    'to': _to,
                                    'block': tx['number'],
                                }

                                self.producer.send('Tx', value=TX)


if __name__ == '__main__':
    producer = PyProducer(local=True, fromFlagBlock=True)
