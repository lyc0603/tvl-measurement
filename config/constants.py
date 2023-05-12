"""
Configuration for the project
"""

from os import path
from config.settings import PROJECT_ROOT

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
# --------------------------------------------
# The Graph Queries
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
# Yearn related addresses
YREGISTRY_ADDRESS = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0".lower()
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

# Delisted tokens
DELISTED_TOKENS_BALANCER = [
    # No Wrapped aUSDT pool in Balancer
    "0xf8fd466f12e236f4c96f7cce6c79eadb819abf58",
    # No Wrapped aDAI pool in Balancer
    "0x02d60b84491589974263d922d9cc7a3152618ef6",
    # No Wrapped aUSDC pool in Balancer
    "0xd093fa4fb80d09bb30817fdcd442d4d02ed3e5de",
    # Balancer Euler Boosted Pool (USDT) (bb-e-USDT)
    "0x3c640f0d3036ad85afa2d5a9e32be651657b874f"
    # Balancer Euler Boosted Pool (USDC) (bb-e-USDC)
    "0xd4e7c1f3da1144c9e2cfd1b015eda7652b4a4399"
    # Balancer Euler Boosted Pool (DAI) (bb-e-DAI)
    "0xeb486af868aeb3b6e53066abc9623b1041b42bc0",
    # bb-euler-USD (bb-euler-USD-BPT)
    "0x50cf90b954958480b8df7958a9e965752f627124",
    # Balancer Aave v3 Boosted Pool (DAI)
    "0x6667c6fa9f2b3fc1cc8d85320b62703d938e4385",
    # Balancer Aave v3 Boosted Pool (USDT)
    "0xa1697f9af0875b63ddc472d6eebada8c1fab8568",
    # Balancer Aave v3 Boosted Pool (USDC)
    "0xcbfa4532d8b2ade2c261d3dd5ef2a2284f792692",
]

# Balancer Aave v3 Boosted Pool
BALANCER_AAVE_V3_BOOSTED_POOL = {
    "derivative_square": {
        # Balancer Aave v3 Boosted StablePool (bb-a-USD)
        "0xfebb0bbf162e64fb9d0dfe186e517d84c395f016": [
            # Balancer Aave v3 Boosted Pool (DAI) (bb-a-DAI)
            "0x6667c6fa9f2b3fc1cc8d85320b62703d938e4385",
            # Balancer Aave v3 Boosted Pool (USDT) (bb-a-USDT)
            "0xa1697f9af0875b63ddc472d6eebada8c1fab8568",
            # Balancer Aave v3 Boosted Pool (USDC) (bb-a-USDC)
            "0xcbfa4532d8b2ade2c261d3dd5ef2a2284f792692",
        ],
        # Balancer Boosted swETH-WETH (swETH-bb-a-WETH-BPT)
        "0x02d928e68d8f10c0358566152677db51e1e2dc8c": [
            # Balancer Aave v3 Boosted Pool (WETH) (bb-a-WETH)
            "0x60d604890feaa0b5460b28a424407c24fe89374a",
            # swETH (swETH)
            "0xf951e335afb289353dc249e82926178eac7ded78",
        ],
        # Balancer Gearboox Boosted StablePool (bb-g-USD)
        "0x99c88ad7dc566616548adde8ed3effa730eb6c34": [
            # Balancer Gearbox Boosted Pool (USDC) (bb-g-USDC)
            "0x8f5adc58b32d4e5ca02eac0e293d35855999436c",
            # Balancer Gearbox Boosted Pool (DAI) (bb-g-DAI)
            "0xe03af00fabe8401560c1ff7d242d622a5b601573",
        ],
        # Balancer 50wstETH-50Tessera-Boosted-APE (50wstETH-50stk-APE)
        "0x959216bb492b2efa72b15b7aacea5b5c984c3cca": [
            # Balancer Tessera Boosted APE Pool (bb-t-stkAPE)
            "0x126e7643235ec0ab9c103c507642dc3f4ca23c66",
            # Wrapped liquid staked Ether 2.0 (wstETH)
            "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
        ],
    },
    "derivative_simple": [
        # Balancer Aave v3 Boosted Pool (DAI) (bb-a-DAI)
        "0x6667c6fa9f2b3fc1cc8d85320b62703d938e4385",
        # Balancer Aave v3 Boosted Pool (USDT) (bb-a-USDT)
        "0xa1697f9af0875b63ddc472d6eebada8c1fab8568",
        # Balancer Aave v3 Boosted Pool (USDC) (bb-a-USDC)
        "0xcbfa4532d8b2ade2c261d3dd5ef2a2284f792692",
        # Balancer Aave v3 Boosted Pool (WETH) (bb-a-WETH)
        "0x60d604890feaa0b5460b28a424407c24fe89374a",
        # Balancer Gearbox Boosted Pool (USDC) (bb-g-USDC)
        "0x4a82b580365cff9b146281ab72500957a849abdc",
        # Balancer Gearbox Boosted Pool (DAI) (bb-g-DAI)
        "0xe03af00fabe8401560c1ff7d242d622a5b601573",
        # Balancer Tessera Boosted APE Pool (bb-t-stkAPE)
        "0x126e7643235ec0ab9c103c507642dc3f4ca23c66",
    ],
    "no_record_underlying": {
        # Diesel USDC : USDC
        "0xc411db5f5eb3f7d552f9b8454b2d74097ccde6e3": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        # Diesel DAI : DAI
        "0x6cfaf95457d7688022fc53e7abe052ef8dfbbdba": "0x6b175474e89094c44da98b954eedeac495271d0f",
        # Staked Apecoin (sAPE): APE
        "0x7966c5bae631294d7cffcea5430b78c2f76db6fa": "0x4d224452801ACEd8B2F0aebE155379bb5D594381",
    },
}

# Euler Finance related addresses
EULER_RELATED_ADDRESSES = [
    # eDAI
    "0xe025e3ca2be02316033184551d4d3aa22024d9dc",
    # eUSDC
    "0xeb91861f8a4e1c12333f42dce8fb0ecdc28da716",
    # eUSDT
    "0x4d19f33948b99800b6113ff3e83bec9b537c85d2",
]
