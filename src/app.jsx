import { useState, useEffect } from 'react'
import './app.css'

const API_URL = 'http://localhost:5000/api'

function App() {
  const [wallet, setWallet] = useState(null)
  const [privateKey, setPrivateKey] = useState('')
  const [importMode, setImportMode] = useState(false)
  const [balance, setBalance] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [connected, setConnected] = useState(false)

  const handleGenerateWallet = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_URL}/generate-wallet`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      const data = await response.json()
      if (data.success) {
        setWallet(data)
        setPrivateKey(data.private_key)
      } else {
        setError(data.error || 'Failed to generate wallet')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleImportWallet = async () => {
    if (!privateKey.trim()) {
      setError('Please enter a private key')
      return
    }
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_URL}/import-wallet`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ private_key: privateKey })
      })
      const data = await response.json()
      if (data.success) {
        setWallet(data)
        setImportMode(false)
      } else {
        setError(data.error || 'Failed to import wallet')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleConnect = async () => {
    if (!wallet) {
      setError('Please generate or import a wallet first')
      return
    }
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_URL}/connect-ethereum`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      const data = await response.json()
      if (data.success) {
        setConnected(true)
      } else {
        setError(data.error || 'Failed to connect')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleGetBalance = async () => {
    if (!wallet || !connected) {
      setError('Please connect to Ethereum first')
      return
    }
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_URL}/get-balance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: wallet.eth_address })
      })
      const data = await response.json()
      if (data.success) {
        setBalance(data.balance)
      } else {
        setError(data.error || 'Failed to get balance')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1>💰 Crypto Wallet</h1>
        <p className="subtitle">Multi-Network Wallet for Bitcoin & Ethereum</p>

        {error && <div className="error">{error}</div>}

        {!wallet && !importMode && (
          <div className="section">
            <button 
              className="btn btn-primary" 
              onClick={handleGenerateWallet}
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate New Wallet'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={() => setImportMode(true)}
              disabled={loading}
            >
              Import Existing Wallet
            </button>
          </div>
        )}

        {importMode && (
          <div className="section">
            <h3>Import Wallet</h3>
            <textarea
              className="input"
              rows="3"
              value={privateKey}
              onChange={(e) => setPrivateKey(e.target.value)}
              placeholder="Enter your private key (hex)"
            />
            <button 
              className="btn btn-primary" 
              onClick={handleImportWallet}
              disabled={loading}
            >
              {loading ? 'Importing...' : 'Import Wallet'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={() => {
                setImportMode(false)
                setPrivateKey('')
              }}
            >
              Cancel
            </button>
          </div>
        )}

        {wallet && (
          <>
            <div className="section">
              <h3>📊 Wallet Info</h3>
              <div className="info-box">
                <label>Bitcoin Address</label>
                <code>{wallet.btc_address}</code>
              </div>
              <div className="info-box">
                <label>Ethereum Address</label>
                <code>{wallet.eth_address}</code>
              </div>
              {wallet.wif && (
                <div className="info-box">
                  <label>WIF (Wallet Import Format)</label>
                  <code>{wallet.wif}</code>
                </div>
              )}
            </div>

            <div className="section">
              <div className="button-group">
                <button 
                  className={`btn ${connected ? 'btn-success' : 'btn-primary'}`}
                  onClick={handleConnect}
                  disabled={loading}
                >
                  {connected ? '✓ Connected' : 'Connect to Ethereum'}
                </button>
                {connected && (
                  <button 
                    className="btn btn-secondary" 
                    onClick={handleGetBalance}
                    disabled={loading}
                  >
                    {loading ? 'Loading...' : 'Check ETH Balance'}
                  </button>
                )}
              </div>
              {balance !== null && (
                <div className="balance-display">
                  <strong>ETH Balance:</strong> {balance.toFixed(6)} ETH
                </div>
              )}
            </div>

            <SendETH wallet={wallet} privateKey={privateKey} />
          </>
        )}
      </div>
    </div>
  )
}

function SendETH({ wallet, privateKey }) {
  const [toAddress, setToAddress] = useState('')
  const [amount, setAmount] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [txHash, setTxHash] = useState('')

  const handleSend = async () => {
    if (!toAddress || !amount) {
      setError('Please fill all fields')
      return
    }
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_URL}/send-eth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to_address: toAddress,
          amount: parseFloat(amount),
          private_key: privateKey
        })
      })
      const data = await response.json()
      if (data.success) {
        setTxHash(data.tx_hash)
        setToAddress('')
        setAmount('')
      } else {
        setError(data.error || 'Failed to send ETH')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="section send-section">
      <h3>💸 Send ETH</h3>
      <div className="input-group">
        <input
          className="input"
          type="text"
          value={toAddress}
          onChange={(e) => setToAddress(e.target.value)}
          placeholder="Recipient Address (0x...)"
        />
        <input
          className="input"
          type="number"
          step="0.000001"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="Amount (ETH)"
        />
      </div>
      {error && <div className="error">{error}</div>}
      {txHash && (
        <div className="success">
          Transaction sent! Hash: <code>{txHash}</code>
        </div>
      )}
      <button 
        className="btn btn-primary" 
        onClick={handleSend}
        disabled={loading}
      >
        {loading ? 'Sending...' : 'Send ETH'}
      </button>
    </div>
  )
}

export default App
