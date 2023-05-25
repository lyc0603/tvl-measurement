"""
Configuration for the project
"""

from os import path
from config.settings import PROJECT_ROOT

# --------------------------------------------
# Target protocols
TVL_LIST = ["AAVE_V2", "BALANCER", "YEARN", "CURVE", "MAKER", "COMPOUND_V2"]
# --------------------------------------------
# Data paths
DATA_PATH = path.join(PROJECT_ROOT, "data")
PROCESSED_DATA_PATH = path.join(PROJECT_ROOT, "processed_data")
FIGURES_PATH = path.join(PROJECT_ROOT, "figures")
TABLES_PATH = path.join(PROJECT_ROOT, "tables")
CACHE_PATH = path.join(DATA_PATH, "cache")
# --------------------------------------------
# API keys
ALCHEMY_ETH_SOCKET = (
    "https://eth-mainnet.g.alchemy.com/v2/20Whs6Xw4uaBBdhUfgsc2gIOIexUJ6Ki"
)
THE_GRAPH_API_KEY = "1b3e7f080713d36560cac31fdda56396"
# --------------------------------------------
# The Graph URLs
THE_GRAPH_URL = (
    "https://gateway.thegraph.com/api/" + THE_GRAPH_API_KEY + "/subgraphs/id/"
)
BALANCER_URL = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2"
UNISWAP_V2_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
UNISWAP_V3_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
YEARN_URL = "https://api.thegraph.com/subgraphs/name/rareweasel/yearn-vaults-v2-subgraph-mainnet"
# --------------------------------------------
# The Graph Queries
# Pool queries
UNISWAP_V2_POOLS_QUERY_DICT = {
    "first_batch": """
query MyQuery {
  pairs(first: 1000, orderBy: id, orderDirection: asc) {
    reserve0
    reserve1
    reserveUSD
    id
    totalSupply
    token0 {
      id
      name
      symbol
    }
    token1 {
      id
      name
      symbol
    }
  }
}
""",
    "following_batch": """
query ($id_gt: ID!){
  pairs(
    first: 1000
    orderBy: id
    orderDirection: asc
    where: {id_gt: $id_gt}
  ) {
    reserve0
    reserve1
    reserveUSD
    id
    token0 {
      id
      name
      symbol
    }
    token1 {
      id
      name
      symbol
    }
  }
}
""",
}

UNISWAP_V3_TOKENS_QUERY_DICT = {
    "first_batch": """
query MyQuery {
  pools(first: 1000, orderBy: id, orderDirection: asc) {
    id
  }
}
""",
    "following_batch": """
query ($id_gt: ID!){
  pools(
    first: 1000
    orderBy: id
    orderDirection: asc
    where: {id_gt: $id_gt}
  ) {
    id
  }
}
""",
}

BALANCER_POOLS_QUERY = UNISWAP_POOLS_QUERY = """
{
  liquidityPools(orderBy:totalValueLockedUSD,orderDirection:desc){
    id
    symbol
    inputTokenBalances
    outputTokenSupply
    inputTokens{
      id
      symbol
      decimals
    }
    outputToken {
      id
      symbol
      decimals
    }
  }
}
"""

COMPOUND_POOLS_QUERY = """
{
  markets {
    id
    cTokenSymbol
    cTokenDecimals
    underlyingName
    underlyingPerCToken
    totalSupply
    totalBorrow
  }
}
"""

YEARN_POOLS_QUERY = """
{
  vaults(first: 1000, orderBy: id, orderDirection: asc) {
    id
  }
}
"""

# Token price queries
UNISWAP_V2_TOKEN_PRICE_QUERY = """
query ($id: ID!){
  tokenDayDatas(
    where: {token: $id}
    first: 1
    orderBy: date
    orderDirection: desc
  ) {
    priceUSD
  }
}
"""

BALANCER_TOKEN_PRICE_QUERY = """
query ($id: ID!){
  token(id: $id) {
    latestUSDPrice
  }
}
"""

# TVL queries
UNISWAP_V2_POOL_TVL_QUERY = """
query{
  uniswapDayDatas(first: 1, orderBy: date, orderDirection: desc) {
    totalLiquidityUSD
  }
}
"""

