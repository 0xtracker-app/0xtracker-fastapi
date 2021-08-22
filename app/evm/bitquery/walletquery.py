query = """query (
  $network: EthereumNetwork!,
  $address: String!
) {
  ethereum(network: $network) {
    address(address: {is: $address}) {
      balances {
        currency {
          address
          symbol
          tokenType
          decimals
          name
        }
        value
      }
    }
  }
}"""

variables = """{"limit":1000,
  "offset":0,
  "network":"bsc",
  "address":"%s"
}"""