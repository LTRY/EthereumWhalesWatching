from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from pprint import pprint
from tqdm import tqdm
import time
import pymysql
import asyncio


PAD = 100
LAST_PROCESSED_BLOCK = 0
START_BLOCK = LAST_PROCESSED_BLOCK
END_BLOCK = 11327362



def queryQL(START_BLOCK, END_BLOCK):
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://127.0.0.1:8545/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=120)

    # Provide a GraphQL query
    query = gql(
        """
            {
                blocks(from: """ + str(START_BLOCK) + """ , to: """ + str(END_BLOCK) + """) {
                    transactions {
                        value
                        from {
                            address
                        }
                    }
                }
            }
        """
    )

    # Execute the query on the transport
    t = time.time()
    result = client.execute(query)
    print(result)
    print(f"\n {time.time() - t}")
    """
    try:
        result = client.execute(query, execute_timeout=30)
    except Exception as err:
        print('rollback')
    """

    return result


def processGraphQlQuery(rep):

    _list = []
    for block in rep['blocks']:
        for tx in block['transactions']:
            _list.append((tx['from']['address'], str(int(tx['value'], 16))))

    return _list


def main():
   block = START_BLOCK
   ITR = int((END_BLOCK - START_BLOCK) / PAD)
   _itr = 0
   for _itr in tqdm(range(ITR)):
       _itr += 1
       _list = processGraphQlQuery(queryQL(block, block + PAD))
       #print("nb tx processed: {0}      from block {1} to {2}      {3}/{4}\n".format(len(_list), block, block + PAD, _itr + 1, ITR))
       commit(_list)
       block += PAD


def commit(addr_tab):
    if len(addr_tab) != 0:
        conn = pymysql.connect("127.0.0.1", "root", "******", "ETH")
        cur = conn.cursor()
        _str = "REPLACE INTO addrQL (`from`, `value`) VALUES "
        for addr in addr_tab:
            _str += str(addr) + ','
        _str = _str[:-1] + ';'
        cur.execute(_str)
        conn.commit()
        cur.close()
        conn.close()


async def asynctest():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://localhost:8545/graphql")

    # Create a GraphQL client using the defined transport
    #client = Client(transport=transport, fetch_schema_from_transport=True)
    async with Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=60) as session:
        # Provide a GraphQL query
        query = gql(
            """
                {
                    blocks(from: 100000, to:200000) {
                        transactions {
                            value
                            from {
                                address
                                transactionCount 
                            }
                        }
                    }
                }
            """
        )

        # Execute the query on the transport
        result = await session.execute(query)
        # return result
        return result


def test():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://127.0.0.1:8545/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=60)

    # Provide a GraphQL query
    query = gql(
        """
                {
                    blocks(from: 140000, to:150000) {
                        transactions {
                            value
                            from {
                                address
                                transactionCount 
                            }
                        }
                    }
                }
            """
    )

    # Execute the query on the transport
    result = client.execute(query)
    """    
    try:
        result = client.execute(query, execute_timeout=30)
    except Exception as err:
        print('rollback')
    """
    return result


if __name__ == '__main__':
    tt = time.time()
    # main()
    test()
    # asyncio.run(asynctest())
    print("\ntotal time exection: {}".format(time.time() - tt))
