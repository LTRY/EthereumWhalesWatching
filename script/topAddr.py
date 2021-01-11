#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import io
import json
import pymysql


with open('../non-repertorie/etherTopAddr.html') as f:
    resp = f.read()

soup = BeautifulSoup(resp, 'html.parser')

_addr = {}

for tr in soup.find_all('tr')[1:]:
    tds = tr.find_all('td')
    a = [addr.get_text() for addr in tds]
    query = f"REPLACE INTO iswhale (`address`, `nameTag`, `whale`) VALUES ('{a[1]}', '{a[2]}', {1 if a[2] == '' else 0});"
    conn = pymysql.connect("127.0.0.1", "root", "pwd", "ETH")
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

'''
    _addr[a[1]] = {
        'nameTag': a[2],
        'balance': int(a[3].split(' ')[0].replace(',', '').split('.')[0]),
        'txCount': int(a[5].replace(',', ''))
    }

with io.open('Top100ETHAddr.json', 'w') as f:
    f.write(str(json.dumps(_addr, indent=4)))
'''





