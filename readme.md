
| ![Image](img/baleines.jpg) |
|:--:|
| *Ethereum Whales Watching* |


## Présentation du projet

essayer de repondre a ca: Les gens ont de l'interet pour le bitcoin, puis ont découvert eth. les baleines sont passé de BTC a ETH, why? on sait pas trop mais ca correspond a la periode du developpement de la defi. OK

- sujet
- enjeux
- etat de l'art

inclure en bas des bas concerné les refs ci-dessous:
- https://fc19.ifca.ai/preproceedings/130-preproceedings.pdf
- http://cs229.stanford.edu/proj2017/final-reports/5244232.pdf
- https://arxiv.org/pdf/2003.13399.pdf
- https://bitinfocharts.com/comparison/ethereum-transactions.html
- https://whale-alert.io

## Évolution du projet
#### 00 . [ Définition de la méthode à mettre en place](gettingTechnical/00_prequelle.md)
#### 01 . [ Utilisation de Docker: Explication/Installation](gettingTechnical/01_installDocker.md)
#### 02 . [ Télécharger la blockchain ethereum depuis Geth par Docker](gettingTechnical/02_dockerGeth.md)
#### 03 . [ Étude des fonctionalités de Geth](gettingTechnical/03_explorationGeth.md)
#### 04 . [ Retranscrire les transactions dans un conteuneur mysql en passant par python en local](gettingTechnical/04_gethToMysql.md)
#### 05 . [ Enrichir l'image officiel ethereum/client-go avec un interpreteur python](gettingTechnical/05_enrichGethImageWithPython.md)
#### 06 . [ Scrapper le premier million de blocs](gettingTechnical/06_firstConsequantScrap.md)
#### 07 . [ Scrapper le premier million de blocs avec GraphQL](gettingTechnical/07_sameButFaster.md)
#### 08 . [ Estimer le temps d'execution total du script](gettingTechnical/08_estimationForFollowingBlockScrap.md)
#### 09 . [ Créer la table Tx qui répertorie les transacions suspect](gettingTechnical/09_createTableTX.md)
#### 10 . [ Utilisation de Kafka: Explication/Installation](gettingTechnical/10_includeKafka.md)
#### 11 . [ Solution retenue](gettingTechnical/11_partialSolution.md)
#### 12 . [ Difficultés et perspectives d'évolutions](gettingTechnical/12_difficulties&Evolutions.md)

## Apercu de la solution finale


![Image](img/schemaSoluce.png)


![Image](img/solution.gif)

## TODO

- 08 estimation du temps d'exécution

- faire la partie présentation du sujet (comprendre la DeFi, la garder, pas la garder...)

- maybe merge 00 & 01

- finir 11 partial solutions + graphique
- finir 12 diff et evolutions


- faire le Readme.md





