
# Les Adresses Ethereum 


# Table of Contents
1. [Comment les addresses sur ethereum sont-elles créées](#methodes-d'acces-aux-transactions)
2. [Comment lister toutes les addresses sur ethereum](#methodes-d'acces-aux-transactions)
3. [Comment lister tous les détenteurs d'un token ERC](#methodes-d'acces-aux-transactions)
4. [Comment lister tous les tokens et leurs détenteurs associés](#methodes-d'acces-aux-transactions)

---

## 1. Comment les addresses ethereum sont-elles créées?

Les addresses sur ethereum peuvent être créées de 4 façons différentes:
- une transaction est envoyée à cette adresse.
- un appel de message est effectué à cette adresse dans le cadre d'un contrat.
- un bloc miné où l'adresse est spécifiée comme base de monnaie (destinataire de la récompense en bloc).
- de nouvelles adresses sont également créées lorsqu'un appel de message est effectué dans le cadre d'un contrat. Pour répertorier ces appels, chaque transaction doit être exécutée ou bien les traces de transaction doivent être inspectées.

## 2. Comment lister les adresses ethereum

1. obtenir tous les blocs
2. dans chaque bloc, obtenir toutes les transactions et regarder le "from" et le "to"
3. filtrer toutes les transactions ayant une valeur > 0
4. enregistrer la liste de toutes les adresses
5. filtrer les doublons
6. filtrer les adresses avec un solde de 0

`Note`:
un noeud synchronisé a en mémoire ce qui s'appelle le state trie qui contient toutes les informations en temps réel de qui possède quoi sur la blockchain, malheureusement, 
on ne peut pas l'analyser car les addresses sont hashées avant d'être inscrites dans l'arbre.

---

## 3. Liste des détenteurs de jetons ERC-20 

https://stackoverflow.com/questions/63553500/get-array-of-ownership-of-an-erc20.  
https://ethereum.stackexchange.com/questions/36274/a-list-of-token-holders-at-a-specific-time

## Est-il possible d'obtenir une liste des détenteurs de jetons pour un jeton ERC20 donné dans le cadre d'un autre solidity contract ?  

Il n'est pas possible d'obtenir une liste des détenteurs de jetons ERC20 directement à partir d'un contrat.  Les "balances" sont stockées dans une cartographie dont la pluspart sont des contrats ERC20, mais comme nous ne pouvons pas obtenir une liste de clés pour une cartographie dans Solidity, il est impossible de le faire sans intervention externe.  
Les jetons ERC-20 ne maintiennent pas une liste itérable des détenteurs de jetons actuels, le type de mappage utilisé nous permet uniquement de vérifier une adresse connue. Pour obtenir une liste de tous les détenteurs de jetons, nous devez la traiter hors ligne et la construire nous-même à partir des données de la chaîne de blocs. Il n'est pas possible de réaliser ce que nous souhaitons en utilisant uniquement la chaîne de blocs, mais une combinaison de logique on-chain/off-chain peut nous permettre d'atteindre nos objectifs.  
Il semble que nous devons passer en revue tous les événements de transfert pour un jeton ERC-20 spécifique. Cela semble très gourmand en ressources. Mais il semble que ce soit le seul moyen. Comme le montre cet exemple :
https://docs.tokenmarket.net/captable.html#cap-table-for-any-erc-20-token

---

## 4. Liste de tous les contrats et jetons associés à un compte

https://ethereum.stackexchange.com/questions/15372/how-can-i-view-all-the-tokens-and-contracts-associated-with-an-ethereum-address

D'où le fait qu'il faille choisir un nombre fini de tokens pour que ce ne soit pas trop gênant.

Et aussi https://stackoverflow.com/questions/49938672/web3-js-how-to-search-all-the-contracts-ever-created-by-and-address

---

SOURCES :
- https://medium.com/@piyopiyo/how-to-get-erc20-token-balance-with-web3-js-206df52f2561
- https://ethereum.stackexchange.com/questions/27809/how-to-list-all-ethereum-addresses-with-a-positive-balance
- https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_tracetransaction
- https://ethereum.stackexchange.com/questions/40254/getting-complete-state-of-a-smart-contract/40280#40280
