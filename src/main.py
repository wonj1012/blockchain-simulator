from contracts.uniswap_v2 import UniswapV2
from simulation import create_env_from_yaml
from simulation.simulator import Epoch, Simulator


def main():
    blockchain = create_env_from_yaml("data/blockchain_config.yaml")

    simulator = Simulator(blockchain)
    simulator.create_users(100)
    simulator.create_liquidity_providers(10)
    simulator.create_block_producers(1)

    epochs = [
        Epoch(
            num_blocks=1000,
            oracle={
                blockchain.tokens["USDC"]: 1.0,
                blockchain.tokens["ETH"]: 3000.0,
            },
        ),
        Epoch(
            num_blocks=100,
            oracle={
                blockchain.tokens["USDC"]: 1.0,
                blockchain.tokens["ETH"]: 4000.0,
            },
        ),
    ]

    simulator.run(epochs=epochs, verbose=True)


if __name__ == "__main__":
    main()
