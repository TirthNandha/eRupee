from blockchain import Blockchain
import time

def main():
    # Create a new blockchain
    blockchain = Blockchain(difficulty=4)
    
    # Create two accounts
    print("Creating accounts...")
    account1 = blockchain.create_account()
    account2 = blockchain.create_account()
    
    print(f"\nAccount 1 address: {account1.address}")
    print(f"Account 2 address: {account2.address}")
    
    # Create a miner account
    miner = blockchain.create_account()
    print(f"Miner address: {miner.address}")
    
    # Mine some blocks to get initial coins
    print("\nMining initial blocks to get some coins...")
    for _ in range(3):
        blockchain.mine_pending_transactions(miner)
        time.sleep(1)  # Simulate mining time
    
    # Transfer some coins from miner to account1
    print(f"\nTransferring 50 eRupee from miner to Account 1...")
    blockchain.add_transaction(miner, account1, 50)
    blockchain.mine_pending_transactions(miner)
    
    # Show balances
    print(f"\nCurrent balances:")
    print(f"Miner: {blockchain.get_balance(miner)} eRupee")
    print(f"Account 1: {blockchain.get_balance(account1)} eRupee")
    print(f"Account 2: {blockchain.get_balance(account2)} eRupee")
    
    # Transfer coins between accounts
    print(f"\nTransferring 20 eRupee from Account 1 to Account 2...")
    blockchain.add_transaction(account1, account2, 20)
    blockchain.mine_pending_transactions(miner)
    
    # Show updated balances
    print(f"\nUpdated balances:")
    print(f"Miner: {blockchain.get_balance(miner)} eRupee")
    print(f"Account 1: {blockchain.get_balance(account1)} eRupee")
    print(f"Account 2: {blockchain.get_balance(account2)} eRupee")
    
    # Show transaction history for Account 1
    print(f"\nTransaction history for Account 1:")
    history = blockchain.get_transaction_history(account1)
    for tx in history:
        print(f"Type: {tx['type']}, Amount: {tx['amount']} eRupee, Counterparty: {tx['counterparty']}, Block: {tx['block_index']}")
    
    # Verify blockchain integrity
    print(f"\nBlockchain is valid: {blockchain.is_chain_valid()}")

if __name__ == "__main__":
    main() 