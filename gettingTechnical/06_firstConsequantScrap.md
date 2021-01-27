
# 06 . Scrapper le premier million de blocs

### Objectifs
- scrapper les 1 000 000 premiers blocks de la blockchain Ethereum
- enregistrer les données dans une table SQL du disque dur


## 0. Avant de commencer

Pourquoi s'affairer uniquement sur ce premier million de blocs? Premièrement parce que nous n'avons toujours pas réussit à télécharger Ethereum en entier. Oui c'est très long. Et deuxièment, parce que ce chiffre est représentatif de l'ordre de grandeur de la blockchain Ethereum. Si l'exécution de script sur la totalité de ces blocs se fait dans un laps de temps résonnable, alors on peut sans trop s'avancer que le scrapping de la blockchain entière sera faisable avec quelques prérequis en plus.

`Etapes`:  
- on monte un conteneur Geth capable d'acceuillir du script python. (On ajoute `maxpeers=0` pour que la mémoire vive ne serve uniquement aux requêtes)
- on monte le conteneur SQL ou l'on stockera notre base de données et on créer la table ADDR
- on importe le script scrap.py dans ce conteneur
- on l'execute et on attend un certain temps
- on observe le résultat dans le conteneur SQL

## 1. On monte un conteneur GETH (avec l'image enrichie)
```shell script
~ docker run -ti --name eth2 -v /mnt/usb/.ethereum:/root -p 30303:30303 \
    -d eth_image:latest --cache=4096 --ipcpath=/IPC/geth.ipc --maxpeers=0
```

## 2. On monte un conteneur MYSQL et on créer la table ADDR
```shell script
~ docker run -p 3306:3306 --name db2 -v ETH:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=pwd -d mysql --innodb-use-native-aio=0
```

```shell script
~ docker exec -ti db2 sql -p
mysql> CREATE DATABASE ETH;
mysql> USE ETH;
mysql> create table addr(`from` varchar(42) primary key,`nonce` int, `value` varchar(30));
```

Justification du choix des attributs:
- **`from` varchar(42) primary key**
    - on l'utilise en PK pour nous forcer a ne pas avoir de doublon
    - 42 parce que c'est la taille en octets d'une adresse ETH

- **Un int classique pour le `nonce`**
    - codé sur 4 octets, on peut avoir un nombre max de 2 147 483 647 transactions, c'est suffisant pour l'instant

- **`value`: Pourquoi utiliser un varchar(30) et non un bigint?**
    - Bigint est la plus grosse unité pour les nombres (10^18) et c'est insuffisant -> obliger de convertir en varchar
    - L'unité de mesure des valeurs des transactions est le Wgei qui correspond à 10^18 ETH.
    - Le nombre d'Ether n'est pas limité en nombre. Il y a aujourd'hui de l'ordre de 100 000 000 d'ETH en circulation.  
    **--> On veut donc pouvoir insérer un nombre avec un maximum de 18+9=27 décimales, pour être large on prend 30**


### Methode d'ajouts

Comment rajouter des elements dans les tables:
Si l'on prend l'adresse comme primary key (PK), il faut se poser la question, quelle fonction utiliser:
- INSERT
- REPLACE
- INSERT...ON DUPLICATE KEY UPDATE
- INSERT IGNORE

Une fois qu'on est parti:
- ligne par ligne
- en une ligne quelques adresses
- en une ligne beaucoup d'adresses


## 3. On copie scrap.py dans le conteneur GETH
`scrap.py`
```python
from web3 import Web3
from tqdm import tqdm
import time
import pymysql


START_BLOCK = 20000
END_BLOCK = 1000000
PAD = 10000


def main():
    web3 = Web3(Web3.IPCProvider("/IPC/geth.ipc"))
    #web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/c61bccacc0c04d068436d27d7b836a51"))
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
```

```shell script
~ docker cp /Users/louistiercery/PycharmProjects/eth_whales/gettingTechnical/howToScrap/scrap.py eth2:/
```

## 4. On execute le script et on attend un certain temps
```shell script
~ docker exec -ti eth2 python3 scrap.py
...
## Après ~ 4h d'exécution ##
...
100%|█████████████████████████████████████████████████████████████████████████████| 10000/10000 [02:44<00:00, 60.94it/s]
nb tx processed: 29906      from block 970000 to 980000      96/98

100%|█████████████████████████████████████████████████████████████████████████████| 10000/10000 [03:11<00:00, 52.10it/s]
nb tx processed: 38337      from block 980000 to 990000      97/98

100%|█████████████████████████████████████████████████████████████████████████████| 10000/10000 [02:58<00:00, 55.97it/s]
nb tx processed: 36843      from block 990000 to 1000000      98/98

total time exection: 14384.370118618011
```

