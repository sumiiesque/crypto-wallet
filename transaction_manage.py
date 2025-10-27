# getting balance
def balance(web3,address):
    balance=web3.eth.get_balance(address)
    eth=web3.from_wei(balance,'ether')
    return eth

# sending ether
def send_eth(web3,from_acc,to_address,amt_eth):
    value=web3.to_wei(amt_eth,'ether')

    txn={
        'to':to_address,
        'value':value,
        'gas':21000,
        'gas_price':web3.eth.gas_price,
        'nonce':web3.eth.get_transaction_count(from_acc.address)
    }

    signed_txn=from_acc.sign_transaction(txn)

    txn_hash=web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Transaction sent. Hash:", txn_hash.hex()) 
    
    return txn_hash
