```python
import pandas as pd
from web3 import Web3
from pprint import pprint
```


```python
infura_url = "https://mainnet.infura.io/v3/9d104517caec45d49c818fe50063aaed"
```


```python
web3 = Web3(Web3.HTTPProvider(infura_url))
```


```python
print(web3.isConnected())
```


```python
data= pd.DataFrame()
last_block = web3.eth.blockNumber
j = 0
for i in range(0,10):
    informations = web3.eth.getBlock(last_block-i) #toutes les informations sur le block
    HexBytes = informations.transactions #toutes les transactions
    for HexBytes in HexBytes:
        transaction = web3.eth.getTransaction(HexBytes)#nous donne les infos sur la transaction
        if transaction['nonce']>1000:
            adresse = transaction['from']
            balance = web3.eth.getBalance(adresse) #donne le resultat en wei
            balance = web3.fromWei(balance,'ether') #nombre d'ether de l'adresse
            if int(balance)>1000:
                data.loc[j,"adresse"] = adresse
                data.loc[j,"quantité"] = int(balance)
                j= j+1
data.head(126)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>adresse</th>
      <th>quantité</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0x4eF5C587e53c66cdfBC6588E29DCb100A5859263</td>
      <td>3412.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0xFa453aec042a837e4AEBbADAB9d4E25B15FAd69D</td>
      <td>1148.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0xCdEF4F34E5CEb46C7c55134Cda34273349bE65b7</td>
      <td>1583.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0x97122dDca38c29b7653D52b07998d06a7128fa0B</td>
      <td>4569.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0x28FFE35688fFFfd0659AEE2E34778b0ae4E193aD</td>
      <td>8817.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>122</th>
      <td>0x9FCaFcca8aec0367abB35fBd161c241f7b79891B</td>
      <td>2209.0</td>
    </tr>
    <tr>
      <th>123</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157071.0</td>
    </tr>
    <tr>
      <th>124</th>
      <td>0x3e9AFaA4a062A49d64b8Ab057B3Cb51892e17Ecb</td>
      <td>1391.0</td>
    </tr>
    <tr>
      <th>125</th>
      <td>0x2819c144D5946404C0516B6f817a960dB37D4929</td>
      <td>8602.0</td>
    </tr>
    <tr>
      <th>126</th>
      <td>0x4FED1fC4144c223aE3C1553be203cDFcbD38C581</td>
      <td>1228.0</td>
    </tr>
  </tbody>
</table>
<p>127 rows × 2 columns</p>
</div>




```python
data.head(50)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>adresse</th>
      <th>quantité</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0x4eF5C587e53c66cdfBC6588E29DCb100A5859263</td>
      <td>3412.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0xFa453aec042a837e4AEBbADAB9d4E25B15FAd69D</td>
      <td>1148.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0xCdEF4F34E5CEb46C7c55134Cda34273349bE65b7</td>
      <td>1583.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0x97122dDca38c29b7653D52b07998d06a7128fa0B</td>
      <td>4569.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0x28FFE35688fFFfd0659AEE2E34778b0ae4E193aD</td>
      <td>8817.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0x73f8FC2e74302eb2EfdA125A326655aCF0DC2D1B</td>
      <td>206447.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0xFB90501083a3b6AF766c8dA35d3Dde01eB0d2a68</td>
      <td>2927.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>0x564286362092D8e7936f0549571a803B203aAceD</td>
      <td>19313.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>0x0681d8Db095565FE8A346fA0277bFfdE9C0eDBBF</td>
      <td>18759.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>0x0681d8Db095565FE8A346fA0277bFfdE9C0eDBBF</td>
      <td>18759.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>0x0681d8Db095565FE8A346fA0277bFfdE9C0eDBBF</td>
      <td>18759.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>0xD551234Ae421e3BCBA99A0Da6d736074f22192FF</td>
      <td>31164.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>0x0681d8Db095565FE8A346fA0277bFfdE9C0eDBBF</td>
      <td>18759.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0x564286362092D8e7936f0549571a803B203aAceD</td>
      <td>19313.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>0xD551234Ae421e3BCBA99A0Da6d736074f22192FF</td>
      <td>31164.0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157684.0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>0x564286362092D8e7936f0549571a803B203aAceD</td>
      <td>19313.0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>0x986a2fCa9eDa0e06fBf7839B89BfC006eE2a23Dd</td>
      <td>3438.0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>0x986a2fCa9eDa0e06fBf7839B89BfC006eE2a23Dd</td>
      <td>3438.0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>0x0D0707963952f2fBA59dD06f2b425ace40b492Fe</td>
      <td>67681.0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>0x0D0707963952f2fBA59dD06f2b425ace40b492Fe</td>
      <td>67681.0</td>
    </tr>
    <tr>
      <th>30</th>
      <td>0xCdEF4F34E5CEb46C7c55134Cda34273349bE65b7</td>
      <td>1583.0</td>
    </tr>
    <tr>
      <th>31</th>
      <td>0x61189Da79177950A7272c88c6058b96d4bcD6BE2</td>
      <td>65039.0</td>
    </tr>
    <tr>
      <th>32</th>
      <td>0xeB6c4bE4b92a52e969F4bF405025D997703D5383</td>
      <td>2070.0</td>
    </tr>
    <tr>
      <th>33</th>
      <td>0x97122dDca38c29b7653D52b07998d06a7128fa0B</td>
      <td>4569.0</td>
    </tr>
    <tr>
      <th>34</th>
      <td>0xA694068FDfd382FA60c249e9A2B92a5548aD50EF</td>
      <td>1922.0</td>
    </tr>
    <tr>
      <th>35</th>
      <td>0xA694068FDfd382FA60c249e9A2B92a5548aD50EF</td>
      <td>1922.0</td>
    </tr>
    <tr>
      <th>36</th>
      <td>0x0681d8Db095565FE8A346fA0277bFfdE9C0eDBBF</td>
      <td>18759.0</td>
    </tr>
    <tr>
      <th>37</th>
      <td>0x0681d8Db095565FE8A346fA0277bFfdE9C0eDBBF</td>
      <td>18759.0</td>
    </tr>
    <tr>
      <th>38</th>
      <td>0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE</td>
      <td>157681.0</td>
    </tr>
    <tr>
      <th>39</th>
      <td>0x564286362092D8e7936f0549571a803B203aAceD</td>
      <td>19308.0</td>
    </tr>
    <tr>
      <th>40</th>
      <td>0x564286362092D8e7936f0549571a803B203aAceD</td>
      <td>19308.0</td>
    </tr>
    <tr>
      <th>41</th>
      <td>0xD551234Ae421e3BCBA99A0Da6d736074f22192FF</td>
      <td>31164.0</td>
    </tr>
    <tr>
      <th>42</th>
      <td>0xD551234Ae421e3BCBA99A0Da6d736074f22192FF</td>
      <td>31164.0</td>
    </tr>
    <tr>
      <th>43</th>
      <td>0x27E9F4748a2eb776bE193a1F7dec2Bb6DAAfE9Cf</td>
      <td>90681.0</td>
    </tr>
    <tr>
      <th>44</th>
      <td>0x58c2cb4a6BeE98C309215D0d2A38d7F8aa71211c</td>
      <td>37970.0</td>
    </tr>
    <tr>
      <th>45</th>
      <td>0xCAc725beF4f114F728cbCfd744a731C2a463c3Fc</td>
      <td>217541.0</td>
    </tr>
    <tr>
      <th>46</th>
      <td>0x986a2fCa9eDa0e06fBf7839B89BfC006eE2a23Dd</td>
      <td>3438.0</td>
    </tr>
    <tr>
      <th>47</th>
      <td>0xFBb1b73C4f0BDa4f67dcA266ce6Ef42f520fBB98</td>
      <td>27005.0</td>
    </tr>
    <tr>
      <th>48</th>
      <td>0x46340b20830761efd32832A74d7169B29FEB9758</td>
      <td>10285.0</td>
    </tr>
    <tr>
      <th>49</th>
      <td>0x46340b20830761efd32832A74d7169B29FEB9758</td>
      <td>10285.0</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
