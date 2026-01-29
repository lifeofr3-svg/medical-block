# Alchemy Setup Guide

This guide will help you set up Alchemy as your blockchain provider instead of Ganache.

## Why Alchemy?

- **Cloud-based**: No need to run a local blockchain node
- **Production-ready**: Reliable infrastructure for deployment
- **Free tier**: Sufficient for development and testing
- **Easy deployment**: Works seamlessly with Render and other cloud platforms

## Step 1: Create an Alchemy Account

1. Go to https://www.alchemy.com/
2. Click "Sign Up" and create a free account
3. Verify your email address

## Step 2: Create a New App

1. Log in to your Alchemy dashboard: https://dashboard.alchemy.com/
2. Click "+ Create new app"
3. Configure your app:
   - **Name**: Blockchain Medical App (or any name you prefer)
   - **Chain**: Ethereum
   - **Network**: Sepolia (recommended for testing)
     - Sepolia is a testnet, so transactions are free
     - For production, use "Mainnet" (requires real ETH)
   - **Description**: (optional)
4. Click "Create app"

## Step 3: Get Your API Key and URL

1. Click on your newly created app
2. Click "View Key" button
3. You'll see:
   - **API KEY**: Copy this (e.g., `abc123def456ghi789`)
   - **HTTPS URL**: Copy this (e.g., `https://eth-sepolia.g.alchemy.com/v2/abc123def456ghi789`)
   - **WSS URL**: (optional, for WebSocket connections)

Your Alchemy URL will look like:
```
https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
```

## Step 4: Get a Testnet Wallet

Since you're switching from Ganache, you'll need a real wallet for testnets.

### Option A: Use MetaMask (Recommended)

1. Install MetaMask: https://metamask.io/
2. Create a new wallet or import existing one
3. Switch to Sepolia network:
   - Click network dropdown at top
   - Enable "Show test networks" in settings
   - Select "Sepolia test network"
4. Get your account address and private key:
   - **Account Address**: Click on your account name to copy
   - **Private Key**: Click ⋮ → Account details → Export Private Key

### Option B: Create Wallet with Python

```python
from eth_account import Account
import secrets

# Generate new account
private_key = "0x" + secrets.token_hex(32)
account = Account.from_key(private_key)

print(f"Address: {account.address}")
print(f"Private Key: {private_key}")
```

**IMPORTANT**: Save your private key securely! Never share it or commit it to GitHub!

## Step 5: Get Test ETH (Sepolia)

You need test ETH to deploy contracts and make transactions.

### Sepolia Faucets:

1. **Alchemy Sepolia Faucet**: https://www.alchemy.com/faucets/ethereum-sepolia
   - Login with your Alchemy account
   - Enter your wallet address
   - Receive 0.5 SepoliaETH

2. **Infura Sepolia Faucet**: https://www.infura.io/faucet/sepolia
   - Enter your wallet address
   - Receive test ETH

3. **QuickNode Faucet**: https://faucet.quicknode.com/ethereum/sepolia
   - Enter your wallet address
   - Complete verification
   - Receive test ETH

You only need about 0.1-0.5 SepoliaETH for testing.

## Step 6: Configure Your Application

Update your environment variables:

### Local Development (.env file):

```bash
# Alchemy Configuration
ALCHEMY_API_KEY=your_alchemy_api_key_here
BLOCKCHAIN_NETWORK=sepolia
GANACHE_URL=https://eth-sepolia.g.alchemy.com/v2/your_alchemy_api_key_here

# Your Wallet
ACCOUNT_ADDRESS=0xYourWalletAddressHere
PRIVATE_KEY=0xYourPrivateKeyHere

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Render Production:

In Render dashboard, set these environment variables:
- `ALCHEMY_API_KEY`: Your Alchemy API key
- `BLOCKCHAIN_NETWORK`: `sepolia` (or `mainnet` for production)
- `GANACHE_URL`: Your full Alchemy HTTPS URL
- `ACCOUNT_ADDRESS`: Your wallet address
- `PRIVATE_KEY`: Your private key (mark as secret!)
- `SECRET_KEY`: Random secret for Flask

## Step 7: Test Your Connection

Run this test script to verify your Alchemy connection:

```python
from web3 import Web3

# Replace with your Alchemy URL
alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Test connection
if w3.is_connected():
    print("✓ Connected to Alchemy!")
    print(f"Latest block: {w3.eth.block_number}")

    # Check your account balance
    account = "0xYourWalletAddress"
    balance = w3.eth.get_balance(account)
    eth_balance = w3.from_wei(balance, 'ether')
    print(f"Balance: {eth_balance} ETH")
else:
    print("✗ Connection failed")
```

## Step 8: Deploy Your Application

Your smart contract will be deployed to Sepolia testnet automatically when the app starts.

### First Time Deployment:

1. Make sure you have test ETH in your wallet
2. Run your application locally to test:
   ```bash
   python app.py
   ```
3. Watch the console for contract deployment:
   ```
   Deploying smart contract...
   Contract deployed at: 0x...
   ```
4. Save the contract address for future reference

### Subsequent Runs:

To avoid redeploying the contract each time, you can:
1. Set `CONTRACT_ADDRESS` environment variable with your deployed contract address
2. The app will load the existing contract instead of deploying a new one

## Networks Comparison

### Sepolia Testnet (Recommended for Development)
- **Pros**: Free, fast, perfect for testing
- **Cons**: Not real blockchain, data may be reset
- **Use for**: Development, testing, demos

### Ethereum Mainnet (Production Only)
- **Pros**: Real blockchain, permanent data
- **Cons**: Costs real ETH, expensive gas fees
- **Use for**: Production deployments only

## Cost Considerations

### Alchemy Free Tier:
- **300M Compute Units per month**
- Sufficient for development and small apps
- Upgrade to paid plan if you exceed limits

### Testnet (Sepolia):
- **Transactions**: Free (uses test ETH)
- **Perfect for**: Development and testing

### Mainnet:
- **Gas fees**: Real ETH required
- **Deployment cost**: Typically 0.005-0.05 ETH (~$10-100)
- **Transaction costs**: 0.0001-0.001 ETH per transaction

## Security Best Practices

1. **Never commit private keys** to version control
2. **Use environment variables** for all sensitive data
3. **Use different wallets** for testnet and mainnet
4. **Limit funds** in deployment wallets
5. **Rotate API keys** regularly
6. **Monitor usage** in Alchemy dashboard

## Troubleshooting

### "Insufficient funds for gas"
- Get more test ETH from faucets
- Check your wallet balance

### "Connection refused"
- Verify your Alchemy API key
- Check your internet connection
- Ensure the URL is correct

### "Nonce too low"
- Clear nonce cache
- Wait a few minutes and retry

### "Rate limit exceeded"
- You've exceeded Alchemy's free tier
- Upgrade your plan or wait for reset

## Need Help?

- **Alchemy Documentation**: https://docs.alchemy.com/
- **Alchemy Discord**: https://discord.gg/alchemy
- **Ethereum Testnet Faucets**: https://faucetlink.to/sepolia

## Next Steps

After setting up Alchemy:
1. Test contract deployment locally
2. Verify transactions on Sepolia Etherscan: https://sepolia.etherscan.io/
3. Deploy to Render with your Alchemy credentials
4. Monitor usage in Alchemy dashboard

Good luck with your blockchain deployment! 🚀
