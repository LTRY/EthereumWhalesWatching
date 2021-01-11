from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from tqdm import tqdm
import time
import pymysql


PAD = 10
LAST_PROCESSED_BLOCK = 7753299
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


def processGraphQlQuery(rep, not_processed_tx):

    _list = []
    for block in rep['blocks']:
        for tx in block['transactions']:
            if tx['value'] != "0x0":

                if tx['to'] is None:
                    _list.append((tx['from']['address'], str(int(tx['value'], 16)), False, int(block['number'], 16)))
                else:
                    _list.append((tx['from']['address'], str(int(tx['value'], 16)), tx['to']['address'], int(block['number'], 16)))

            else:
                not_processed_tx += 1
    return _list, not_processed_tx


def commit(addr_tab):

    if len(addr_tab) != 0:
        conn = pymysql.connect("127.0.0.1", "root", "Qr8:moew1B/?", "ETH")
        cur = conn.cursor()
        _str = "INSERT INTO tx_01 (`from`, `value`, `to`, `blockNo`) VALUES "
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
    not_processed_tx = 0
    for _itr in tqdm(range(ITR)):
        _itr += 1
        _list, not_processed_tx = processGraphQlQuery(queryQL(block, block + PAD), not_processed_tx)
        commit(_list)
        block += PAD
    print(f"not_processed_tx: {not_processed_tx}")


if __name__ == '__main__':

    tt = time.time()
    main()
    print("\ntotal time exection: {}".format(time.time() - tt))
