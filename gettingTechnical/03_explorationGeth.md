
# 03. Explorer les différentes méthodes qui permettent d'interogger la blockchain

### Objectifs

- determiner la plus rapide méthode d'accès aux transactions proposé par geth

## 0. Où nous en sommes

Aujourd'hui nous avons de disponible un container geth qui tourne avec quelques 3 000 000 de blocks téléchargés. 
Soit un peu moins du tiers d'ethereum. C'est amplement suffisant pour commencer à faire des tests d'exécution de scripts

L'accès au noeud ethereum se fait via **HTTP** et ce dernier se lance alors avec la commande suivante:
```shell script
docker run -ti --name eth2 -v /Volumes/ETH/.ethereum:/root \
  -p 127.0.0.1:8545:8545 -p 30303:30303 \
  -d eth_image:latest --ipcpath=/IPC/geth.ipc \
  --http --http.api eth,web3,personal --http.addr="0.0.0.0" --maxpeers=0
```

La première curiositée qui nous est apparut lors de notre apprentissage de la blockchain ethereum est l'énorme ressemblance
de 2 fonctions qui retournent à priori la même chose. En effet, la console javascript du client ethereum geth propose 2 
méthodes différentes pour accéder aux transactions. Elles ne fonctionnent cependant pas de la même facon. 
L'une cherche les transactions et l'autre cherche l'indice des transactions dans un bloc. L'intuition qui s'en dégage 
est que la vitesse d'exécution de ces 2 méthodes est différentes. Voici les 2 méthodes:

- eth.getTransaction
- eth.getTransactionFromBlock

## 1. Comparaison des méthodes

Le but de cette petite étude est de déterminer si l'une est effectivement plus rapide que l'autre en vue du scappring
de la blockchian Ethereum.  
On écrit un script python qui fait plusieurs bloucles, ce qui nous permet de moyenner la vitesse d'exécution des méthodes.  


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

`NOTE`: Il a été compris que plus tard que Geth entretenait un système de cache qui fait qu'une fois une commande effectué, l'exécuté une seconde fois était plus rapide.
Cepandant, cale n'a pas d'influence sur notre conclusion
