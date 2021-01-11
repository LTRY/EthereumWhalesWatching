#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from pprint import pprint


def run_query(query):  # A simple function to use requests.post to make the API call.
    request = requests.post('https://graphql.bitquery.io/', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                        query))


# The GraphQL query

query = """
{
  ethereum {
    smartContractCalls(options: {desc: "block.height", limit: 10}, 
      smartContractMethod: {is: "Contract Creation"}, 
      smartContractType: {is: Token}) {
      block {
        height
        timestamp {
          time
        }
      }
      smartContract {
        contractType
        address {
          address
          annotation
        }
        currency {
          name
          symbol
          decimals
          tokenType
        }
      }
    }
  }
}
"""
result = run_query(query)  # Execute the query
pprint(result)