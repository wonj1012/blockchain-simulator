from blockchain import Blockchain
from contracts import Contract
from core.user import User


class Engine:
    def __init__(self):
        self.blockchain = Blockchain()

    def add_user(self, user: User):
        self.blockchain.users[user.address] = user

    def add_contract(self, contract: Contract):
        self.blockchain.contracts[contract.name] = contract
