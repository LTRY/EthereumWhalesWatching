
# 04 . Retranscrire les transactions de notre noeud Geth dans un conteneur mysql en passant par python en local


### Objectifs
- créer un conteneur mysql
- parcourir quelques blocs depuis la machine local
- enregistrer nos informations selon un schéma à déterminer


## 0. Jusqu'ici

On a un container geth et une partie de la blockchain ethereum disponible.
L'accès au noeud ethereum se fait via **HTTP** et ce dernier se lance alors avec la commande suivante:
```shell script
docker run -ti -d \
  -v /Volumes/ETH/.ethereum:/root \
  -p 127.0.0.1:8545:8545 -p 30303:30303 ethereum/client-go --ipcpath=/IPC/geth.ipc \
  --http --http.api eth,web3,personal --http.addr "0.0.0.0" --maxpeers 0
```

## I. PARTIE MYSQL

On crée un conteneur Mysql avec les arguments de base requis. La base de données est stockée sur le disque dur de l'ordinateur. 
On verra comment stocker la base de données sur notre disque externe plus tard !

```shell script
~ docker run -p 3306:3306 --name db -e MYSQL_ROOT_PASSWORD=pwd -d mysql
2a982e3470339aad55feadb2c39e50ef5257eeab3f70681b12fd4661d41e2999
```

---

Maintenant go sur la console sql
```shell script
docker exec -ti db mysql -p

mysql> CREATE DATABASE ETH_ADDR;
  Query OK, 1 row affected (0.58 sec)

mysql> use ETH_ADDR;
  Database changed

mysql> CREATE TABLE addr(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, address VARCHAR(42) NOT NULL);
  Query OK, 0 rows affected (0.35 sec)

mysql> DESCRIBE addr;
+---------+-------------+------+-----+---------+----------------+
| Field   | Type        | Null | Key | Default | Extra          |
+---------+-------------+------+-----+---------+----------------+
| id      | int         | NO   | PRI | NULL    | auto_increment |
| address | varchar(42) | NO   |     | NULL    |                |
+---------+-------------+------+-----+---------+----------------+
2 rows in set (0.01 sec)
```

La base de données est prête à acceuillir de la donnée. 

## II. PARTIE PYTHON

On travaille avec python depuis notre ordinateur, on verra plus tard comment executer du script python depuis un conteneur docker.

- On commence par installer la librairie `pymysql`
```shell script
pip install pymysql
```

- Ensuite on écrit les fonctions qui nous permettront d'intéragir avec la base de données sql. (De python local à docker sql)
`mysql.py`
```python
import pymysql


def commit(addr_tab):
    print(addr_tab)
    conn = pymysql.connect("127.0.0.1", "root", "******", "ETH_ADDR")
    cur = conn.cursor()
    for addr in addr_tab:
        cur.execute("INSERT INTO addr (address) VALUES ('{}');".format(addr))
    conn.commit()
    cur.close()
    conn.close()
    print("done")


def show():
    conn = pymysql.connect("127.0.0.1", "root", "******", "ETH_ADDR")
    cur = conn.cursor()
    cur.execute("SELECT * FROM addr;")
    rows = cur.fetchall()
    for row in rows:
        print(" ", row[0], row[1])
    conn.commit()
    cur.close()
    conn.close()
```

- Ensuite on recupère les addresses des blocks 3 865 000 à 3 865 010 et les stocke dans la base de données grace à nos fonctions précédemment créées. 
`GethToMysql.py`
```python
from web3 import Web3
from tqdm import tqdm
import time
import mysql

web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
if web3.isConnected():
    print("start process")

_addr = []
t = time.time()

for ref_block in tqdm(range(3865000, 3865010)):

    for transaction in range(len(web3.eth.getBlock(ref_block).transactions)):

        _addr.append(web3.eth.getTransactionByBlock(ref_block, transaction)['from'])

print("time execution: {}".format(time.time() - t))
print("nb addresss retrieve: {}".format(len(_addr)))

mysql.commit(_addr)

print("process successfully exited")
```

`result`:
```
start process
100%|██████████| 10/10 [00:04<00:00,  2.01it/s]
time execution: 5.009487152099609
nb addresss retrieve: 600
process successfully exited
```

```sql
mysql> select * from addr limit 10;
+-------+--------------------------------------------+
| id    | address                                    |
+-------+--------------------------------------------+
| 26520 | 0x167A9333BF582556f35Bd4d16A7E80E191aa6476 |
| 26521 | 0x159706e2D14de4993666ab6022aD475c2103e85C |
| 26522 | 0x67c719EF8Baaf4514442e1DE9EFd16BA5dd22e47 |
| 26523 | 0xb2930B35844a230f00E51431aCAe96Fe543a0347 |
| 26524 | 0x5653918FFe457b65E95d383fF485BC346e3bA285 |
| 26525 | 0x1b1B8ED8332dcCc267509aF993b4701C9Fc64D9D |
| 26526 | 0x17441Ec5AFDf341CCd86816D3773f67410aed725 |
| 26527 | 0xeF322F77bE51d73f39C0085eEdE578b5aaBb129b |
| 26528 | 0x0a73573Cf2903d2D8305b1eCb9e9730186a312aE |
| 26529 | 0x00472c1e4275230354dbe5007A5976053f12610a |
+-------+--------------------------------------------+
10 rows in set (0.01 sec)
```

### Nos conclusions:
- On a essayé de mettre la base de données directement sur notre disque dur externe et cela apporte son lot de difficultés. 
  De plus, c'est très compliqué de faire en sorte à ce que la base de données soit accessible depuis une autre machine (windows pour sûr). 
  A essayer avec un autre mac. Du coup avec un mac reboot, ca ne fonctionne pas non plus (chose marrante: in select * from user, on retrouve 2 roots)
- Cette façon apporte beaucoup de doublons d'adresses. Prochainement travailler avec les adresses comme des PRIMARY KEY?
- Tester la rapidité du processus, si on entre dans la base de données toutes les adresses, tous les blocks, tous les qq blocs **TODO**
