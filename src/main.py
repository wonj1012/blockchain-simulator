from pprint import pprint

from blockchain import Blockchain, Transaction
from contracts import LiquidityPool
from core import Token


def main():
    blockchain = Blockchain()

    user1 = blockchain.create_user()
    user2 = blockchain.create_user()

    token_usdc = Token("USDC", 0, 0)
    token_eth = Token("ETH", 0, 0)
    blockchain.create_token(token_usdc)
    blockchain.create_token(token_eth)

    user1.add_to_wallet(token_usdc, 1000)
    user1.add_to_wallet(token_eth, 1000)
    user2.add_to_wallet(token_usdc, 1000)
    user2.add_to_wallet(token_eth, 1000)

    usdc_eth_pool_contract = LiquidityPool(
        token_1=token_usdc, token_2=token_eth, fee=0.003
    )
    blockchain.create_contract(usdc_eth_pool_contract)

    transactions = []

    transactions.append(
        Transaction(
            sender=user1,
            contract=usdc_eth_pool_contract,
            function="add_liquidity",
            args={"amount_1": 100, "amount_2": 100},
        )
    )
    transactions.append(
        Transaction(
            sender=user2,
            contract=usdc_eth_pool_contract,
            function="add_liquidity",
            args={"amount_1": 10, "amount_2": 10},
        )
    )

    blockchain.create_block(transactions=transactions)
    pprint(blockchain)

    print(str(usdc_eth_pool_contract))


if __name__ == "__main__":
    main()
