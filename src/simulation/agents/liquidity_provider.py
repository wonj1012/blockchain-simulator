import math
import random

from contracts.contract import Contract
from core.blockchain import Blockchain
from core.transaction import Transaction
from market.actors.user import User


class LiquidityProviderAgent:
    """
    This class represents a liquidity provider agent.
    """

    @staticmethod
    def simulate_lp_actions(
        user_list: list[User], contract: Contract, blockchain: Blockchain
    ):
        """
        Simulates liquidity provider actions.

        Args:
            user_list (list[User]): List of users.
            contract (Contract): Contract object.
            blockchain (Blockchain): Blockchain object.
        """
        for user in user_list:
            # Select tokens from the pool
            token1, token2 = random.sample(blockchain.pool.tokens, 2)

            # Calculate pool ratio and market ratio
            pool_ratio = blockchain.get_spot_price(token1, token2)
            market_ratio = token2.real_value / token1.real_value

            # Calculate LP strategy
            lp_discourage = abs(math.log(pool_ratio) - math.log(market_ratio))
            lp_volume = (1 - lp_discourage) * user.total_value() * 0.2
            lp_amount = lp_volume / blockchain.pool.pool_token.real_value

            # Adjust investment
            if lp_amount < 0:
                lp_amount = min(
                    -lp_amount, user.get_quantity(blockchain.pool.pool_token)
                )
                if lp_amount > 0:
                    transaction = Transaction(
                        user, contract, "withdraw", {"amount": lp_amount}
                    )
                    user.send_transaction(transaction, blockchain)
            else:
                # Calculate needed budget and providing quantities
                needed_budget = 0
                providing_quantities = {}
                for token in blockchain.tokens.values():
                    if token != token1:
                        needed_quantity = (
                            blockchain.pool.get_quantity(token)
                            / blockchain.pool.total_pool_token_quantity
                            * lp_amount
                        )
                        active_quantity = user.get_quantity(token)
                        if active_quantity > needed_quantity:
                            transaction = Transaction(
                                user,
                                contract,
                                "sell",
                                {
                                    "token": token,
                                    "amount": active_quantity - needed_quantity,
                                },
                            )
                            user.send_transaction(transaction, blockchain)
                        else:
                            needed_budget += (
                                needed_quantity - active_quantity
                            ) * token.real_value

                # Adjust LP based on budget
                if user.budget < needed_budget:
                    lp_amount = lp_amount / needed_budget * user.budget * 0.9

                if lp_amount > 0.01:
                    for token, quantity in blockchain.pool.quantities.items():
                        needed_quantity = (
                            quantity
                            * lp_amount
                            / blockchain.pool.total_pool_token_quantity
                        )
                        active_quantity = user.get_quantity(token)
                        if active_quantity < needed_quantity:
                            transaction = Transaction(
                                user,
                                contract,
                                "buy",
                                {
                                    "token": token,
                                    "amount": needed_quantity - active_quantity,
                                },
                            )
                            user.send_transaction(transaction, blockchain)
                        providing_quantities[token] = needed_quantity
                    transaction = Transaction(
                        user, contract, "provide", {"quantities": providing_quantities}
                    )
                    user.send_transaction(transaction, blockchain)
