
# 09 . Créer la table Tx qui répertorie les transacions suspect

### Objectifs
- créer la table TX

## Why?
- On veut répertoirier toutes les transactions effectués dans la blockchain pour ensuite repérer les baleines

## 0. Jusqu'ici

On connait le nombre de transations dans la blockchain car nous avons récupérer ces informations dans la partie précédente. 
```shell script
~ mysql -uroot -p
mysql> use ETH;
mysql> SELECT SUM(transactionCount) FROM block_info;
+-----------------------+
| SUM(transactionCount) |
+-----------------------+
|             914382777 |
+-----------------------+
1 row in set (3,70 sec)
```
On a un peu moins d'un milliard de transactions sur ethereum , nous pensons qu'il reste raisonable de récupérer la totalité de 
ces informations dans une table sql. Pour rappel, le but de transférer les données de la blockchain à une base de donnée SQL, 
en perdant le moins d'informations possibles, SQL étant bien plus rapide pour effectuer des opérations sur nos données. 
Cependant, nous n'insérons pas les transactions d'une valeur de "0x0"...

`Etapes`:  
- Faire tourner notre client Geth en local
- Installer mysql en local avec homebrew et on créé la table `tx`
- Executer le script `tableTX.py` en local
- Observer le résultat dans la table sql


## 1. Rendre disponible le noeud Ethereum stocker sur notre HDD.
```shell script
~ geth --syncmode fast --nousb --cache 4096 --datadir=/Volumes/ETH/.ethereum/.ethereum \
   --ipcpath=~/IPC/geth.ipc --http --http.api eth,web3,personal --graphql --maxpeers 0
```

## 2. On lance le service mysql et on créé la table tx
```shell script
mysql> create table tx (`tx_id` int primary key auto_increment, `from` varchar(42), `value` varchar(30), `to` varchar(42), `blockNo` int);
Query OK, 0 rows affected (0,24 sec)

mysql> describe tx;
+---------+-------------+------+-----+---------+----------------+
| Field   | Type        | Null | Key | Default | Extra          |
+---------+-------------+------+-----+---------+----------------+
| tx_id   | int         | NO   | PRI | NULL    | auto_increment |
| from    | varchar(42) | YES  |     | NULL    |                |
| value   | varchar(30) | YES  |     | NULL    |                |
| to      | varchar(42) | YES  |     | NULL    |                |
| blockNo | int         | YES  |     | NULL    |                |
+---------+-------------+------+-----+---------+----------------+
5 rows in set (0,02 sec)
```

## 3. On execute le script `tableTX.py` en local
`tableTX.py`:
```python
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from tqdm import tqdm
import time
import pymysql


PAD = 100
LAST_PROCESSED_BLOCK = 7490300
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
        conn = pymysql.connect("127.0.0.1", "root", "*******", "ETH")
        cur = conn.cursor()
        _str = "REPLACE INTO tx (`from`, `value`, `to`, `blockNo`) VALUES "
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
    print("\ntotal time exection: {}".format(time.time() - tt)) #Very Very long ~ 24h
```

