from crypto.key_management import KeyManagement
from crypto.crypto_utils import sign_message, to_wif
from crypto.address_generation import generate_bitcoin_address, generate_ethereum_address
from blockchain.eth_connect import connect_eth, create_wallet
from blockchain.transaction_manage import balance, send_eth

ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/z55UPz10Gxs4WjpBUCOsp"

def main_menu():
    print("=== Welcome to Beginner-Friendly Multi-Network Wallet ===")
    
    km = KeyManagement()
    eth_account = None
    web3 = None

    #menu
    def option_generate_wallet():
        nonlocal km
        print("\nGenerating Private Key...")
        km.generate_private_key()
        km.derive_public_key()
        print("Private Key (hex):", km.private_key.hex())
        print("Public Key (hex):", km.public_key.hex())

        btc_addr = generate_bitcoin_address(km.public_key)
        eth_addr = generate_ethereum_address(km.public_key)
        print("\nBitcoin Address:", btc_addr)
        print("Ethereum Address:", eth_addr)
        print("WIF Private Key (Bitcoin):", to_wif(km.private_key))

    def option_sign_message():
        if not km.private_key:
            print("Generate wallet first.")
            return
        msg = input("Enter message to sign: ")
        sig = sign_message(km.private_key, msg)
        print("Signature:", sig[:64], "...")

    def option_connect_ethereum():
        nonlocal web3, eth_account
        web3 = connect_eth(ALCHEMY_URL)
        if web3:
            eth_account = create_wallet(web3)

    def option_check_balance():
        if web3 and eth_account:
            bal = get_eth_balance(web3, eth_account.address)
            print(f"ETH Balance of {eth_account.address}: {bal} ETH")
        else:
            print("Connect to Ethereum first")

    def option_send_eth():
        if web3 and eth_account:
            to_addr = input("Enter recipient address: ").strip()
            try:
                amount = float(input("Enter amount in ETH: "))
                txn_hash = send_eth(web3, eth_account, to_addr, amount)
                print(f"Transaction hash: {txn_hash}")
            except ValueError:
                print("Invalid amount!")
        else:
            print("Connect to Ethereum first!")

    def option_exit():
        print("exiting....")
        exit()

    switch = {
        "1": option_generate_wallet,
        "2": option_sign_message,
        "3": option_connect_ethereum,
        "4": option_check_balance,
        "5": option_send_eth,
        "6": option_exit
    }

    while True:
        print("\n--- Main Menu ---")
        print("1. Generate Wallet (Bitcoin & Ethereum)")
        print("2. Sign Message")
        print("3. Connect to Ethereum")
        print("4. Check ETH Balance")
        print("5. Send ETH")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        switch.get(choice, lambda: print("Invalid option"))()


if __name__ == "__main__":
    main_menu()
