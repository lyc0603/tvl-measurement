"""
Configuration for the project
"""

from os import path
from config.settings import PROJECT_ROOT

# --------------------------------------------
END_OF_SAMPLE_PERIOD = "2023-07-01"
CHAIN_LIST = [
    "Total",
    "Ethereum",
    "Tron",
    "Binance",
    "Arbitrum",
    "Polygon",
    "Optimism",
    "Avalanche",
    "Mixin",
    "Solana",
]
PTC_LIST = ["lido", "aave-v2", "makerdao"]
# --------------------------------------------
# Target protocols
TVL_LIST = ["AAVE_V2", "BALANCER", "YEARN", "CURVE", "MAKER", "COMPOUND_V2"]
LLAMA_SLUG_LIST = [
    "aave-v2",
    "balancer-v2",
    "yearn-finance",
    "curve-dex",
    "makerdao",
    "compound",
    # "uniswap-v2",
]

LLAMA_SLUG_ALL_LIST = [
    "makerdao",
]
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
# The Token category URLs
CMC_GOV = (
    "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?"
    + "start=1&limit=200&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&"
    + "cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,"
    + "num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,"
    + "self_reported_circulating_supply,self_reported_market_cap,total_supply,volume_7d,"
    + "volume_30d&tagSlugs=governance"
)
CMC_WRAPPED = (
    "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?"
    + "start=1&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&"
    + "cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,"
    + "cmc_rank,date_added,tags,platform,max_supply,circulating_supply,"
    + "self_reported_circulating_supply,self_reported_market_cap,total_supply,volume_7d,"
    + "volume_30d&tagSlugs=wrapped-tokens"
)
CMC_LAYER_ONE = (
    "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?"
    + "start=1&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&"
    + "cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,"
    + "cmc_rank,date_added,tags,platform,max_supply,circulating_supply,"
    + "self_reported_circulating_supply,self_reported_market_cap,total_supply,volume_7d,"
    + "volume_30d&tagSlugs=layer-1"
)

CMC_LAYER_TWO = (
    "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?"
    + "start=1&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&"
    + "cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,"
    + "cmc_rank,date_added,tags,platform,max_supply,circulating_supply,"
    + "self_reported_circulating_supply,self_reported_market_cap,total_supply,volume_7d,"
    + "volume_30d&tagSlugs=layer-2"
)

LLAMA_STABLE = "https://stablecoins.llama.fi/stablecoins?includePrices=true"

# --------------------------------------------
# DeFiLlama URLs
DEFI_LLAMA_PROTOCOL_URL = "https://api.llama.fi/protocols"
DEFI_LLAMA_TVL_URL = "https://api.llama.fi/protocol"
DEFI_LLAMA_TREASURY_URL = "https://api.llama.fi/treasury"
DEFI_LLAMA_ETH_TVL_URL = "https://api.llama.fi/v2/historicalChainTvl/Ethereum"
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

# --------------------------------------------