## 5. Après 4h, on obtient la table SQL ADDr ci-dessous
```shell script
mysql> select count(*) from addr;
+----------+
| count(*) |
+----------+
|    30121 |
+----------+
1 row in set (0.08 sec)

mysql> select * from addr limit 10;
+--------------------------------------------+-------+-----------------------+
| from                                       | nonce | value                 |
+--------------------------------------------+-------+-----------------------+
| 0x0000000103026f36d9f2BA6468d2816Cd5Dce83a |     0 | 95000000000000000     |
| 0x00006314Ee6Ba5a9421e4aa6A47C6867A882BD92 |     0 | 1000000000000000000   |
| 0x000083cEb2317F5755bE7a745e3C4be7BA396877 |     2 | 8000000000000000000   |
| 0x0001be2782b76273093874aa372870cE6E418B22 |     0 | 1008950000000000000   |
| 0x000251104CE432bD728a5712f175eff4e446023F |     1 | 900000000000000000    |
| 0x0004B15be8cB573A7be023e203E268DbcFFD302B |     7 | 138000000000000000000 |
| 0x0007Ca35a2680425974312233a59A74C00D3C040 |     4 | 100000000000000000    |
| 0x0007D7E9763E6137369CAA6400F76A2059b6CfA5 |     0 | 10541536900000000000  |
| 0x0007E36161eB9e4799197B441a4310BC70DE1538 |     0 | 0                     |
| 0x0008973f5772FF0D13CDb64FA10fc35cbF71D03c |     0 | 1253000000000000000   |
+--------------------------------------------+-------+-----------------------+
10 rows in set (0.00 sec)

mysql> select * from addr order by nonce DESC limit 10;
+--------------------------------------------+--------+----------------------+
| from                                       | nonce  | value                |
+--------------------------------------------+--------+----------------------+
| 0x52bc44d5378309EE2abF1539BF71dE1b7d7bE3b5 | 178398 | 925981218596705024   |
| 0x2a65Aca4D5fC5B5C859090a6c34d164135398226 | 159503 | 2604244150000000000  |
| 0x63a9975ba31B0b9626b34300f7f627147dF1F526 |  79525 | 271048909999999968   |
| 0x1DCb8d1F0FCc8CbC8C2d76528E877F915e299fbE |  67985 | 160000000000000000   |
| 0x48175Da4c20313bcb6B62d74937d3fF985885701 |  67794 | 0                    |
| 0xf8b483DbA2c3B7176a3Da549ad41A48BB3121069 |  64817 | 21501395590000000000 |
| 0x4Bb96091Ee9D802ED039C4D1a5f6216F90f81B01 |  31010 | 4962687394500000000  |
| 0xC400b9D93A23b0be5d41ab337aD605988Aef8463 |  24139 | 1                    |
| 0x26588a9301b0428d95e6Fc3A5024fcE8BEc12D51 |  22510 | 0                    |
| 0xe6A7a1d47ff21B6321162AEA7C6CB457D5476Bca |  18496 | 12205832661846755000 |
+--------------------------------------------+--------+----------------------+
10 rows in set (0.04 sec)

mysql> select count(*) from addr where nonce > 1000;
+----------+
| count(*) |
+----------+
|       83 |
+----------+
1 row in set (0.02 sec)
```

`CONCLUSION`
- On a mis 4h à parcourir les 1 000 000 premiers blocks
- On trouve à peine 30 000 adresses actives sur ces 1 000 0000 blocks
- On trouve déja plus de 83 adresses avec plus de 1000 transactions effectuées

`SOURCE`:
- https://docs.microsoft.com/fr-fr/sql/t-sql/data-types/int-bigint-smallint-and-tinyint-transact-sql?view=sql-server-ver15
- https://sql.sh/cours/insert-into
- https://stackoverflow.com/questions/8043908/how-do-i-force-an-insert-into-a-table-with-a-unique-key-if-its-already-in-the-t
- https://stackoverflow.com/questions/548541/insert-ignore-vs-insert-on-duplicate-key-update
