from web3 import Web3

alchemy_url="https://eth-mainnet.g.alchemy.com/v2/z55UPz10Gxs4WjpBUCOsp"

def connect_eth(alchemy_url):
    web3=Web3(Web3.HTTPProvider(alchemy_url))

    if web3.is_connected():
        print("successfully connected to the ethereum blockchain")
        return web3
    else:
        print("connection failed")
        return None

def create_wallet(web3):
    account=web3.eth.account.create()
    print("public address:",account.address)
    print("private key:",account.key.hex())
    return account
