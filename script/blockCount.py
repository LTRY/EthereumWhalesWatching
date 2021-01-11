from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from tqdm import tqdm
import time
import pymysql


PAD = 1000
LAST_PROCESSED_BLOCK = 0
START_BLOCK = LAST_PROCESSED_BLOCK
END_BLOCK = 11327362


def queryQL(START_BLOCK, END_BLOCK):

    transport = AIOHTTPTransport(url="http://127.0.0.1:8545/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=120)
    query = gql(
        """
            {
                blocks(from: """ + str(START_BLOCK) + """ , to: """ + str(END_BLOCK) + """) {
                    number
                    transactionCount
                    timestamp
                }
            }
        """
    )
    return client.execute(query)


def processGraphQlQuery(rep):

    _list = []
    for block in rep['blocks']:
        _list.append((int(block['number'], 16), block['transactionCount'], int(block['timestamp'], 16)))

    return _list


def commit(addr_tab):

    if len(addr_tab) != 0:
        conn = pymysql.connect("127.0.0.1", "root", "*******", "ETH")
        cur = conn.cursor()
        _str = "REPLACE INTO block_info (`number`, `transactionCount`, `timestamp`) VALUES "
        for addr in addr_tab:
            _str += str(addr) + ','
        _str = _str[:-1] + ';'
        cur.execute(_str)
        conn.commit()
        cur.close()
        conn.close()


def main():

   block = START_BLOCK
   ITR = int((END_BLOCK - START_BLOCK) / PAD)
   _itr = 0
   for _itr in tqdm(range(ITR)):
       _itr += 1
       _list = processGraphQlQuery(queryQL(block, block + PAD))
       commit(_list)
       block += PAD


if __name__ == '__main__':

    tt = time.time()
    main()
    print("\ntotal time exection: {}".format(time.time() - tt))
