import random

from contracts.contract import Contract
from core.blockchain import Blockchain
from core.transaction import Transaction
from market.actors.user import BlockProducer


class BlockProducerAgent:
    @staticmethod
    def simulate_bp_actions(
        user_list: list[BlockProducer], contract: Contract, blockchain: Blockchain
    ):
        # for user in user_list:
        #     token_in = random.choice(list(user.wallet.keys()))
        #     amount_in = (
        #         random.choice(list(user.wallet.values())) * random.randint(1, 100) / 100
        #     )

        #     other_tokens = [
        #         token for token in blockchain.tokens.values() if token != token_in
        #     ]
        #     token_out = random.choice(other_tokens)

        #     transaction = Transaction(
        #         sender=user,
        #         contract=contract,
        #         function="swap",
        #         args={
        #             "token_in": token_in,
        #             "amount_in": amount_in,
        #             "token_out": token_out,
        #         },
        #     )
        #     user.send_transaction(transaction=transaction, blockchain=blockchain)

        blockchain.create_block()
