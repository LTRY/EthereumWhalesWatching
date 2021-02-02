
# 07 . Scrapper le premier million de blocs avec GraphQL

### Objectifs
- scrapper les 1 000 000 premiers blocks de la blockchain ethereum avec GraphQL
- enregistrer les datas dans une table sql du disque dur


## Pourquoi utiliser GraphQL?

Les requêtes RPC, que ce soit via IPC, WS ou HTTP ont plusieurs inconvéniants:
- manque de specification
- Pas fortement dactylographié 
- sur-extrapolation / sous-extrapolation
- pas de concept de données et de relations

GraphQL est basé sur le protocol HTTP, ainsi, nous n'avons plus besoin de passer par IPC. Auparavant, nous devions travailler à l'intérieur du conteneur, 
en modifiant un peu l'image etherem/go-client. Ceci n'était pas une solution optimale, de plus, [nous recontrons de nombreux problèmes avec l'exploitation du conteneur GETH](12_difficulties&Evolutions.md#docker-image-ethereumclient-go-not-working). 
Nous avons décider de revenir à une solution avec Geth en locale.

## 1. Jusqu'ici

Comme dit précédémment, le scrapping du premier million de blocks de la blockchain ethereum représente une étape majeure. On ne s'occupe pas encore pour l'instant d'aller chercher les blocs au dessus pour 2 raisons:
- nous n'avons toujours pas réussit à télécharger la blockchain en entier
- nous sommes toujours en phase de test et d'exploration ce qui signifit que certainement nous serons amenés à 
retourner chercher d'autres infos et donc à répéter le processus.

Maintenant que nous maitrisons la technique la plus simple de récupération de données c'est à dire via RPC, nous nous attelons à 
une nouvauté de client ethereum geth sorti en juillet 2019: GraphQL.


`Etapes`:  
- On fait tourner notre client Geth en locale
- on monte le container sql on l'on stockera notre db et on créer la table ADDR
- on execute le script `scrap.py` en local et on attend un certain temps
- on observe le résultat dans le container sql

## 2. Rendre disponible le noeud Ethereum stocker sur notre HDD.
```shell script
~ geth --syncmode fast --nousb --cache 4096 --datadir=/Volumes/ETH/.ethereum/.ethereum \
   --ipcpath=~/IPC/geth.ipc --http --http.api eth,web3,personal --graphql --maxpeers 0
```

## 3. Monter le conteuneur SQL
```shell script
~ docker run -p 3306:3306 --name db2 -v ETH:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=pwd -d mysql --innodb-use-native-aio=0
~ docker exec -ti db2 mysql -uroot -p
mysql> create database ETH;
mysql> use ETH;
mysql> create table addrQL(`from` varchar(42) primary key, `value` varchar(30));
```

- On créer une table sql qui ne prend pas le nonce. Pour une raison, il apparait tout le temps "0x0"


## 4. On exécute le script scrap.py en local
`scrap.py`
```python
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from tqdm import tqdm
import time
import pymysql

START_BLOCK = 0
END_BLOCK = 6000000
PAD = 250


def queryQL(START_BLOCK, END_BLOCK):
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://127.0.0.1:8545/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

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
    result = client.execute(query)
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


if __name__ == '__main__':
    tt = time.time()
    main()
    print("\ntotal time exection: {}".format(time.time() - tt))
````
```shell script
100%|██████████| 3840/3840 [10:29<00:00,  6.10it/s]
```

## 5. On se rend dans le conteneur SQL et en tire nos observations
```shell script
mysql> select count(*) from addrQL;
+----------+
| count(*) |
+----------+
|    29378 |
+----------+
1 row in set (0.03 sec)
```

`CONCLUSION`:
- `good`: Le temps d'exécution est incroyablement plus rapide ~10min contre ~4h en requete http
- `bad`: On arrive malheureusement pas à récupérer les nonces. 
- `bad`: On ne retrouve que 29378 adresses avec cette méthode contre 30121 avec http


### Après avoir fait tourner le script sur plus de blocs..

Au 5414500 ème block, on contabilise 24 099 616 d'adresses ethereum unique. Nous pensions que le temps d'exécution serait 
relativement moins élevé puique qu'il nous a fallu pas loin de 6h d'éxécution. Il semblerait que la méthode GraqphQL soit 
efficace lorsqu'il s'agit des premiers blocs. Mais que celle-ci ait tout de même du mal à parcourir la fin de la blockchain ou les blocs sont plus grand. 
Il semblerait que le temps d'éxécution des requetes graphQL soient proportionelles à la taille des blocs, nous essayerons donc prochainement de déterminer le temps d'execution de notre script sur la blockchain complète.
```shell script
mysql> select count(*) from addrQL;
+----------+
| count(*) |
+----------+
| 24099616 |
+----------+
1 row in set (14,98 sec)
```


`SOURCES`:
- https://vsupalov.com/docker-shared-permissions/
- https://blog.ethereum.org/2019/07/10/geth-v1-9-0/
- https://github.com/shawntabrizi/ETH-Transaction-Graph
- https://cito.github.io/blog/shakespeare-with-graphql/
- https://eips.ethereum.org/EIPS/eip-1767
- https://github.com/ethereum/go-ethereum/tree/master/graphql

