from flask import Flask, request, jsonify
from flask_cors import CORS
from crypto.key_management import KeyManagement
from crypto.crypto_utils import sign_message, to_wif
from crypto.address_generation import generate_bitcoin_address, generate_ethereum_address
from blockchain.eth_connect import connect_eth, create_wallet
from blockchain.transaction_manage import balance, send_eth
import os

app = Flask(__name__)
CORS(app)

# Global state
key_manager = KeyManagement()
web3 = None
eth_account = None
current_addresses = None

ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/z55UPz10Gxs4WjpBUCOsp"

@app.route('/api/generate-wallet', methods=['POST'])
def generate_wallet():
    """Generate new wallet with private/public keys"""
    try:
        km = KeyManagement()
        km.generate_private_key()
        km.derive_public_key()
        
        private_key_hex = km.private_key.hex()
        public_key_hex = km.public_key.hex()
        
        btc_addr = generate_bitcoin_address(km.public_key)
        eth_addr = generate_ethereum_address(km.public_key)
        wif = to_wif(km.private_key)
        
        # Store in global state
        global key_manager
        key_manager = km
        
        return jsonify({
            'success': True,
            'private_key': private_key_hex,
            'public_key': public_key_hex,
            'btc_address': btc_addr,
            'eth_address': eth_addr,
            'wif': wif
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/import-wallet', methods=['POST'])
def import_wallet():
    """Import wallet from private key"""
    try:
        data = request.get_json()
        private_key_hex = data.get('private_key')
        
        if not private_key_hex:
            return jsonify({'success': False, 'error': 'Private key required'}), 400
        
        km = KeyManagement()
        km.import_private_key(private_key_hex)
        
        btc_addr = generate_bitcoin_address(km.public_key)
        eth_addr = generate_ethereum_address(km.public_key)
        wif = to_wif(km.private_key)
        
        # Store in global state
        global key_manager
        key_manager = km
        
        return jsonify({
            'success': True,
            'btc_address': btc_addr,
            'eth_address': eth_addr,
            'wif': wif
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/connect-ethereum', methods=['POST'])
def connect_ethereum():
    """Connect to Ethereum blockchain"""
    try:
        global web3, eth_account
        
        web3_conn = connect_eth(ALCHEMY_URL)
        if not web3_conn:
            return jsonify({'success': False, 'error': 'Failed to connect'}), 500
        
        web3 = web3_conn
        
        # If we have an address from key manager, use it
        if key_manager and key_manager.public_key:
            eth_addr = generate_ethereum_address(key_manager.public_key)
            return jsonify({
                'success': True,
                'address': eth_addr,
                'message': 'Connected to Ethereum'
            })
        else:
            # Create new account for testing
            account = create_wallet(web3)
            eth_account = account
            return jsonify({
                'success': True,
                'address': account.address,
                'private_key': account.key.hex(),
                'message': 'New wallet created and connected to Ethereum'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-balance', methods=['POST'])
def get_balance():
    """Get ETH balance for an address"""
    try:
        global web3
        
        data = request.get_json()
        address = data.get('address')
        
        if not address:
            return jsonify({'success': False, 'error': 'Address required'}), 400
        
        if not web3:
            # Reconnect if needed
            web3 = connect_eth(ALCHEMY_URL)
        
        eth_balance = balance(web3, address)
        
        return jsonify({
            'success': True,
            'balance': float(eth_balance),
            'balance_wei': int(web3.to_wei(eth_balance, 'ether'))
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send-eth', methods=['POST'])
def send_eth_transaction():
    """Send ETH transaction"""
    try:
        global web3, eth_account, key_manager
        
        data = request.get_json()
        to_address = data.get('to_address')
        amount = float(data.get('amount', 0))
        private_key = data.get('private_key')
        
        if not to_address or not amount or not private_key:
            return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
        
        if not web3:
            web3 = connect_eth(ALCHEMY_URL)
        
        # Create account from private key
        from web3 import Account
        account = Account.from_key(private_key)
        
        tx_hash = send_eth(web3, account, to_address, amount)
        
        return jsonify({
            'success': True,
            'tx_hash': tx_hash.hex(),
            'message': 'Transaction sent successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

