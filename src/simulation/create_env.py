import yaml

from contracts.uniswap_v2 import UniswapV2
from core.blockchain import Blockchain
from market.token import Token


def create_env_from_yaml(yaml_file: str) -> Blockchain:
    # Read YAML file
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # Create blockchain
    blockchain = Blockchain()

    # Create tokens
    for token_info in data["tokens"]:
        blockchain.create_token(Token(token_info["name"], token_info["value"], 0))

    # Create users
    for user_info in data["users"]:
        user = blockchain.create_user(user_info["name"])
        for token_info in user_info["tokens"]:
            user.add_to_wallet(
                blockchain.tokens[token_info["name"]], token_info["amount"]
            )

    # Create contracts
    for contract_info in data["contracts"]:
        if contract_info["name"] == "UniswapV2":
            uniswap_v2 = UniswapV2()
            blockchain.create_contract(uniswap_v2)
            pool_info = contract_info["pools"]
            uniswap_v2.create_pool(
                blockchain.tokens[pool_info[0]["name"]],
                blockchain.tokens[pool_info[1]["name"]],
                pool_info[2]["fee"],
                pool_info[0]["amount"],
                pool_info[1]["amount"],
            )

    return blockchain
