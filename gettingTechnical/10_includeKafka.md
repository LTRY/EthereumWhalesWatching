
# 10 . Utiliser Kafka pour gérer les flux de données lors de la synchronisation de la blockchain


### Objectifs
- Comprendre pourquoi on restera toujours bloqué 60-100 blocs derièrre la blockchain officielle.
- Mettre au point un croquis de la solution avec docker et kafka


## Pourquoi la synchronisation ne se terminera jamais avec notre solution

On remarque que notre noeud ne termine pas sa synchronisation, il reste en quelque sorte bloqué 100 blocs dernière. Il s'agit de quelque chose que l'on ne pourrat changer. 
En effet, même avec une très bonne connection à internet, il n'est pas possible de compléter la synchronisation de la blockchain ethereum sur un HDD. Ceci est du a la limitation d'écriture/lecture du disque.

`explications`:
- Le mode de synchronisation par défaut de Geth est appelé fast sync. C'est la mode de synchronisation que nous avons choisit car c'est le plus rapide.
- Au lieu de partir du bloc de genèse et de retraiter toutes les transactions qui se sont produites, la fast sync télécharge les blocs et ne vérifie que la preuve de travail associée. Le téléchargement de tous les blocs est une procédure simple et rapide.
- Avoir les blocs ne veut pas dire être synchronisé. Puisque aucune transaction n'a été exécutée, nous n'avons donc aucun état de compte disponible (c'est-à-dire soldes, nonces, code de contrat intelligent et données). Ceux-ci doivent être téléchargés séparément et vérifiés avec les derniers blocs. Cette phase s'appelle le `state trie download ` et elle s'exécute en fait en même temps que les téléchargements de blocs.
- Le `state trie` est un schéma complexe de centaines de millions de preuves cryptographiques. Pour vraiment avoir un nœud synchronisé, toutes les données des `accounts` doivent être téléchargées, ainsi que toutes les preuves cryptographiques pour vérifier que personne sur le réseau n'essaie de tricher. La partie où cela devient encore plus compliqué est que ces données se transforment constamment: à chaque bloc (15s), environ 1000 nœuds sont supprimés de ce trie et environ 2000 nouveaux sont ajoutés. Cela signifie que votre nœud doit synchroniser un ensemble de données qui change 200 fois par seconde. Le pire, c'est que pendant la synchronisation, le réseau avance et l'état que vous avez commencé à télécharger peut disparaître pendant le téléchargement, de sorte que votre nœud doit constamment suivre le réseau tout en essayant de collecter toutes les données récentes. Mais tant que vous n'avez pas collecté toutes les données, votre nœud local n'est pas utilisable car il ne peut rien prouver de manière cryptographique concernant les comptes.
- Le state trie d'Ethereum contient des centaines de millions de nœuds, dont la plupart prennent la forme d'un seul hash référençant jusqu'à 16 autres hashs. C'est une très mauvaises façon de stocker des données sur un disque, car il n'y a presque pas de structure, juste des nombres aléatoires faisant référence à des nombres encore plus aléatoires. C'est problématique car cela ne permet pas d'optimiser le stockage et la recherche des données de manière significative.

*En conclusion, notre noeud ethereum restera coincée 60 à 100 blocs dernières la blockchain officielle. Cela ne nous pose pas plus de soucis que ca, cela voudra juste dire que nos analyses en temps réelles sur la blockchain auront un décalage de 10 minutes.*


## Pourquoi utiliser Kafka?

Apache Kafka est un projet open-source écrit en Scala, il est entretenu et développé par la fondation Apache Software. 
Kafka est un système de gestion de flux de donnée en temps réel et à faible latence. Dans notre cas, il nous est utile car les requêtes faites sur la blockchain, le traitement ainsi que l'écriture de ces réponses dans une base de donnée externe ne se fait pas à la même vitesse. Il est donc préférable d'effectuer ces actions de manière asynchrone, nous délégeons cette tâche à Apache Kafka qui s'execute dans un conteneur.
Même si l'utilisation de ce logiciel requière une grosse capacité de mémoire vive, une des raisons qui nous a poussé à l'utiliser dans notre solution est ca facilité d'intégration en temps que conteneur Docker. 

`étapes`:
- Faire tourner un noeud Geth
- Lancer le conteuneur Kafka
- Lancer un conteuneur mongodb
- Executer le script `producer.py` et`consumer.py`

## 1. Faire tourner un noeud Geth
```shell script
~ geth --syncmode full --nousb --cache 4096 --datadir=/Volumes/ETH/.testeth \
  --ipcpath=~/IPC/geth.ipc --http --http.api eth,web3,personal --graphql
```

## 2. Lancer le conteuneur Kafka
`docker-compose.yml`:
```yaml
version: '2'

services:
  # this is our v1 cluster.
  kafka-cluster:
    image: landoop/fast-data-dev
    environment:
      ADV_HOST: 127.0.0.1         # Change to 192.168.99.100 if using Docker Toolbox
      RUNTESTS: 0                 # Disable Running tests so the cluster starts faster
      FORWARDLOGS: 0              # Disable running 5 file source connectors that bring application logs into Kafka topics
      SAMPLEDATA: 0               # Do not create sea_vessel_position_reports, nyc_yellow_taxi_trip_data, reddit_posts topics with sample Avro records.
    ports:
    - 2181:2181                 # Zookeeper
    - 3030:3030                 # Landoop UI
    - 8081-8083:8081-8083       # REST Proxy, Schema Registry, Kafka Connect ports
    - 9581-9585:9581-9585       # JMX Ports
    - 9092:9092                 # Kafka Broker
```
```shell script
~ docker-compose up
```

## 3. Lancer un conteuneur mongodb
```shell script
~ docker run --name mongodb -v /Volumes/ETH/mongotest:/data/db -p 27017:27017 -d mongo
```

## 4. Executer le script `producer.py` et`consumer.py`

`producer.py`:
```python
from time import sleep
from json import dumps
from kafka import KafkaProducer
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from web3 import Web3
from pprint import pprint


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


if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/"))

    while True:
        if w3.eth.is_syncing():
            lastBlock = w3.eth.syncing['currentBlock']
            break
        sleep(5)

    while True:
        first_block = lastBlock
        lastBlock = w3.eth.syncing['currentBlock']
        if first_block == lastBlock:
            print(f'no new block, stuck at {lastBlock}')
        else:
            print(f'{first_block} to {lastBlock}')
            data = queryQL(first_block, lastBlock)
            producer.send('test', value=data)
        sleep(5)
```

`consumer.py`:
```python
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from pprint import pprint

consumer = KafkaConsumer(
    'test',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

client = MongoClient('localhost:27017')
collection = client.numtest.test

for message in consumer:
    message = message.value
    pprint(message)
    collection.insert_one(message)
    print('{} added to {}'.format(message, collection))
```


```shell script
~ python producer.py
~ python consumer.py
```

`CONCLUSION`:
- Kafka nous permet de lire et d'enregistrer les transactions de la blockchain de manière asynchrone. Ci-dessous, on peut voir un exemple de la solution en train de tourner

| ![Image](../img/shells_SK08.png) |
|:--:|
| *Solution running* |


`SOURCE`: 
- https://github.com/ethereum/go-ethereum/issues/16796  
- https://github.com/ethereum/go-ethereum/issues/20938     
- https://medium.com/big-data-engineering/hello-kafka-world-the-complete-guide-to-kafka-with-docker-and-python-f788e2588cfc
