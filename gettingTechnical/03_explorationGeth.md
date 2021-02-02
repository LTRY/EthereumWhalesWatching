
# 03. Exploration des différentes méthodes qui permettent d'interroger la blockchain

### Objectifs

- Déterminer la méthode la plus rapide afin d'accéder aux transactions proposé par geth.

## 1. Où nous en sommes

Aujourd'hui nous avons un container geth qui tourne avec quelques 3 000 000 de blocks téléchargés. 
Soit un peu moins du tiers d'ethereum. C'est amplement suffisant pour commencer à faire des tests d'éxécution de scripts.

L'accès au noeud ethereum se fait via **HTTP** et ce dernier se lance alors avec la commande suivante:
```shell script
docker run -ti --name eth2 -v /Volumes/ETH/.ethereum:/root \
  -p 127.0.0.1:8545:8545 -p 30303:30303 \
  -d eth_image:latest --ipcpath=/IPC/geth.ipc \
  --http --http.api eth,web3,personal --http.addr="0.0.0.0" --maxpeers=0
```

La première curiosité qui nous est apparu lors de notre apprentissage de la blockchain ethereum est l'énorme ressemblance
de 2 fonctions qui retournent à priori la même chose. En effet, la console javascript du client ethereum geth propose 2 
méthodes différentes pour accéder aux transactions. 
L'une cherche les transactions et l'autre cherche l'indice des transactions dans un bloc. L'intuition qui s'en dégage 
est que la vitesse d'exécution de ces 2 méthodes est différente. Voici les 2 méthodes:

- eth.getTransaction
- eth.getTransactionFromBlock

## 2. Comparaison des méthodes

Le but de cette petite étude est de déterminer si l'une est effectivement plus rapide que l'autre en vue du scappring
de la blockchian Ethereum.  
On écrit un script python qui réalise plusieurs bloucles, ce qui nous permet de moyenner la vitesse d'éxécution des méthodes.  


`speed_comparaison.py`
```python
from web3 import Web3
from tqdm import tqdm
import time

web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
print(web3.isConnected())


def byTransaction():
    _dic = {}
    t = time.time()

    for ref_block in tqdm(range(3865000, 3865100)):

        a = web3.eth.getBlock(ref_block).transactions
        for b in a:
            c = web3.eth.getTransaction(b)
            _dic[c['from']] = {
                'value': c['value'],
                'nonce': c['nonce']
            }
    print(len(_dic))
    return time.time() - t


def byTransactionFromBlock():
    _dic = {}
    t = time.time()

    for ref_block in tqdm(range(3865000, 3865100)):

        for transaction in range(len(web3.eth.getBlock(ref_block).transactions)):
            c = web3.eth.getTransactionByBlock(ref_block, transaction)
            _dic[c['from']] = {
                'value': c['value'],
                'nonce': c['nonce']
            }
    print(len(_dic))
    return time.time() - t


if __name__ == '__main__':
    byT = 0
    byTfB = 0

    for i in range(5):
        byT += byTransaction()
        byTfB += byTransactionFromBlock()

    print('getTransaction: {}'.format(byT / 5))
    print('getTransactionFromBlock: {}'.format(byTfB / 5))
```

`result`:
```shell script
(venv) ~ python3 speed_comparaison.py
getTransaction: 70,5946566104889
getTransactionFromBlock: 44,562959051132204
```

`CONCLUSION`:  
La méthode web3.eth.getTransactionFromBlock est `58,42%` plus rapide que web3.eth.getTransaction

`NOTE`: Il a été compris plus tard que Geth entretenait un système de cache une fois la commande effectuée, l'exécuter une seconde fois était donc plus rapide.
Cependant, cela n'a pas d'influence sur notre conclusion.
