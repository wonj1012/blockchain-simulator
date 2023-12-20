import random

from contracts.contract import Contract
from core.blockchain import Blockchain
from core.transaction import Transaction
from market.actors.user import User


class UserAgent:
    @staticmethod
    def simulate_user_actions(
        user_list: list[User], contract: Contract, blockchain: Blockchain
    ):
        random.shuffle(user_list)
        for user in user_list:
            token_in, token_in_balance = random.choice(list(user.wallet.items()))
            amount_in = token_in_balance * random.uniform(0.01, 1.0)

            other_tokens = [
                token for token in blockchain.tokens.values() if token != token_in
            ]
            token_out = random.choice(other_tokens) if other_tokens else None

            if not token_out:
                continue

            transaction = Transaction(
                sender=user,
                contract=contract,
                function="swap",
                args={
                    "token_in": token_in,
                    "amount_in": amount_in,
                    "token_out": token_out,
                },
            )
            user.send_transaction(transaction=transaction, blockchain=blockchain)
