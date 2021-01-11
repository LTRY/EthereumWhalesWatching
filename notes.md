
## Objectifs Pi2:
- comprendre la blockchain etehereum
- savoir manipuler les contracts eth
- do shit

![](https://media.giphy.com/media/o0vwzuFwCGAFO/giphy.gif)

**D'un point de vue technique:**
- faire un setup facile a répliquer

**Quelles informations ressortir du noeud?:**
- volume de trnansaction en ether
- qui font le plus d'echange
- identifier les adresses avec plus de fond
- être au courant de lorsque les gros players (re)commence à jouer avec de l'ether


# Steps

## Step I
run a full ethereum node
- dans un conteneur docker?

## Step II
- extraire les données du noeud et les ranger dans un conteneur sous forme de données SQL ou noSQL (à déterminer) -> why?

## Step III
extraire la donnée, la rafiner
- isole les exchanges
- isole les individuts
- pour les mvt en ethers
- correler les mvts avec ...

## Step IV

![](https://media.giphy.com/media/mLpLzy2XWIN3y/giphy.gif)

## Other Steps (To Determine)
- se pencher sur ERC20
- extraire les tokens

## In the end
pour un nombre de token fini [(disons 10)](https://github.com/LTRY/eth_whales/blob/main/list%20token.md):

- list des players & baleines pour les ethers -> seems hard
- list de players & baleines pour les tokens -> seems harder
- list des players & baleines sur plusieurs tokens -> seems easy si on prend comme base les whales eth déjà spotté en step 1

- regarder les contracts plus exotiques (liquidity mining)

## WalkTrought

1. What is DeFi? -> [DeFi.md](https://github.com/LTRY/eth_whales/blob/main/DeFi.md)

2. Comment mesurer sont ampleure? [mesurer la DeFi.md](https://github.com/LTRY/eth_whales/blob/main/mesurer%20la%20DeFi.md)

3. La couille dans le paté [distribution inégale des tokens DeFi.md](https://github.com/LTRY/eth_whales/blob/main/distribution%20inégale%20des%20tokens%20DeFi.md)

4. Faire la liste des principaux holders d'un token ERC-20 [ERC-20 Holder List - Method.md](https://github.com/LTRY/eth_whales/blob/main/ERC-20%20Holder%20List%20-%20Method.md)



- graph newly created address by block
- graph time-computed for block retrievement. seconde passer sur 100 blocs 
- est-ce que le nombre de blocs par requete influt sur la perf?
