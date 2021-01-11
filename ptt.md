## 1. Présentation et Analyse du sujet
Sujet, scope  
Enjeux -> Les gens ont de l'interet pour le bitcoin, puis ont découvert eth. les baleines sont passé de BTC a ETH, why? on sait pas trop mais ca correspond a la periode du developpement de la defi.  
Etat de l’art. -> ethereum c'est assez nouveau, pas grand chose de developper dessus, whalealert  
Attendus du partenaire en fin de projet. -> aller jusqu'ou vous pouvez.  
   
## 2. Gestion du projet
Organisation globale
Définition et répartition des tâches
Gestion du temps, des deadline, des risques Communication

## 3. Présentation technique
Justification des choix théoriques/techniques retenus Justification des choix théoriques/techniques rejetés
Tâches effectivement accomplies actuellement (y compris tests)
### Retenu
- utlisation Docker
- utlisation Geth
- utilisation Mysql
- utilisation Graphql
- utilisation kafka

### Rejeté
- retranscire tt les Txs dans sql -> 32go
- utlisation partielle Docker
- utilisation de l'image ethereum/client-go enrichit de python
- utilisation de rabbitMQ
- utlisation redis / mongodb

```
         ipc   http
rpc       fast slower
graphql  x    hyperfast
```


## 4. Résultats actuels obtenus en regard des résultats finaux attendus
Probabilité d’atteindre les résultats demandés,  oui.   il n'y avait de resultat 
niveau de confiance dans la dernière ligne droite du projet,  
probabilité de satisfaction du partenaire au moment de la clôture, avec justification
