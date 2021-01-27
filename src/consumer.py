from kafka import KafkaConsumer
from json import loads
import pymysql
import json
from web3 import Web3
import requests
from fire import Fire
from os import system
from os import popen
from pprint import pprint
import utils


class PyConsumer:

    def __init__(self, local=False, logs=False, txTriggeringValue=10000, ERClower=True, waitGethSync=True,
                 onlyETH=False, analyseTX=True, recordSuspectTx=True, sql=True):

        self.SQL_PWD = "pwd"

        """ Params from constructor """
        self.logs = logs
        self._analyseTX = analyseTX
        self.txTriggeringValue = txTriggeringValue
        self.waitGethSync = waitGethSync
        self.onlyETH = onlyETH
        self.recordSuspectTx = recordSuspectTx
        self.sql = sql

        """ Variables for process """
        self.block = None
        if ERClower:
            self._ERC = {}
            for k, v in utils.get_ERC().items():
                self._ERC[k.lower()] = v
        else:
            self._ERC = utils.get_ERC()

        if self.txTriggeringValue > 0:
            system("echo ...retrieve price tickers from POLONIEX exchange...")
            rep = requests.get("https://poloniex.com/public?command=returnTicker").json()
            for addr, dict in self._ERC.items():
                if dict['token'] == 'USDT':
                    self._ERC[addr]['valueFlag'] = self.txTriggeringValue
                else:
                    for k, v in rep.items():
                        if k.find(dict['token']) != -1 and k.find('USDT') != -1:
                            self._ERC[addr]['valueFlag'] = self.txTriggeringValue / float(v['last'])
                            break

        if local:
            self.SQL_HOST = "127.0.0.1"
            self.KAFKA_HOST = "localhost"
            self.HOST = "127.0.0.1"
        else:
            self.SQL_HOST = "sql"
            self.KAFKA_HOST = "kafka-cluster"
            stream = popen("nslookup host.docker.internal | grep Address")
            output = stream.read()
            self.HOST = output.split(' ')[1][:-1]

        if sql:
            self.initSQL()

        system("echo ...Wait for GETH to be started...")
        while True:
            self.w3 = Web3(Web3.HTTPProvider(f"http://{self.HOST}:8545/"))
            if self.w3.isConnected():
                break
            else:
                utils.giveMeFive("geth not started yet...")

        system("echo ...Wait for GETH to be syncing if required...")
        while True:
            if self.w3.eth.is_syncing() or not self.waitGethSync:
                break
            else:
                utils.giveMeFive("geth not syncing yet...")

        system("echo ...Wait for Kafka to be ready...")
        while True:
            try:
                self.consumerQuery = KafkaConsumer('tx', bootstrap_servers=[f'{self.KAFKA_HOST}:9092'],
                                                   auto_offset_reset='earliest',
                                                   enable_auto_commit=True,
                                                   group_id='my-group',
                                                   value_deserializer=lambda x: loads(x.decode('utf-8')))
                break
            except:
                utils.giveMeFive("Kafka sleeping... ")

        system("\n echo ...waiting for messages... ")
        self.consuming()

    def initSQL(self):
        """ init ETH databases, make sure things are in place """

        system("echo ...Wait for SQL to be ready...")
        tables = self.querySQL("show tables;")
        tables = [i[0] for i in tables]
        if 'iswhale' not in tables:
            self.querySQL(
                "CREATE TABLE iswhale (`address` VARCHAR(42) PRIMARY KEY, `nameTag` VARCHAR(40), `whale` BOOL);")
        if 'suspect_tx' not in tables:
            self.querySQL("CREATE TABLE suspect_tx (`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,`from` VARCHAR(42),"
                          " `value` FLOAT, `token` VARCHAR(4), `to` VARCHAR(42), `blockNo` MEDIUMINT UNSIGNED);")

        print(f'...Tables found in SQL ETH db: {[i[0] for i in self.querySQL("show tables;")]}...')

    def querySQL(self, query):
        """ Query SQL databases """

        while True:
            try:
                conn = pymysql.connect(self.SQL_HOST, "root", self.SQL_PWD, "ETH")
                break
            except:
                utils.giveMeFive("SQL sleeping... ")

        cur = conn.cursor()
        cur.execute(query)
        rep = [c for c in cur]
        conn.commit()
        cur.close()
        conn.close()
        return rep

    def registerWhale(self, addr):
        """" Register Whales into SQL database """

        self.querySQL(f"INSERT INTO iswhale (`address`, `whale`) VALUES ('{addr}', True);")
        system(f'echo {utils.start_logs(self.block)}Whale {addr} registered!')

    def isWhales(self, addr):
        """" Research if addr is know as a Whale. If so, call registerWhale(self, addr) """

        rep = self.querySQL(f"SELECT nameTag FROM iswhale WHERE address = '{addr}';")
        if len(rep) == 0:
            self.registerWhale(addr)
            return f"{utils.Color.CBLUE.value}New Unknown Whale{utils.Color.CEND.value} "
        elif rep[0][0] is not None:
            return rep[0][0]
        else:
            return f"{utils.Color.CBLUE.value}Known Whale{utils.Color.CEND.value} "

    def dumpInSql(self, tx):
        """ Dump suspect tx in sql table suspect_tx """
        self.querySQL(
            f"INSERT INTO suspect_tx (`from`, `value`, `token`, `to`, `blockNo`) VALUES "
            f"('{tx['from']}', {tx['value']}, '{tx['token']}', '{tx['to']}', {tx['block']});")
        system(f'echo {utils.start_logs(tx["block"])}Tx from {tx["from"][:5]}.. to {tx["to"][:5]}.. stored into suspect_tx table')

    def AnalyseTX(self, TX):
        """ Replaces `from` and `to` address if registered whales """

        TX['from'] = self.isWhales(TX["from"])
        TX['to'] = self.isWhales(TX["to"])

    def consuming(self):
        """ Consuming the messages send from producer.py """

        for tx in self.consumerQuery:
            tx = tx.value
            self.block = tx['block']
            TX = None
            if tx['to'] is None:
                _to = 'missing'
            else:
                _to = tx['to']['address']

            if int(tx['value'], 16) / 1e+18 > 10000:
                TX = {
                    'token': 'ETH',
                    'value': int(tx['value'], 16),
                    'from': tx['from']['address'],
                    'to': _to,
                    'block': tx['block'],
                    'color': utils.Color.CGREEN.value,
                    }

            if not self.onlyETH and _to in self._ERC.keys():
                contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(_to), abi=utils.getABI())
                try:
                    _input = str(contract.decode_function_input(tx['inputData']))
                except ValueError as e:
                    """ abi function not registered """
                    _input = ''

                if _input.find('transferFrom') != -1:
                    _tx = json.loads(_input[_input.find('{'):][:-1].replace("'", '\"'))
                    TX = {
                        'token': self._ERC[_to]['token'],
                        'value': _tx['_value'] / 10 ** self._ERC[_to]['dec'],
                        'from': _tx['_from'],
                        'to': _tx['_to'],
                        'block': tx['block'],
                        'color': self._ERC[_to]['color'],
                    }
                    if TX["value"] < self._ERC[_to]['valueFlag']:
                        TX = None

                elif _input.find('transfer') != -1:
                    _tx = json.loads(_input[_input.find('{'):][:-1].replace("'", '\"'))
                    TX = {
                        'token': self._ERC[_to]['token'],
                        'value': _tx['_value'] / 10 ** self._ERC[_to]['dec'],
                        'from': tx['from']['address'],
                        'to': _tx['_to'],
                        'block': tx['block'],
                        'color': self._ERC[_to]['color'],
                    }
                    if TX["value"] < self._ERC[_to]['valueFlag']:
                        TX = None

            if TX is not None:
                if self.sql:
                    if self.recordSuspectTx:
                        self.dumpInSql(TX)
                    if self._analyseTX:
                        self.AnalyseTX(TX)
                if self.logs:
                    utils.displayLogs(TX)


if __name__ == '__main__':
    Fire(PyConsumer)
