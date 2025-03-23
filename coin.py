import uuid
from typing import Dict, List, Optional

class ERupeeCoin:
    DENOMINATIONS = [1, 2, 5, 10, 50, 100]
    
    def __init__(self, denomination: int, owner_address: str):
        if denomination not in self.DENOMINATIONS:
            raise ValueError(f"Invalid denomination. Must be one of {self.DENOMINATIONS}")
        self.denomination = denomination
        self.serial_number = str(uuid.uuid4())
        self.owner_address = owner_address
        self.transaction_history = []

    def add_transaction(self, from_address: str, to_address: str, timestamp: float):
        self.transaction_history.append({
            'from': from_address,
            'to': to_address,
            'timestamp': timestamp
        })
        self.owner_address = to_address

    def get_transaction_history(self) -> List[Dict]:
        return self.transaction_history

class CoinWallet:
    def __init__(self, address: str):
        self.address = address
        self.coins: Dict[int, List[ERupeeCoin]] = {
            denomination: [] for denomination in ERupeeCoin.DENOMINATIONS
        }

    def add_coin(self, coin: ERupeeCoin):
        self.coins[coin.denomination].append(coin)

    def remove_coin(self, coin: ERupeeCoin):
        self.coins[coin.denomination].remove(coin)

    def get_balance(self) -> int:
        return sum(denomination * len(coins) for denomination, coins in self.coins.items())

    def get_coins_by_denomination(self) -> Dict[int, List[ERupeeCoin]]:
        return self.coins

    def find_coins_for_amount(self, amount: int) -> List[ERupeeCoin]:
        remaining_amount = amount
        selected_coins = []
        
        # Sort denominations in descending order to use largest coins first
        sorted_denominations = sorted(ERupeeCoin.DENOMINATIONS, reverse=True)
        
        for denomination in sorted_denominations:
            while remaining_amount >= denomination and self.coins[denomination]:
                coin = self.coins[denomination].pop(0)
                selected_coins.append(coin)
                remaining_amount -= denomination
        
        # If we couldn't find enough coins, put them back
        if remaining_amount > 0:
            for coin in selected_coins:
                self.coins[coin.denomination].append(coin)
            return []
            
        return selected_coins

    def get_all_coins(self) -> List[ERupeeCoin]:
        all_coins = []
        for coins in self.coins.values():
            all_coins.extend(coins)
        return all_coins 