# --------------------------------------------
# The Graph IDs
UNISWAP_V3_SUBGRAPH_ID = "ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7"
BALANCER_SUBGRAPH_ID = "Ei5typKWPepPSgqkaKf3p5bPhgJesnu1RuRpyt69Pcrx"
# --------------------------------------------
# Config parameters
# Maximum number of pools to fetch
MAXIMUM_LP_COUNT_UNISWAP_V2 = 20
MAXIMUM_LP_COUNT_UNISWAP_V3 = 15
# --------------------------------------------
# Key addresses
# Uniswap related addresses
UNISWAP_V2_FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f".lower()
# AAVE related addresses
AAVE2_PROTOCOL_DATA_PROVIDER_ADDRESS = (
    "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d".lower()
)
AAVE_ADDRESS = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9".lower()
# Balancer related addresses
BAL_ADDRESS = "0xba100000625a3754423978a60c9317c58a424e3D".lower()
# Compound related addresses
COMPTROLLER_ADDRESS = "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B".lower()
COMP_ADDRESS = "0xc00e94cb662c3520282e6f5717214004a7f26888".lower()
# Curve related addresses
CURVE_ADDRESS_PROVIDER_ADDRESS = "0x0000000022D53366457F9d5E68Ec105046FC4383".lower()
CRV_ADDRESS = "0xD533a949740bb3306d119CC777fa900bA034cd52".lower()
# Maker related addresses
ILK_REGISTRY_ADDRESS = "0x5a464C28D19848f44199D003BeF5ecc87d090F87".lower()
VAT_ADDRESS = "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B".lower()
DAI_ADDRESS = "0x6B175474E89094C44Da98b954EedeAC495271d0F".lower()
SAI_ADDRESS = "0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359".lower()
MCD_SPOT_ADDRESS = "0x65C79fcB50Ca1594B025960e539eD7A9a6D434A3".lower()
MKR_ADDRESS = "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2".lower()
# --------------------------------------------
# Burn addresses
BURN_ADDRESS = [
    "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "0x0000000000000000000000000000000000000000",
]
# --------------------------------------------
# Non-standard contracts
NONSTANDARD_CONTRACTS = [
    # Tellor TRB token : non-standard contract
    "0x0ba45a8b5d5575935b8158a88c631e9f9c95a2e5",
    # ETH
    "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
]
# --------------------------------------------
# Real world assets
RWA_ASSETS = [
    # RWA-013 (RWA013)
    "0xd6c7fd4392d328e4a8f8bc50f4128b64f4db2d4c",
    # RWA-012 (RWA012)
    "0x3c7f1379b5ac286eb3636668deae71eaa5f7518c",
    # RWA-011 (RWA011)
    "0x0b126f85285d1786f52fc911affaaf0d9253e37a",
    # RWA-010 (RWA010)
    "0x20c72c1fdd589c4aaa8d9ff56a43f3b17ba129f8",
    # RWA-007 (RWA007)
    "0x078fb926b041a816facced3614cf1e4bc3c723bd",
    # RWA-009 (RWA009)
    "0x8b9734bbaa628bfc0c9f323ba08ed184e5b88da2",
    # RWA-008 (RWA008)
    "0xb9737098b50d7c536b6416daeb32879444f59fca",
    # RWA-006 (RWA006)
    "0x4ee03cfbf6e784c462839f5954d60f7c2b60b113",
    # RWA-005 (RWA005)
    "0x6db236515e90fc831d146f5829407746eddc5296",
    # RWA-004 (RWA004)
    "0x873f2101047a62f84456e3b2b13df2287925d3f9",
    # RWA-003 (RWA003)
    "0x07f0a80ad7aeb7bfb7f139ea71b3c8f7e17156b9",
    # RWA-002 (RWA002)
    "0xaaa760c2027817169d7c8db0dc61a2fb4c19ac23",
    # RWA-001 (RWA001)
    "0x10b2aa5d77aa6484886d8e244f0686ab319a270d",
]
# Custodian asset
CUSTODIAN_ASSETS = [
    # Wrapped BTC (WBTC)
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    # USD Coin (USDC)
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    # Tether USD (USDT)
    "0xdac17f958d2ee523a2206206994597c13d831ec7",
    # renBTC (renBTC)
    "0xeb4c2781e4eba804ce9a9803c67d0893436bb27d",
    # TrueUSD (TUSD)
    "0x0000000000085d4780b73119b644ae5ecd22b376",
    # Wrapped BTC (WBTC)
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    # Gemini dollar (GUSD)
    "0x056fd409e1d7a124bd7017459dfea2f387b6d5cd",
    # Pax Dollar (USDP)
    "0x8e870d67f660d95d5be530380d0ec0bd388289e1",
]

#  Delisted tokens
DELISTED_TOKENS = [
    "0xd5147bc8e386d91cc5dbe72099dac6c9b99276f5",
]
# --------------------------------------------
# Balancer-related special addresses

NO_RECORD_TOKEN = [
    # 1st July 2023 wstETH Sense Principal Token, A12 (sP-wstETH:01-07-2023:12)
    "0xc9ee62f98e251a7aa41116c3dc6272559791d387"
]
