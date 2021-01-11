
# Decentralized Finance

### Qu'est-ce que la DeFi?
La DeFi est l'ensemble des applications de services financiers qui se base sur des technologies décentralisées comme la blockchain. Les projets DeFi visent à fournir des services financiers sans avoir recours à une tierce personne ou à une instution dite centralisée.  
Reprendre des concepts de la finance traditionnelles, emprunt, assurance, la bourse. Plus de transparence dans la gouvernance.  

### Comment mesurer le succès de la DeFi?  
Le succès d'un projet de la DeFi est souvent évalué par sa *Total Value Locked (TVL)* - Valeur Totale Verrouillée - en $.  
Par ailleurs, cette métrique est considérée comme la capitalisation boursière de l'ensemble de l'écosystème de la DeFi.  
Voir article (...)

| ![Image](img/defi_pulse_13:10:2020.png) |
|:--:|
| *Screenshot du site [DeFi Pulse](https://defipulse.com) le 13/10/2020* |

### Pourquoi 96% des apllications de la DeFi sont écrit sur la blokchain Ethereum ?
Les applications DeFi sont principalement écritent avec la blockchain ethereum car celle-ci permet l’écriture de smart contracts avec le langage Solidity, qui est suffisamment mature et contient la logique nécessaire à la création de ces apps.  
Ethereum a l’écosystème autour des smarts contracts le plus développé. 



## Milestones
- `Décembre 2017` : Lancement du Ethereum-based protocol [MakerDao](https://makerdao.com/en/).  
- `Août 2018`:  Le terme DeFi surgit d'une conversation Telegram entre les devs et entrepreneurs d'ETH.  
- `Septembre 2018` : Lancement Compound Finance (COMP)
- `Novembre 2018` : Lancement Uniswap (UNI)
- `Février 2019` : Lancement de Synthetix on the mainnet
- `Janvier 2020`: Lancement de Curve
- `Février 2020` : Lancement Year.Finance
- `Mars 2020` : Lancement Balancer(BAL)
- `Août 2020` : **Huobi DeFi Labs**, initiative de l’exchange singapourien **Huobi**, créée la **Global DeFi Alliance**. A l’origine elle rassemblait uniquement les projets **MakerDAO** (MKR), **Compound** (COMP), **Nest** (NEST) et **dYdX** (dYdX).  
- `Septembre 2020`: 10 nouveaux membres ont rejoint le consortium DeFi : Curve, Aave, Synthetix, Loopring, Zapper, Zerion, Bitpie, Mykey et CoinGecko.
	
La Global DeFi Alliance vise à promouvoir la collaboration au sein d’un écosystème encore très nouveau et particulièrement hétéroclite. Plus précisément, il s’agit de rapprocher l’Orient de l’Occident, selon Sharlyn Wu, le responsable de l’investissement chez Huobi :  
> « Nous ressentons fortement l’isolement entre les exchanges centralisés, les institutions financières et la communauté globale, et nous voulons combler ce gouffre. [Nous ressentons] aussi les grandes différences culturelles entre l’Est et l’Ouest, et nous pensons qu’il en va de notre responsabilité de rassembler la communauté. »

On liste 5 types d'application différentes dans la DeFi:
- Decentralized exchanges
– Derivatives
– Stable Coins 
– Lending & Borrowing
– Margin Trading
– Assurance


## I . Decentralized Exchanges DEXES
Liquidity Pool Based Dex :  
_Il faut de la liquidité pour faire ces échanges décentralisés. Donc on prête des cryptos à la blockchain. On prête et on recoit un token qui prouve qu’on a prêté._
-	UNISWAP: Permet d’échanger des tockens ERC20 contre ERC20
-	Kyber network
-	Bancor
- food tokens (SushiSwap -> PizzaCoin -> Sake) -> Ceux qui vont arriver en dernier finance ceux qui sont arriver en premier.  

Order Book Based Dex :
-	Loopring
-	Idex

## II. Derivatives
`Synthetix`: Trading décentralisé , Provides on-chain exposure to different assests


## III. Margin Trading
Augmenter la position d’un asset en empruntant des fonds.  
`dy/dx`
`Fulcrum`

## IV. Insurrances
_Unslashed_
Donne des garanties de compensation.  
Protection contre le fail de smart contracts.  
`Nexus Mutual`
`Opyn`


## V. Lending & Borrowing
__Lending__:  
_les détenteurs de tokens ERC-20 peuvent prêter leurs assets pour que d'autre empruntent monaillant un certain taux._  

__Borrowing__:  
_L'idée n'est donc pas de d'emprunter de la liquidité et d'en rebourser une partie tous les mois comme dans la finance traditionelle centralisé._  
_Il s'agit de mettre sous séquestre des jetons que l'on possède et qui servent de caution à un emprunt de ce même token ou d'autre dans une proportion moindre._  

Instinctivement, mettre sous séquestre un quantité d'asset pour en emprunter une quantité moindre est une opération qui parait peu lucrative et ne guère résonner avec la définition du terme emprunt.  
Pourtant, on peut voir plusieurs cas d'usage à l'utilisation de ses services:

- Un acteur possède une certaine quantité de tokens et pour une quelquonque raison, il ne veut pas s'en séparer et a besoin d'autre tokens pour d'autres activités.
- Un acteur spécule sur la hausse d'un asset, il met sous séquestre cet asset et en obtient d'autre en échange. Si la hausse de l'asset compense le taux d'emprunt ou bien le bénéfice de l'activité résultante de l'asset emprunté fait de même, l'emprunteur s'y trouve gagant. 

On distingue 2 types d'applications qui proposent ce service:
- centralisé: (Crypto.com, binance) dont le mécanisme est opaque et dont les taux d'emprunts et de staking sont élevés et relativement fixe
- décentralisé (Compound) ou le mécanisme est régit selon un protocole open-source mais qui reste excessivement complexe. La dynamique de marché (offre/demande) dicte les taux et sont donc moins important que sur les exchanges centralisés car beaucoup moins utilisé. Un système de gouvernance peut aussi pondérer les taux.

`Note`: _Il est curieux de remarque que les baleines sont particulièrement investi dans ces projet_ --> [link to another page](https://github.com/LTRY/eth_whales/blob/main/distribution%20inégale%20des%20tokens%20DeFi.md)

__Compound__:  
biggest DeFi lending Project.  
Autonomous algorithmic interest rate protocol.  

__AAVE__:  
Collateral for borrowing another asset  

## VI. StableCoin
-	Algorithmic stable coin (DAI)
-	Non-algotihmic stable coins (USDC – USDT) – centralized


# Acteurs majeur de la DeFi:
- `MarkerDao`:  
Une des premières applis de finance décentralisées. Lock in collatéral et obtenir du Dai. 


source: https://coinmarketcap.com/alexandria/article/what-is-decentralized-finance
- https://medium.com/@jgm.orinoco/understanding-erc-20-token-contracts-a809a7310aa5
- https://www.dappuniversity.com/articles/web3-js-intro