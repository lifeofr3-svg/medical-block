# Quick Migration Guide: Ganache → Alchemy

This guide will help you quickly migrate from Ganache to Alchemy for Render deployment.

## Why Migrate?

- **Ganache runs locally** - not accessible from cloud platforms like Render
- **Alchemy is cloud-based** - works perfectly with Render and other cloud platforms
- **Free tier available** - perfect for development and testing
- **Production-ready** - scales from development to production

## Quick Start (5 Minutes)

### 1. Create Alchemy Account

1. Go to https://www.alchemy.com/
2. Sign up for a free account
3. Verify your email

### 2. Create an Alchemy App

1. Go to https://dashboard.alchemy.com/
2. Click "+ Create new app"
3. Fill in:
   - **Name**: Blockchain Medical App
   - **Chain**: Ethereum
   - **Network**: Sepolia (testnet for free testing)
4. Click "Create app"
5. Click "View Key" to see your credentials

### 3. Get Your API Key

Copy your API key from the dashboard. It looks like:
```
abc123def456ghi789jkl012mno345pqr678
```

### 4. Set Up Your Wallet

#### Option A: Use MetaMask (Easiest)

1. Install MetaMask: https://metamask.io/
2. Create a new wallet or use existing
3. Switch to **Sepolia Test Network**:
   - Click network dropdown
   - Enable "Show test networks" in settings
   - Select "Sepolia test network"
4. Get your credentials:
   - **Address**: Click account name to copy
   - **Private Key**: ⋮ → Account details → Export Private Key

#### Option B: Generate New Wallet with Python

```bash
python3 << 'EOF'
from eth_account import Account
import secrets

private_key = "0x" + secrets.token_hex(32)
account = Account.from_key(private_key)

print(f"Address: {account.address}")
print(f"Private Key: {private_key}")
print("\n⚠️  SAVE THESE CREDENTIALS SECURELY!")
EOF
```

### 5. Get Free Test ETH

You need test ETH to deploy contracts. Get it from:

**Alchemy Faucet** (Recommended):
1. Go to https://www.alchemy.com/faucets/ethereum-sepolia
2. Login with your Alchemy account
3. Enter your wallet address
4. Receive 0.5 SepoliaETH

**Alternative Faucets**:
- https://www.infura.io/faucet/sepolia
- https://faucet.quicknode.com/ethereum/sepolia

### 6. Configure Your Application

Create a `.env` file in your project directory:

```bash
# Copy the example file
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

Update these values in `.env`:

```bash
# Alchemy Configuration
ALCHEMY_API_KEY=your_alchemy_api_key_here
BLOCKCHAIN_NETWORK=sepolia

# Your Wallet (from MetaMask or generated)
ACCOUNT_ADDRESS=0xYourWalletAddressHere
PRIVATE_KEY=0xYourPrivateKeyHere

# Flask Configuration
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=development
```

### 7. Test Your Connection

Run the test script to verify everything works:

```bash
python test_alchemy_connection.py
```

You should see:
```
✓ Connected successfully!
✓ Latest block: XXXXX
✓ Account balance: 0.5 ETH
✓ ALL TESTS PASSED!
```

### 8. Test Locally

Run your app locally to test contract deployment:

```bash
python app.py
```

Watch for:
```
✓ Connected to blockchain network
  Network: sepolia
  Account: 0xYour...Address
  Balance: 0.5 ETH
Compiling smart contract...
✓ Contract deployed successfully!
  Contract address: 0x...
  View on Etherscan: https://sepolia.etherscan.io/address/0x...
