# Beginner-Friendly Multi-Network Crypto Wallet

A non-custodial cryptocurrency wallet supporting Bitcoin and Ethereum networks, featuring both a modern React frontend and Python CLI.

## 🎯 Key Features

### Wallet & Keys
- Generate secure private and public keys
- Derive Bitcoin & Ethereum addresses from the same private key
- Export Bitcoin WIF private key
- Import existing wallets using private keys
- Sign messages digitally for verification

### Ethereum Network
- Connect to Ethereum blockchain via Alchemy
- Create Ethereum wallets
- Check ETH balance
- Send Ether transactions

### User Interfaces
- 🖥️ **Modern React Frontend** - Beautiful, gradient-based UI
- 💻 **Python CLI Menu** - Text-based interface for advanced users

## 🚀 Quick Start

### Frontend + Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the API server:**
   ```bash
   python api_server.py
   ```

4. **Start the React frontend (in a new terminal):**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Visit `http://localhost:3000`

### Python CLI Only

Run the Python script directly:
```bash
python main.py
```

## 📁 Project Structure

```
├── src/                    # React frontend
│   ├── App.jsx            # Main React component
│   ├── App.css            # Styles
│   └── main.jsx           # Entry point
├── crypto/                # Crypto utilities
│   ├── key_management.py
│   ├── address_generation.py
│   └── crypto_utils.py
├── blockchain/            # Blockchain functions
│   ├── eth_connect.py
│   └── transaction_manage.py
├── api_server.py          # Flask API server
├── main.py                # Python CLI interface
├── requirements.txt       # Python dependencies
└── package.json           # Node.js dependencies
```

## 🌐 API Endpoints

- `POST /api/generate-wallet` - Generate new wallet
- `POST /api/import-wallet` - Import existing wallet
- `POST /api/connect-ethereum` - Connect to Ethereum
- `POST /api/get-balance` - Get ETH balance
- `POST /api/send-eth` - Send ETH transaction

## 🎨 Frontend Features

- Gradient-based modern UI
- Wallet creation/import
- Address display
- Balance checking
- Transaction sending
- Responsive design

## 📝 Requirements

- Python 3.7+
- Node.js 16+
- Internet connection for Alchemy API
