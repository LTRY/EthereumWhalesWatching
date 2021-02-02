
# 05 . Enrichir l'image ethereum/client-go avec un interpréteur python

### Objectif
- Intégrer python et ses dépendances dans l'image geth.

Le but ici est de comprendre qu'il y a différentes façons de se connecter à un noeud de la blockchain ethereum. 
La méthode la plus rapide pour se connecter à un noeud en locale est IPC. Mais l'utilisation de celle-ci vient avec son lot de difficultés.  
Quoi qu'il arrive, nous aurions eu tôt ou tard à créer un conteneur pour exécuter nos scripts python. Pour rappel, un des objectifs de ce projet est de le rendre le plus portable possible.  
Aujourd'hui, nous faisons le choix de garder une structure à 2 containers (geth enrichit & mysql)  


## 1. Pourquoi est-il préférable de se connecter via IPC?

Il existe 3 façons principales pour se connecter à un noeud Ethereum :

- IPC (utilise un système de fichiers local : plus rapide et plus sûr).
- Websockets (fonctionne à distance, plus rapidement que le HTTP).
- HTTP (plus de nœuds le soutiennent).

source: https://web3py.readthedocs.io/en/stable/providers.html


## 2. Comment dialoguer avec la blockchain via IPC?

Tout d'abord, un fichier geth.ipc est généré lors du boot du noeud c'est à dire lors de l'éxécution de la commande *geth*.  

On peut alors accéder au noeud par:
- la console javascript:
````shell script
geth attach ipc:/path/to/geth.ipc
````
- la librairie web3 de python3
```python
from web3 import Web3
web3 = Web3(Web3.HTTPProvider("/path/to/geth.ipc"))
print(web3.isConnected())
```

---

Le problème ici, c'est que notre solution fonctionne par l'intermédiaire de containers Docker.
Et le container qui éxécute le client geth se lance de cette façon:
```shell script
~ docker run -ti --name eth2 -v /mnt/usb/.ethereum:/root \
  -p 127.0.0.1:8545:8545 -p 30303:30303 \
  -d eth_image:latest --maxpeers=0
```
\
Le conteuneur crash. En regardant dans les logs, on voit cette erreur.
```shell script
~ docker logs -f eth2
  ...
  Fatal: Error starting protocol stack: listen unix /root/.ethereum/geth.ipc: bind: operation not permitted
  ...
```

Il semblerait que geth n'apprécie pas le fait de sortir le fichier geth.ipc du container (tout du moins de l'écrire sur le disque dur). 
Afin de palier à ce problème, on ajoute le paramètre `--ipcpath=/IPC/geth.ipc` à la commande geth. On obient alors:
```shell script
docker run -ti --name eth2 -v /mnt/usb/.ethereum:/root \
  -p 127.0.0.1:8545:8545 -p 30303:30303 \
  -d eth_image:latest --ipcpath=/IPC/geth.ipc --maxpeers=0
```

De cette façon, le fichier IPC reste dans le container et on garde les chaindatas de la blockchain sur notre disque dur **mais on perd donc l'accès au noeud depuis notre machine MacOS par l'intermédiare IPC.**  
En effet, il n'est pas possible de faire directement référence à un fichier inscrit dans un container depuis notre machine locale.
Cela implique que l'éxécution de scripts dialoguant par IPC, python ou non, **devra s'exécuter à l'intérieur du container** qui fait tourner le noeud geth.  
Cela soulève plusieurs interrogations, à savoir:
- Est-t'il possible de dialoguer par IPC depuis l'extérieur du container, la machine host ou bien même un autre container?
- Faut-il créer un container avec une image python ?
- L'enrichissement de l'image go-ethereum/ethereum est-il une bonne idée, cela pourrait-il engendrer des problêmes?

`NOTE`: Il est possible de rajouter l'argument -v `~/local/machine/geth.ipc:/IPC/geth.ipc` dans la commande docker afin de 
linker le fichier .ipc à notre système de fichiers local. De cette façon, on peut faire appel au fichier. 
Mais pour une raison que nous ignorons, l'éxécution des scripts ci-dessous retourne une erreur.

```python
from web3 import Web3
web3 = Web3(Web3.IPCProvider("/IPC/geth.ipc"))
print(web3.isConnected()) # FALSE
```

On retiendra donc la solution d'éxécuter nos scripts python directement dans le container.


## 3. Intégration de python, web3 & pymysql dans l'image geth

