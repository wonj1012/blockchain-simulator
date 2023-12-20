from contracts.uniswap_v2 import UniswapV2
from core.blockchain import Blockchain
from market.actors.user import BlockProducer, User
from market.token import Token
from simulation.agents import (BlockProducerAgent, LiquidityProviderAgent,
                               UserAgent)
from utils.logger import with_logging
from utils.math import adjust_random_percent


class Epoch:
    def __init__(self, num_blocks: int, oracle: dict[Token, float]):
        self.num_blocks = num_blocks
        self.oracle = oracle

    def __repr__(self) -> str:
        return f"Epoch({self.num_blocks}, {self.oracle})"


class Simulator:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.users: list[User] = []
        self.liquidity_providers: list[User] = []
        self.block_producers: list[BlockProducer] = []

    def __repr__(self) -> str:
        return f"Simulator(blockchain={self.blockchain.name}, users={len(self.users)}, liquidity_providers={len(self.liquidity_providers)}, block_producers={len(self.block_producers)})"

    @with_logging
    def create_users(self, num: int):
        for i in range(num):
            user = self.blockchain.create_user(name=f"User_{i}")

            for token in self.blockchain.tokens.values():
                user.add_to_wallet(token=token, amount=1000)

            self.users.append(user)

    @with_logging
    def create_liquidity_providers(self, num: int):
        for i in range(num):
            lp = self.blockchain.create_user(name=f"LP_{i}")

            for token in self.blockchain.tokens.values():
                lp.add_to_wallet(token=token, amount=50000)

            self.liquidity_providers.append(lp)

    @with_logging
    def create_block_producers(self, num: int):
        for i in range(num):
            bp = self.blockchain.create_block_producer(name=f"BP_{i}")

            for token in self.blockchain.tokens.values():
                bp.add_to_wallet(token=token, amount=10000)

            self.block_producers.append(bp)

    def run(self, epochs: list[Epoch], verbose: bool = False):
        epoch_num = 0
        if verbose:
            self.print_snapshot(epoch_num)

        for epoch in epochs:
            self.run_epoch(epoch)

            epoch_num += 1

            if verbose:
                self.print_snapshot(epoch_num)

    @with_logging
    def run_epoch(self, epoch: Epoch):
        prev_percents = {}
        for _ in range(epoch.num_blocks):
            for token, value in epoch.oracle.items():
                prev_percent = prev_percents.get(token, 0.0)
                random_percent = adjust_random_percent(
                    prev_percent, max_percent=0.05, change_limit=0.01
                )
                prev_percents[token] = random_percent
                token.value = value * (1 + random_percent)

            UserAgent.simulate_user_actions(
                self.users, self.blockchain.contracts["UniswapV2"], self.blockchain
            )

            # LiquidityProviderAgent.simulate_lp_actions(
            #     self.liquidity_providers,
            #     self.blockchain.contracts["UniswapV2"],
            #     self.blockchain,
            # )

            BlockProducerAgent.simulate_bp_actions(
                self.block_producers,
                self.blockchain.contracts["UniswapV2"],
                self.blockchain,
            )

    def get_users_total_value(self) -> float:
        total_value = 0
        for user in self.users:
            total_value += user.total_value

        return total_value

    def print_snapshot(self, epoch_num: int):
        print("-" * 80)
        print(f"Epoch {epoch_num}")
        print(f"User total value: {self.get_users_total_value()}")

        uniswap_v2: UniswapV2 = self.blockchain.contracts["UniswapV2"]  # type: ignore

        for pool in uniswap_v2.get_pools():
            print(f"{pool.pair_name}\n{pool.token_reserve}")
            print(f"TVL: {pool.total_value_locked}")

        print("-" * 80 + "\n")
