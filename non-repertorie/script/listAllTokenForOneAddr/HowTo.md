# List All Token For One ETH Addr

tokenAddr.json
```json
{
    "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f", 
    "USDT" : "0xdac17f958d2ee523a2206206994597c13d831ec7", 
    "BNB": "0xB8c77482e45F1F44dE1745F52C74426C631bDD52", 
    "LINK" : "0x514910771af9ca656af840dff83e8264ecf986ca"
}
```

type in shell
```zsh
  node oneHolderTokens.js tokenAddr.json 0x1062a747393198f70f71ec65a582423dba7e5ab3
```

return
```
{ DAI: '0',
  USDT: '161614925526494',
  BNB: '150000000000000000',
  LINK: '2120556748784000000000' }
```

- https://bitquery.io/blog/newly-created-etheruem-token