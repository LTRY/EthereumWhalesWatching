# 02 . Télécharger la blockchain Ethereum avec Geth depuis docker sur MacOS

### Objectifs

- Expérimenter docker et geth
- Vérifier le téléchargement effectif de la blockchain
- Validé l'utilisation de docker pour notre projet

---

*Le but ici est pas noter les commandes qui nous serons utilise à l'expoloitation de Geth par Docker*

---

## Docker & Geth

Voici la commande qui permet de monter un container geth capable de télécharger la blockchain:

```shell script
docker run -ti -d \
  -v /Volumes/ETH/.ethereum:/root \
  -p 127.0.0.1:8545:8545 -p 30303:30303 ethereum/client-go --ipcpath=/IPC/geth.ipc \
  --http --http.api eth,web3,personal --http.addr "0.0.0.0"
```

`Arguments associé au container`:  
- `-v /Volumes/ETH/.ethereum:/root` permet d'écrire la blockchain sur notre disque dur externe
- `-p 127.0.0.1:8545:8545` permet la connection au noeud via HTTP
- `-p 30303:30303` est indispensable au client geth car il permet la connection entre les noeuds du réseau
- `ethereum/client-go` est le nom de l'image qui permet la conception du container

`Arguments associé à geth`:  
- `--ipcpath=/IPC/geth.ipc` spécifie l'emplacement du fichier IPC à l'intérieur du container
- `--http --http.api eth,web3,personal --http.addr "0.0.0.0" ` sont des arguments généraux qui permet l'accès au 
noeud et à ses différentes fonction via HTTP.
- `--maxpeers 0` stop la synchronisation si il est spécifié

`NOTE`: Il y a plusieurs désavantages à utiliser un HDD pour stocker la blockchain. Ici, nous spécifions le chemin du fichier IPC à l'intérieur du conteuneur de sorte à ne qu'il se retrouve pas sur le disque dur, car cela entraine une erreur. 

## Liste de commandes associé

Une fois que l'on a monté un container geth, nous pouvons effectuer quelques actions dessus

- Lister les différents containers UP
```shell script
docker ps
```
- Lister les différents containers UP & DOWN
```shell script
docker ps -a
```

- Faire défiler les logs du container spécifié. A tester avec `--tail=10` pour ne pas tout afficher
```shell script
docker logs -f dazzling_hodgkin
```

- Rentrer dans la console javascript de geth via ipc
```shell script
docker exec -it dazzling_hodgkin geth attach ipc:/IPC/geth.ipc
```

- Pas forcément utile: Le container geth ne vient pas avec une extension python. Dommage. Ce script récupère une variable 
depuis la console javascript et la fait passer en argument d'un script python éphémère. L'exercice était sympa ce pourquoi je la garde
```shell script
python3 -c 'import sys; import datetime; print(datetime.datetime.fromtimestamp(int(sys.argv[1][5:15])).strftime("%d/%m/%Y"))' \
  "$(docker exec -ti recursing_allen geth attach ipc:/IPC/geth.ipc --exec "eth.getBlock(eth.syncing.currentBlock).timestamp")"
```

- Vérifier l'avancement en % du téléchargement de la blockchain
```shell script
docker exec -ti recursing_allen geth attach ipc:/IPC/geth.ipc \
  --exec "eth.syncing.currentBlock / eth.syncing.highestBlock"
```


`CONCLUSION`:
*Cette facon de telecharger la blockchain semble fonctionner. Prochainement, nous .... Il semblerait que la synchronisation d'un noeud est un des plus gros challenge sur Ethereum*


`SOURCE`:
- https://populus.readthedocs.io/en/latest/dev_cycle.part-08.html
- https://medium.com/@andrenit/buildind-an-ethereum-playground-with-docker-part-2-docker-image-928f8ceaac50
- https://ethereum.stackexchange.com/questions/392/how-can-i-get-a-geth-node-to-download-the-blockchain-quickly
- https://ethereum.org/en/developers/docs/
- https://ethdocs.org/en/latest/index.html
- https://stackoverflow.com/questions/59340718/ethereum-which-syncmode-to-use-fast-or-full
- https://ethereum.stackexchange.com/questions/1161/what-is-geths-fast-sync-and-why-is-it-faster
- https://ethereum.stackexchange.com/questions/1556/geth-import-vs-copying-chaindata
- https://blog.slock.it/how-to-not-run-an-ethereum-archive-node-a-journey-d038b4da398b
- https://ethereum.stackexchange.com/questions/34979/geth-disk-and-memory-performance-analysis
- https://blog.slock.it/how-to-not-run-an-ethereum-archive-node-a-journey-d038b4da398b
- https://ethereum.stackexchange.com/questions/69915/copy-geth-full-node-onto-external-drive-then-continue-syncing
- https://kauri.io/run-an-ethereum-node-on-debian-with-an-external-ss/a73723dd2e924d8c948923709763f409/a

