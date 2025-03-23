from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from blockchain import Blockchain, Account
from coin import ERupeeCoin
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Initialize blockchain
blockchain = Blockchain(difficulty=4)

# Create accounts if they don't exist
if not hasattr(app, 'account1'):
    app.account1 = blockchain.create_account()
    app.account2 = blockchain.create_account()
    app.miner = blockchain.create_account()
    
    # Mine some initial blocks and add some coins
    for _ in range(3):
        blockchain.mine_pending_transactions(app.miner)
        time.sleep(0.1)
    
    # Add some initial coins to account1
    for denomination in ERupeeCoin.DENOMINATIONS:
        for _ in range(2):  # Add 2 coins of each denomination
            coin = ERupeeCoin(denomination, app.account1.address)
            app.account1.wallet.add_coin(coin)

@app.route('/')
def index():
    account1_coins = blockchain.get_coins_by_denomination(app.account1)
    account2_coins = blockchain.get_coins_by_denomination(app.account2)
    return render_template('index.html',
                         account1_address=app.account1.address,
                         account2_address=app.account2.address,
                         account1_balance=blockchain.get_balance(app.account1),
                         account2_balance=blockchain.get_balance(app.account2),
                         account1_coins=account1_coins,
                         account2_coins=account2_coins)

@app.route('/send', methods=['POST'])
def send():
    try:
        amount = int(float(request.form['amount']))  # Convert to integer
        sender = request.form['sender']
        recipient = request.form['recipient']
        
        if sender == app.account1.address:
            sender_account = app.account1
        else:
            sender_account = app.account2
            
        if recipient == app.account1.address:
            recipient_account = app.account1
        else:
            recipient_account = app.account2
            
        if blockchain.add_transaction(sender_account, recipient_account, amount):
            blockchain.mine_pending_transactions(app.miner)
            flash('Transaction successful!', 'success')
        else:
            flash(f'Transaction failed! Insufficient balance. Sender has {blockchain.get_balance(sender_account)} eRupee', 'error')
            
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        
    return redirect(url_for('index'))

@app.route('/add_funds', methods=['POST'])
def add_funds():
    try:
        amount = int(float(request.form['amount']))  # Convert to integer
        account = request.form['account']
        
        if account == app.account1.address:
            target_account = app.account1
        else:
            target_account = app.account2
            
        # Create new coins for the target account
        coins = []
        remaining_amount = amount
        for denomination in sorted(ERupeeCoin.DENOMINATIONS, reverse=True):
            while remaining_amount >= denomination:
                coin = ERupeeCoin(denomination, target_account.address)
                coins.append(coin)
                remaining_amount -= denomination
        
        # Add coins to the account
        for coin in coins:
            target_account.wallet.add_coin(coin)
            
        flash(f'Successfully added {amount} eRupee to account', 'success')
            
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        
    return redirect(url_for('index'))

@app.route('/transactions')
def transactions():
    account1_history = blockchain.get_transaction_history(app.account1)
    account2_history = blockchain.get_transaction_history(app.account2)
    return render_template('transactions.html',
                         account1_history=account1_history,
                         account2_history=account2_history,
                         account1_address=app.account1.address,
                         account2_address=app.account2.address)

if __name__ == '__main__':
    app.run(debug=True) 