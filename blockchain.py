import hashlib
import json
import time
from typing import List, Dict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption
import base64
from coin import ERupeeCoin, CoinWallet

class Account:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()
        self.address = self._generate_address()
        self.wallet = CoinWallet(self.address)

    def _generate_address(self) -> str:
        public_bytes = self.public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
        return hashlib.sha256(public_bytes).hexdigest()[:40]

    def sign_transaction(self, transaction: 'Transaction') -> str:
        signature = self.private_key.sign(
            transaction.to_signable_string().encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return base64.b64encode(signature).decode()

class Transaction:
    def __init__(self, sender: Account, recipient: Account, amount: int, coins: List[ERupeeCoin]):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.coins = coins
        self.timestamp = time.time()
        self.signature = None

    def to_signable_string(self) -> str:
        coin_serials = [coin.serial_number for coin in self.coins]
        return f"{self.sender.address}{self.recipient.address}{self.amount}{self.timestamp}{json.dumps(coin_serials)}"

    def sign(self, signature: str):
        self.signature = signature

    def verify(self) -> bool:
        if not self.signature:
            return False
        try:
            self.sender.public_key.verify(
                base64.b64decode(self.signature),
                self.to_signable_string().encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except:
            return False

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'transactions': [{
                'sender': t.sender.address,
                'recipient': t.recipient.address,
                'amount': t.amount,
                'coins': [{'serial': c.serial_number, 'denomination': c.denomination} for c in t.coins],
                'timestamp': t.timestamp,
                'signature': t.signature
            } for t in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty: int):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.accounts: Dict[str, Account] = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        genesis_block.mine(self.difficulty)
        self.chain.append(genesis_block)

    def create_account(self) -> Account:
        account = Account()
        self.accounts[account.address] = account
        return account

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: Account, recipient: Account, amount: int) -> bool:
        if sender.wallet.get_balance() < amount:
            return False

        # Find coins to send
        coins_to_send = sender.wallet.find_coins_for_amount(amount)
        if not coins_to_send:
            return False

        transaction = Transaction(sender, recipient, amount, coins_to_send)
        signature = sender.sign_transaction(transaction)
        transaction.sign(signature)

        if not transaction.verify():
            return False

        self.pending_transactions.append(transaction)
        return True

    def mine_pending_transactions(self, miner: Account):
        block = Block(len(self.chain), self.pending_transactions, self.get_latest_block().hash)
        block.mine(self.difficulty)

        # Process transactions
        for transaction in block.transactions:
            # Update coin ownership and transaction history
            for coin in transaction.coins:
                coin.add_transaction(transaction.sender.address, transaction.recipient.address, transaction.timestamp)
                transaction.recipient.wallet.add_coin(coin)

            # Reward the miner with new coins
            reward_coins = [
                ERupeeCoin(10, miner.address) for _ in range(1)  # 10 eRupee reward
            ]
            for coin in reward_coins:
                miner.wallet.add_coin(coin)

        self.chain.append(block)
        self.pending_transactions = []

    def get_balance(self, account: Account) -> int:
        return account.wallet.get_balance()

    def get_transaction_history(self, account: Account) -> List[Dict]:
        history = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender.address == account.address or transaction.recipient.address == account.address:
                    history.append({
                        'type': 'sent' if transaction.sender.address == account.address else 'received',
                        'amount': transaction.amount,
                        'coins': [{'serial': coin.serial_number, 'denomination': coin.denomination} for coin in transaction.coins],
                        'counterparty': transaction.recipient.address if transaction.sender.address == account.address else transaction.sender.address,
                        'timestamp': transaction.timestamp,
                        'block_index': block.index
                    })
        return history

    def get_coins_by_denomination(self, account: Account) -> Dict[int, List[Dict]]:
        coins_by_denom = account.wallet.get_coins_by_denomination()
        return {
            denomination: [{'serial': coin.serial_number} for coin in coins]
            for denomination, coins in coins_by_denom.items()
        }

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            if current_block.hash[:self.difficulty] != '0' * self.difficulty:
                return False

        return True 