NON_CRYPTO_BACKING_STABLECOINS = [
    {
        "Name": "Tether",
        "Symbol": "USDT",
        "Contract": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "Category": "Fiat-backed",
    },
    {
        "Name": "USD Coin",
        "Symbol": "USDC",
        "Contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "Category": "Fiat-backed",
    },
    {
        "Name": "Binance USD",
        "Symbol": "BUSD",
        "Contract": "0x4Fabb145d64652a948d72533023f6E7A623C7C53",
        "Category": "Fiat-backed",
    },
    {
        "Name": "TrueUSD",
        "Symbol": "TUSD",
        "Contract": "0x0000000000085d4780B73119b644AE5ecd22b376",
        "Category": "Fiat-backed",
    },
    {
        "Name": "Frax",
        "Symbol": "FRAX",
        "Contract": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
        "Category": "Algorithmic",
    },
    {
        "Name": "Pax Dollar",
        "Symbol": "USDP",
        "Contract": "0x8E870D67F660D95d5be530380D0eC0bd388289E1",
        "Category": "Fiat-backed",
    },
    {
        "Name": "USDD",
        "Symbol": "USDD",
        "Contract": "0x0C10bF8FcB7Bf5412187A595ab97a3609160b5c6",
        "Category": "Algorithmic",
    },
    {
        "Name": "Frax Price Index",
        "Symbol": "FPI",
        "Contract": "0x5Ca135cB8527d76e932f34B5145575F9d8cbE08E",
        "Category": "Algorithmic",
    },
    {
        "Name": "Alchemix USD",
        "Symbol": "ALUSD",
        "Contract": "0xBC6DA0FE9aD5f3b0d58160288917AA56653660E9",
        "Category": "Algorithmic",
    },
    {
        "Name": "Euro Coin",
        "Symbol": "EUROC",
        "Contract": "0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c",
        "Category": "Fiat-backed",
    },
    {
        "Name": "Stasis Euro",
        "Symbol": "EURS",
        "Contract": "0xdB25f211AB05b1c97D595516F45794528a807ad8",
        "Category": "Fiat-backed",
    },
    {
        "Name": "Euro Tether",
        "Symbol": "EURT",
        "Contract": "0xC581b735A1688071A1746c968e0798D642EDE491",
        "Category": "Fiat-backed",
    },
    {
        "Name": "Bean",
        "Symbol": "BEAN",
        "Contract": "0xBEA0000029AD1c77D3d5D23Ba2D8893dB9d1Efab",
        "Category": "Algorithmic",
    },
    {
        "Name": "Fei USD",
        "Symbol": "FEI",
        "Contract": "0x956F47F50A910163D8BF957Cf5846D573E7f87CA",
        "Category": "Algorithmic",
    },
    {
        "Name": "ZUSD",
        "Symbol": "ZUSD",
        "Contract": "0xc56c2b7e71B54d38Aab6d52E94a04Cbfa8F604fA",
        "Category": "Fiat-backed",
    },
    {
        "Name": "HUSD",
        "Symbol": "HUSD",
        "Contract": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1",
        "Category": "Fiat-backed",
    },
    {
        "Name": "TerraClassicUSD",
        "Symbol": "USTC",
        "Contract": "0xa47c8bf37f92aBed4A126BDA807A7b7498661acD",
        "Category": "Algorithmic",
    },
    {
        "Name": "Monerium EUR emoney",
        "Symbol": "EURM",
        "Contract": "0x3231Cb76718CDeF2155FC47b5286d82e6eDA273f",
        "Category": "Fiat-backed",
    },
    {
        "Name": "EUROe Stablecoin",
        "Symbol": "EUROe",
        "Contract": "0x820802Fa8a99901F52e39acD21177b0BE6EE2974",
        "Category": "Fiat-backed",
    },
    {
        "Name": "Neutrino USD",
        "Symbol": "USDN",
        "Contract": "0x674C6Ad92Fd080e4004b2312b45f796a192D27a0",
        "Category": "Algorithmic",
    },
    {
        "Name": "USDK",
        "Symbol": "USDK",
        "Contract": "0x1c48f86ae57291F7686349F12601910BD8D470bb",
        "Category": "Fiat-backed",
    },
    {
        "Name": "SpiceUSD",
        "Symbol": "USDS",
        "Contract": "0x45fDb1b92a649fb6A64Ef1511D3Ba5Bf60044838",
        "Category": "Algorithmic",
    },
    {
        "Name": "Offshift anonUSD",
        "Symbol": "ANONUSD",
        "Contract": "0x5a7E6C8204A1359DB9AAcab7bA5Fc309B7981eFd",
        "Category": "Algorithmic",
    },
    {
        "Name": "Meme Dollar",
        "Symbol": "PINA",
        "Contract": "0x02814F435dD04e254Be7ae69F61FCa19881a780D",
        "Category": "Algorithmic",
    },
    {
        "Name": "LUGH",
        "Symbol": "EURL",
        "Contract": "0xA967Dd943B336680540011536E7D8c3d33333515",
        "Category": "Fiat-backed",
    },
    {
        "Name": "VOLT Protocol",
        "Symbol": "VOLT",
        "Contract": "0x559eBC30b0E58a45Cc9fF573f77EF1e5eb1b3E18",
        "Category": "Algorithmic",
    },
    {
        "Name": "Float Protocol Float",
        "Symbol": "FLOAT",
        "Contract": "0xb05097849BCA421A3f51B249BA6CCa4aF4b97cb9",
        "Category": "Algorithmic",
    },
]
