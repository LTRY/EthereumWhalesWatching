
# [Trouver un titre]



# Table of Contents
0. [Comment les addresses sur ethereum sont-elles créées](#methodes-d'acces-aux-transactions)
1. [Comment lister toutes les addresses sur ethereum](#methodes-d'acces-aux-transactions)
2. [Comment lister tous les détenteurs d'un token ERC](#methodes-d'acces-aux-transactions)
3. [Comment lister tous les tokens et leurs détenteurs associés](#methodes-d'acces-aux-transactions)


---

## 0. Comment les addresses ethereum sont-elles créer?

Les addresses sur ethereum peuvent être créer de 4 façons différentes:
- a transaction is sent to this address
- a message call is made to this address within some contract
- a block mined where the address is specified as the coinbase (receiver of the block reward)
- New addresses are created also when a message call is made inside some contract. To list these calls every transaction has to be executed or transaction traces must be inspected


## 1. How to list ALL Ethereum addresses

1. get all the blocks
2. from each block get all the transactions et regarder le `from` et le `to`
3. filter all the transactions with a value > 0
4. record the list of all the to addresses
5. filter out duplicates
6. filter out addresses with balance 0


`Note`:
un noeud synchronisé à en mémoire ce qui s'appelle le state trie qui est contient toutes les informations à jour de qui possède quoi sur la blockchain, malheureusement, 
on ne peut pas l'analyser car les addresses sont hasher avant d'être inscrit dans l'arbre

---

## 2. ERC-20 Tokens Holders List 

https://stackoverflow.com/questions/63553500/get-array-of-ownership-of-an-erc20.  
https://ethereum.stackexchange.com/questions/36274/a-list-of-token-holders-at-a-specific-time

## Is it possible to get a list of token holders for a given ERC20 token from within another solidity contract?  

It is not possible to get a list of ERC20 token holders directly from a contract.  "Balances" are stored in a mapping in most ERC20 contracts but as we cannot get a list of keys for a mapping in Solidity, therefore it is impossible without external intervention.  
ERC-20 tokens do not maintain an iterable list of current token holders, the used mapping type allows you only to check for a known address - balance. To get a list of all token holders, you need to process this offline and build it yourself from blockchain data.
It is not possible to accomplish what you desire using only the blockchain, but using a combination of on-chain/off-chain logic can achieve your goals.  

Seems like you need to walk through all Transfer events for a specific ERC-20 token. That sounds very resource-intensive. But it seems to be the only way. Watch this exmaple: https://docs.tokenmarket.net/captable.html#cap-table-for-any-erc-20-token

---

## 3. List all contract & token associated to an account

https://ethereum.stackexchange.com/questions/15372/how-can-i-view-all-the-tokens-and-contracts-associated-with-an-ethereum-address

D'ou le fait qu'il va falloir choisir un nombre fini de token pour pas que ca soit trop embetant.

Also https://stackoverflow.com/questions/49938672/web3-js-how-to-search-all-the-contracts-ever-created-by-and-address

---

SOURCE:
- https://medium.com/@piyopiyo/how-to-get-erc20-token-balance-with-web3-js-206df52f2561
- https://ethereum.stackexchange.com/questions/27809/how-to-list-all-ethereum-addresses-with-a-positive-balance
- https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_tracetransaction
- https://ethereum.stackexchange.com/questions/40254/getting-complete-state-of-a-smart-contract/40280#40280