```

### 9. Deploy to Render

#### Update Environment Variables in Render:

1. Go to https://render.com/dashboard
2. Select your service
3. Go to "Environment" tab
4. Add these variables:

```
ALCHEMY_API_KEY = your_alchemy_api_key_here
BLOCKCHAIN_NETWORK = sepolia
ACCOUNT_ADDRESS = 0xYourWalletAddressHere
PRIVATE_KEY = 0xYourPrivateKeyHere
SECRET_KEY = [Click "Generate" in Render]
FLASK_ENV = production
PYTHON_VERSION = 3.11.0
```

5. Click "Save Changes"
6. Render will automatically redeploy

### 10. Verify Deployment

1. Wait for Render build to complete
2. Open your Render app URL
3. Check the deployment logs for:
   ```
   ✓ Connected to blockchain network
   ✓ Contract deployed successfully!
   ```
4. Test the application
5. View your transactions on Sepolia Etherscan

## Configuration Summary

### Before (Ganache):
```env
GANACHE_URL=http://127.0.0.1:7545
ACCOUNT_ADDRESS=0x22859a802657c4012d90Ba3259a707aD4559f6A9
PRIVATE_KEY=0xbb92e4d51d7947e632be0fb260f4dd9aba3e7b63a50e466259ff800889d49305
```

### After (Alchemy):
```env
ALCHEMY_API_KEY=your_alchemy_api_key_here
BLOCKCHAIN_NETWORK=sepolia
ACCOUNT_ADDRESS=0xYourRealWalletAddress
PRIVATE_KEY=0xYourRealPrivateKey
```

## Important Notes

### Security
- **NEVER commit .env file to Git** (already in .gitignore)
- **NEVER share your private key**
- **Use different wallets for testnet and mainnet**
- **Keep limited funds in deployment wallets**

### Networks
- **Sepolia**: Free testnet, perfect for development
- **Mainnet**: Production network, requires real ETH (expensive!)

### Costs
- **Sepolia Testnet**: FREE (uses test ETH)
- **Alchemy Free Tier**: 300M compute units/month (plenty for dev)
- **Contract Deployment**: ~0.1-0.5 test ETH (free from faucets)

### Data Persistence
- **Sepolia data is permanent** (unlike Ganache which resets)
- **Contract address stays the same** (save it for future use)
- **Can reuse deployed contract** (set CONTRACT_ADDRESS env var)

## Troubleshooting

### "Cannot connect to Alchemy"
- ✓ Check your API key is correct
- ✓ Verify internet connection
- ✓ Ensure no typos in .env file

### "Insufficient funds for gas"
- ✓ Get test ETH from faucets
- ✓ Wait a few minutes for faucet transaction to confirm
- ✓ Check balance: `python test_alchemy_connection.py`

### "Invalid private key"
- ✓ Ensure private key starts with "0x"
- ✓ Private key should be 66 characters (0x + 64 hex chars)
- ✓ No spaces or quotes in the value

### Contract deployment fails
- ✓ Check you have enough test ETH (need ~0.1 ETH)
- ✓ Verify contracts/MedicalRecord.sol exists
- ✓ Check Alchemy dashboard for API limits

## Next Steps After Migration

1. **Save your contract address** - Set CONTRACT_ADDRESS env var to avoid redeploying
2. **Monitor your app** - Check Alchemy dashboard for usage
3. **View transactions** - Use Sepolia Etherscan
4. **Test thoroughly** - Ensure all features work on testnet
5. **Plan for mainnet** - When ready for production, switch to mainnet

## Getting Help

- **Alchemy Docs**: https://docs.alchemy.com/
- **Alchemy Discord**: https://discord.gg/alchemy
- **Sepolia Faucets**: https://faucetlink.to/sepolia
- **Render Support**: https://render.com/docs

## Complete Example .env File

```bash
# ===================================================================
# ALCHEMY CONFIGURATION
# ===================================================================
ALCHEMY_API_KEY=abc123def456ghi789jkl012mno345pqr678
BLOCKCHAIN_NETWORK=sepolia

# ===================================================================
# WALLET CONFIGURATION
# ===================================================================
ACCOUNT_ADDRESS=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5
PRIVATE_KEY=0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

# ===================================================================
# FLASK CONFIGURATION
# ===================================================================
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
FLASK_ENV=development

# ===================================================================
# APPLICATION CONFIGURATION
# ===================================================================
UPLOAD_FOLDER=uploads
DATABASE_PATH=users.db

# ===================================================================
# OPTIONAL: DEPLOYED CONTRACT
# ===================================================================
# Uncomment and set after first deployment to reuse contract
# CONTRACT_ADDRESS=0xYourDeployedContractAddressHere
```

---

**You're all set!** 🚀 Your app is now using Alchemy and ready for cloud deployment.
