from web3 import Web3
from tqdm import tqdm
import time
import pymysql


START_BLOCK = 20000
END_BLOCK = 1000000
PAD = 10000


def main():
    web3 = Web3(Web3.IPCProvider("/IPC/geth.ipc"))
    # web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/c61bccacc0c04d068436d27d7b836a51"))
    if not web3.isConnected():
        print("Not connected, stop process")
    else:

        block = START_BLOCK
        ITR = int((END_BLOCK - START_BLOCK) / PAD)

        for _itr in range(ITR):

            _list = []

            for ref_block in tqdm(range(block, block + PAD)):

                for transaction in range(len(web3.eth.getBlock(ref_block).transactions)):
                    tx = web3.eth.getTransactionByBlock(ref_block, transaction)
                    _list.append((tx['from'], tx['nonce'], str(tx['value'])))

            print("nb tx processed: {0}      from block {1} to {2}      {3}/{4}\n".format(len(_list), block, block + PAD, _itr + 1, ITR))
            commit(_list)
            block += PAD


def commit(addr_tab):
    if len(addr_tab) != 0:
        conn = pymysql.connect("172.17.0.3", "root", "******", "ETH")
        cur = conn.cursor()
        _str = "REPLACE INTO addr (`from`, `nonce`, `value`) VALUES "
        for addr in addr_tab:
            _str += str(addr) + ','
        _str = _str[:-1] + ';'
        cur.execute(_str)
        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    tt = time.time()
    main()
    print("\ntotal time exection: {}".format(time.time() - tt))