Maintenant que nous avons décidé d'éxécuter nos scripts python directement dans le même container que geth, 
nous devons enrichir la sous-image `apline` de l'image `go-ethereum/client`. Ce n'est pas une suprise qu'alpine soit déjà présent, 
et cela nous facilite quelque peu la tâche.
Alpine est un *very lightweight Os*, ce qui veut dire que très peu de fichiers fonctionnent dessus. Python n'en fait pas parti et l'outil pour installer ses dépendences non plus.

Auparavant, la création un container docker geth depuis l'image `go-ethereum/client` revenait juste à `pull` l'image puis à monter le container.
```shell script
~ docker pull go-ethereum/client
~ docker run -ti [args] -d go-ethereum/client [args]
```

---

Maintentant, si nous voulons enrichir l'image, nous devons la `build` depuis le code source. On import donc la dernière version du répertoire Github (disponible à cette adresse: ). On modifie ensuite le `Dockerfile` à notre convenance.  

`NOTE`: On se rend vite compte d'une certaine maladresse. En effet, si nous voulons faire une mise à jour de l'image, il faut répeter les opérations qui suivront. 
Mais pour l'instant, on s'en tient à cette solution.

Voici le `Dockerfile` qui permet de créer l'image `go-ethereum/client` officielle.

`Dockerfile`:
```Dockerfile
# Build Geth in a stock Go builder container
FROM golang:1.15-alpine as builder

RUN apk add --no-cache make gcc musl-dev linux-headers git

ADD . /go-ethereum
RUN cd /go-ethereum && make geth

# Pull Geth into a second stage deploy alpine container
FROM alpine:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /go-ethereum/build/bin/geth /usr/local/bin/

EXPOSE 8545 8546 30303 30303/udp
ENTRYPOINT ["geth"]
```

---

Maintenant, installer python3 revient à ajouter ces lignes:
```Dockerfile
RUN apk add --no-cache python3-dev && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
```

---

Et installer les dépendences pymysql & web3 revient à ajouter ces lignes. A préciser que pip installe de lui même les
dépendences python dont ce dernier a besoin, mais pas les packages de l'OS. Lors de l'éxécution des premiers `pip install ...` 
nous avons rencontré des erreurs d'éxécutions, il suffisait de debugger dans l'ordre des erreurs et d'installer de nouvelles libraries pour Alpine. 
```Dockerfile
RUN apk add --no-cache gcc && \
    apk add libc-dev openssl-dev libffi-dev &&\
    pip install cython web3 tqdm cryptography pymysql

```

---

Une fois toutes ces lignes ajoutées, on obient le `Dockerfile suivant`:

`UPDATED Dockerfile`:
```Dockerfile
# Build Geth in a stock Go builder container
FROM golang:1.15-alpine as builder

RUN apk add --no-cache make gcc musl-dev linux-headers git

ADD . /go-ethereum
RUN cd /go-ethereum && make geth

# Pull Geth into a second stage deploy alpine container
FROM alpine:latest

RUN apk add --no-cache ca-certificates && \
    apk add --no-cache gcc && \
    apk add --no-cache python3-dev && \
    apk add libc-dev openssl-dev libffi-dev &&\
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    pip install Cython && pip install web3 && pip install tqdm && pip install cryptography && pip install pymysql

COPY --from=builder /go-ethereum/build/bin/geth /usr/local/bin/

EXPOSE 8545 8546 30303 30303/udp
ENTRYPOINT ["geth"]
```

---

On se positionne dans le répertoire qui contient ce fichier et on éxécute la commande suivante:
```shell script
~ docker build -t eth_image .
```

La création de l'image prend un peut de temps. Puis, on monte le conteneur geth avec la commande:
```shell script
~ docker run -ti [args] -d eth_image [args]
```

On copie un fichier python depuis notre machine locale au container et on l'éxécute de cette façon:
```shell script
~ docker cp <local_path_to_python_script> <container_name>:<existing_container_path>
~ docker exec -ti <container_name> python3 <path_to_python_script>
```

---

`CONCLUSION`: nous sommes dorénavant capable d'éxécuter des scritps en python directement dans notre container geth 
et ainsi nous bénéficions d'un gain de temps d'éxécution.


`SOURCES`:
- https://ethereum.stackexchange.com/questions/1492/when-is-the-geth-ipc-file-produced
- https://ethereum.stackexchange.com/questions/74510/web3-py-cannot-connect-to-geth-dev-node-via-ipc