## 4. On observe le résultat dans la table SQL
```shell script
mysql> select * from tx order by tx_id DESC LIMIT 10;
+-----------+--------------------------------------------+-----------------------+--------------------------------------------+---------+
| tx_id     | from                                       | value                 | to                                         | blockNo |
+-----------+--------------------------------------------+-----------------------+--------------------------------------------+---------+
| 251652678 | 0x32b8506a32d633c9e01de102f4aa467235509bcf | 235332510000000000    | 0xb8ba36e591facee901ffd3d5d82df491551ad7ef | 7598900 |
| 251652677 | 0x6544a55f03b53871ec992732a90150392e4307fe | 36932916000000000000  | 0xf113fc1ebf8de5e4411fbd72635ac45b9524e09d | 7598900 |
| 251652676 | 0xae45a8240147e6179ec7c9f92c5a18f9a97b3fca | 246840000000000       | 0x476cce926deca7ca7fa5f36d570842afbe16bca5 | 7598900 |
| 251652675 | 0x04a91e01d951a38e89ee9c3d763002eb28c69992 | 8800000000000001      | 0xcf881556a2fdd7d0b0eaea737c13aa691d952d07 | 7598900 |
| 251652674 | 0x2a38d7eb55000b93f864d8dc5376cfcbbd2cf8bc | 4000210000000000000   | 0xc299d9751002af31f81e5af08b7d4c8204d81b07 | 7598900 |
| 251652673 | 0x5950c541c758d63b5101f8e46e70bd043d5cf515 | 1170000000000000      | 0xaeb13333d82cd70748edae06d3c30314d1006ed6 | 7598900 |
| 251652672 | 0x0d0707963952f2fba59dd06f2b425ace40b492fe | 499300000000000000000 | 0x6e451fba6b96be294c5d84b4bff49b0f5c5308cc | 7598900 |
| 251652671 | 0xfd54078badd5653571726c3370afb127351a6f26 | 999000000000000       | 0x53b10246f246d7aaf55bc880b583acbc04bb2c15 | 7598900 |
| 251652670 | 0x915080d385ae9457882fc2afa45d27a8bf9a764c | 823000000000000000    | 0xeccc2a045a5c141a40b215925546ce97139c8ba3 | 7598900 |
| 251652669 | 0xf056f435ba0cc4fcd2f1b17e3766549ffc404b94 | 8443371000000000000   | 0x515b16a3f0b739d583ac23f8b2f4a219189e0c24 | 7598900 |
+-----------+--------------------------------------------+-----------------------+--------------------------------------------+---------+
10 rows in set (0,00 sec)
```

--- 
# Difficulté
*Arrivé au bloc 7598900, la table sql totalise pas moins de 32Go de données. C'est malheureusement trop pour être 
stocké sur un ordinateur. Nous décidons donc de basculer notre mySQL sur le disque dur.*

### 1. Determiner la taille de la table SQL
```shell script
mysql> SELECT
  TABLE_NAME AS `Table`,
  ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024) AS `Size (MB)`
FROM
  information_schema.TABLES
WHERE
    TABLE_SCHEMA = "ETH"
ORDER BY
  (DATA_LENGTH + INDEX_LENGTH)
DESC;

+------------+-----------+
| Table      | Size (MB) |
+------------+-----------+
| tx         |     32252 |
| addrQL     |      3050 |
| block_info |       367 |
+------------+-----------+
3 rows in set (0,54 sec)
```

### 2. Changer le datadir en ayant installer mysql avec HomeBrew
```shell script
mysql> select @@datadir; # 0. Voir ou sont stocké les données
~ brew services stop mysql # 1. Stop mysql
~ sudo nano /usr/local/Cellar/mysql/8.0.22_1/homebrew.mxcl.mysql.plist
# 2. remplacer --datadir=/usr/local/var/mysql par --datadir=/Volumes/ETH/.mysql/mysql 
~ cp -r /usr/local/var/mysql /Volumes/ETH/.mysql/
~ brew services start mysql # Restart mysql
```

### 3. Exporter/Importer une table SQL
```shell script
mysqldump -p --user=username dbname tableName > tableName.sql
mysql -u username -p -D dbname < tableName.sql
```

On tire les conclusions suivantes:
- 32 Go de données, c'est beaucoup trop, les requêtes sont très longues, de même pour l'importation/exportation des données. Il faut revoir nos critères d'insertions 
- Étant donné la complexité que représente l'utilisation de Mysql en locale, il vaut mieux rester sur du mysql avec Docker.

`SOURCE`:
- https://chartio.com/resources/tutorials/how-to-get-the-size-of-a-table-in-mysql/
- https://stackoverflow.com/questions/17756973/change-mysql-db-location-when-installed-with-homebrew
- https://stackoverflow.com/questions/18741287/mysqldump-exports-only-one-table

