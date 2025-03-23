# eRupee Blockchain Implementation

This is a simple blockchain implementation that creates and manages the eRupee cryptocurrency. The implementation includes account management, transaction handling, and transaction history tracking.

## Features

- Create multiple accounts
- Mine blocks to earn eRupee
- Send and receive eRupee between accounts
- View transaction history
- Verify blockchain integrity
- Secure transaction signing using ECDSA

## Requirements

- Python 3.7+
- cryptography
- pycryptodome

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to see a demonstration of the blockchain functionality:

```bash
python main.py
```

The script will:
1. Create two accounts and a miner account
2. Mine some initial blocks to get coins
3. Transfer coins between accounts
4. Show transaction history
5. Verify blockchain integrity

## How it Works

1. **Accounts**: Each account has a public/private key pair and a unique address
2. **Transactions**: Transactions are signed using ECDSA and include sender, recipient, and amount
3. **Blocks**: Blocks contain multiple transactions and are mined using proof-of-work
4. **Mining**: Miners receive rewards for successfully mining blocks
5. **Transaction History**: All transactions are logged and can be traced through the blockchain

## Security Features

- ECDSA-based transaction signing
- Proof-of-work mining
- Blockchain integrity verification
- Transaction validation
- Balance checking before transactions

## Note

This is a simplified implementation for educational purposes. For production use, additional security measures and optimizations would be needed. 