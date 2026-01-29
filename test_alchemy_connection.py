#!/usr/bin/env python3
"""
Test script to verify Alchemy connection before deployment.
Run this script to ensure your Alchemy configuration is correct.
"""

from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_alchemy_connection():
    """Test connection to Alchemy and verify wallet setup."""

    print("=" * 60)
    print("ALCHEMY CONNECTION TEST")
    print("=" * 60)

    # Get configuration from environment
    alchemy_api_key = os.getenv("ALCHEMY_API_KEY", "")
    blockchain_network = os.getenv("BLOCKCHAIN_NETWORK", "sepolia")
    account_address = os.getenv("ACCOUNT_ADDRESS", "")

    if not alchemy_api_key:
        print("❌ ERROR: ALCHEMY_API_KEY not found in .env file")
        print("   Please set your Alchemy API key in .env file")
        print("   Get your key from: https://dashboard.alchemy.com/")
        return False

    if not account_address:
        print("❌ ERROR: ACCOUNT_ADDRESS not found in .env file")
        print("   Please set your wallet address in .env file")
        return False

    # Build Alchemy URL
    if blockchain_network == "mainnet":
        alchemy_url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api_key}"
    elif blockchain_network == "sepolia":
        alchemy_url = f"https://eth-sepolia.g.alchemy.com/v2/{alchemy_api_key}"
    else:
        print(f"❌ ERROR: Unknown network '{blockchain_network}'")
        print("   Use 'sepolia' or 'mainnet'")
        return False

    print(f"\nConfiguration:")
    print(f"  Network: {blockchain_network}")
    print(f"  API Key: {alchemy_api_key[:10]}...{alchemy_api_key[-4:]}")
    print(f"  Account: {account_address}")
    print(f"  URL: {alchemy_url[:50]}...")

    # Test connection
    print(f"\nConnecting to Alchemy...")
    try:
        w3 = Web3(Web3.HTTPProvider(alchemy_url))

        if not w3.is_connected():
            print("❌ FAILED: Cannot connect to Alchemy")
            print("   Check your API key and internet connection")
            return False

        print("✓ Connected successfully!")

        # Get latest block
        try:
            latest_block = w3.eth.block_number
            print(f"✓ Latest block: {latest_block}")
        except Exception as e:
            print(f"❌ ERROR getting block number: {e}")
            return False

        # Check account balance
        try:
            balance = w3.eth.get_balance(account_address)
            eth_balance = w3.from_wei(balance, 'ether')
            print(f"✓ Account balance: {eth_balance} ETH")

            if balance == 0:
                print("\n⚠️  WARNING: Your account has 0 ETH balance!")
                print("   You need test ETH to deploy contracts.")
                if blockchain_network == "sepolia":
                    print("   Get free test ETH from:")
                    print("   - https://www.alchemy.com/faucets/ethereum-sepolia")
                    print("   - https://www.infura.io/faucet/sepolia")
                    print("   - https://faucet.quicknode.com/ethereum/sepolia")
                return False
            elif eth_balance < 0.01:
                print(f"\n⚠️  WARNING: Low balance ({eth_balance} ETH)")
                print("   You may need more ETH for contract deployment")

        except Exception as e:
            print(f"❌ ERROR checking balance: {e}")
            print("   Please verify your account address is correct")
            return False

        # Gas price check
        try:
            gas_price = w3.eth.gas_price
            gas_price_gwei = w3.from_wei(gas_price, 'gwei')
            print(f"✓ Current gas price: {gas_price_gwei:.2f} Gwei")
        except Exception as e:
            print(f"⚠️  Could not get gas price: {e}")

        # Success!
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYou're ready to deploy your application!")
        print(f"Network: {blockchain_network.upper()}")

        if blockchain_network == "sepolia":
            print(f"Etherscan: https://sepolia.etherscan.io/address/{account_address}")
        else:
            print(f"Etherscan: https://etherscan.io/address/{account_address}")

        print("\nNext steps:")
        print("1. Test locally: python app.py")
        print("2. Deploy to Render with your .env configuration")
        print("3. Monitor transactions on Etherscan")

        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your ALCHEMY_API_KEY is correct")
        print("2. Check your internet connection")
        print("3. Ensure .env file is in the same directory")
        return False

if __name__ == "__main__":
    success = test_alchemy_connection()
    exit(0 if success else 1)
