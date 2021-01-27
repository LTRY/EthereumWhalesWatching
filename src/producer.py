from time import sleep
from json import dumps
from kafka import KafkaProducer
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from web3 import Web3
from sys import stdout
from os import popen
from fire import Fire
from utils import giveMeFive
from os import system
from pprint import pprint


class PyProducer:

    def __init__(self, local=False, fromFlagBlock=0):

        self.SQL_PWD = "pwd"
        self.fromFlagBlock = fromFlagBlock

        if local:
            self.HOST = "127.0.0.1"
            self.KAFKA_HOST = "localhost"
            self.SQL_HOST = "127.0.0.1"
        else:
            stream = popen("nslookup host.docker.internal | grep Address")
            output = stream.read()
            self.HOST = output.split(' ')[1][:-1]
            # self.HOST = output.split('\t')[1].split(':')[0]
            # self.HOST = "192.168.65.2"
            self.KAFKA_HOST = "kafka-cluster"
            self.SQL_HOST = "sql"

        system("echo ...Wait for GETH to be started...")
        while True:
            self.w3 = Web3(Web3.HTTPProvider(f"http://{self.HOST}:8545/"))
            if self.w3.isConnected():
                break
            else:
                giveMeFive("geth not started yet...")

        system("echo ...Wait for GETH to be syncing if required...")
        while True:
            if self.w3.eth.is_syncing() or self.fromFlagBlock != 0:
                break
            else:
                giveMeFive("geth not syncing yet...")

        system("echo ...Wait for GraphQL to be ready...")
        self.client = Client(transport=AIOHTTPTransport(url=f"http://{self.HOST}:8545/graphql"),
                             fetch_schema_from_transport=True,
                             execute_timeout=10)

        system("echo ...Wait for Kafka to be ready...")
        while True:
            try:
                self.producer = KafkaProducer(bootstrap_servers=[f'{self.KAFKA_HOST}:9092'],
                                              value_serializer=lambda x: dumps(x).encode('utf-8'))
                break
            except:
                giveMeFive("Kafka sleeping... ")

        system("echo ...Start querying...")
        self.producing()

    def queryQL(self, block):
        query = gql(
            """
            {
                block(number: """ + str(block) + """ ) {
                    number
                    transactions {
                        inputData
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

    def producing(self):
        """  Wait for GETH to receive blocks """

        if self.fromFlagBlock != 0:
            last_block = self.fromFlagBlock
        else:
            last_block = self.w3.eth.syncing['currentBlock']

        sec = 0
        while True:
            sleep(1)
            first_block = last_block
            if self.fromFlagBlock != 0:
                last_block = first_block + 1000
            else:
                last_block = self.w3.eth.syncing['currentBlock']

            if first_block == last_block:
                display = ['/', '-', '\\']
                stdout.write(f'\rno new block, stuck at {last_block} for {sec}s {display[sec % 3]}  ')
                stdout.flush()
                sec += 1

            else:
                sec = 0
                system(f'echo \rnew blocks found, from {first_block} to {last_block}')
                for block in range(first_block, last_block):
                    # system(f'echo {block}')
                    try:
                    # if 1 == 1:
                        query = self.queryQL(block)
                        if query['block'] is None:
                            system('echo GraphQL returned none')
                        else:
                            block = int(query['block']['number'], 16)
                            for tx in query['block']['transactions']:
                                tx['block'] = block
                                self.producer.send('tx', value=tx)
                    except:
                        pass


if __name__ == '__main__':
    Fire(PyProducer)
