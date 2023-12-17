from pprint import pprint

from core import Transaction
from simulation import create_env_from_yaml


def main():
    blockchain = create_env_from_yaml("data/blockchain_config.yaml")

    users = list(blockchain.users.values())
    user1, user2 = list(users)[0], list(users)[1]

    token_usdc = blockchain.tokens["USDC"]
    token_eth = blockchain.tokens["ETH"]

    uniswap_v2 = blockchain.contracts["UniswapV2"]

    user1.send_transaction(
        Transaction(
            sender=user1,
            contract=uniswap_v2,
            function="add_liquidity",
            args={
                "token_1": token_usdc,
                "amount_1": 100,
                "token_2": token_eth,
                "amount_2": 100,
            },
        ),
        blockchain,
    )

    user2.send_transaction(
        Transaction(
            sender=user2,
            contract=uniswap_v2,
            function="add_liquidity",
            args={
                "token_1": token_usdc,
                "amount_1": 10,
                "token_2": token_eth,
                "amount_2": 10,
            },
        ),
        blockchain,
    )

    blockchain.create_block()
    pprint(blockchain)


if __name__ == "__main__":
    main()
