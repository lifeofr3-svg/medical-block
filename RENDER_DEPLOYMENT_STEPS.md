# Render Deployment Instructions

Follow these steps to deploy your Blockchain Medical App to Render.

## Prerequisites Checklist

Before deploying, make sure you have:
- [ ] Alchemy account created (https://www.alchemy.com/)
- [ ] Alchemy API key
- [ ] Ethereum wallet address
- [ ] Ethereum wallet private key
- [ ] Test ETH in your wallet (get from https://www.alchemy.com/faucets/ethereum-sepolia)
- [ ] GitHub account
- [ ] Render account (https://render.com/)

---

## STEP 1: Set Up Alchemy (If Not Done Already)

### 1.1 Create Alchemy Account
1. Go to https://www.alchemy.com/
2. Click "Sign Up" and create free account
3. Verify your email

### 1.2 Create Alchemy App
1. Go to https://dashboard.alchemy.com/
2. Click "+ Create new app"
3. Configure:
   - **Name**: Blockchain Medical App
   - **Chain**: Ethereum
   - **Network**: Sepolia
4. Click "Create app"

### 1.3 Get Your API Key
1. Click on your app
2. Click "View Key"
3. Copy the **API KEY** (save it for later)

### 1.4 Set Up Wallet

**Option A - MetaMask (Recommended):**
1. Install MetaMask from https://metamask.io/
2. Create new wallet or use existing
3. Switch to Sepolia Test Network
4. Copy your wallet address (click account name)
5. Export private key: ⋮ → Account details → Export Private Key

**Option B - Generate New Wallet:**
```bash
pip install eth-account
python3 << 'EOF'
from eth_account import Account
import secrets
private_key = "0x" + secrets.token_hex(32)
account = Account.from_key(private_key)
print(f"Address: {account.address}")
print(f"Private Key: {private_key}")
EOF
```

### 1.5 Get Test ETH
1. Go to https://www.alchemy.com/faucets/ethereum-sepolia
2. Enter your wallet address
3. Receive 0.5 SepoliaETH (free!)

---

## STEP 2: Push Code to GitHub

### 2.1 Stage All Changes
```bash
cd "/home/sk/Downloads/C472_Blockchain_medical-20260128T081948Z-3-001 (2)/C472_Blockchain_medical/Blockchain_Medical"
git add .
```

### 2.2 Commit Changes
```bash
git commit -m "Configure for Alchemy and Render deployment with Python 3.11"
```

### 2.3 Push to GitHub
```bash
git push origin main
```

If you get errors, try:
```bash
git pull origin main --rebase
git push origin main
```

---

## STEP 3: Create Render Web Service

### 3.1 Go to Render Dashboard
1. Open https://render.com/dashboard
2. Click "New +" button (top right)
3. Select "Web Service"

### 3.2 Connect GitHub Repository
1. Click "Connect account" if not connected
2. Select your repository: `lifeofr3-svg/medical-block`
3. Click "Connect"

### 3.3 Configure Service Settings

Fill in these fields:

**Basic Settings:**
- **Name**: `blockchain-medical-app` (or your preferred name)
- **Region**: Select closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty (or set to project folder if needed)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2`

**Instance Settings:**
- **Instance Type**: `Free` (or select paid plan for better performance)

---

## STEP 4: Configure Environment Variables

**IMPORTANT:** In the Render service configuration, scroll down to "Environment Variables" section.

Click "Add Environment Variable" for each of these:

### Required Variables:

| Key | Value | Notes |
|-----|-------|-------|
| `FLASK_ENV` | `production` | Sets Flask to production mode |
| `ALCHEMY_API_KEY` | `your_alchemy_api_key` | From Alchemy dashboard |
| `BLOCKCHAIN_NETWORK` | `sepolia` | Use testnet |
| `ACCOUNT_ADDRESS` | `0xYourWalletAddress` | Your wallet address |
| `PRIVATE_KEY` | `0xYourPrivateKey` | **KEEP SECRET!** |
| `SECRET_KEY` | Click "Generate" | Random secret for Flask |

**Note:** Python version is set via `.python-version` file in the repo (already included)

### How to Add Each Variable:
1. Click "Add Environment Variable"
2. Enter **Key** in first field
3. Enter **Value** in second field
4. Click checkmark to save
5. Repeat for all variables

### Example Values:
```
FLASK_ENV = production
ALCHEMY_API_KEY = abc123def456ghi789jkl012
BLOCKCHAIN_NETWORK = sepolia
ACCOUNT_ADDRESS = 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5
PRIVATE_KEY = 0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
SECRET_KEY = [Click Generate button]
```

---

## STEP 5: Deploy!

### 5.1 Create Service
1. Review all settings
2. Click "Create Web Service" button at bottom
3. Render will start building your app

### 5.2 Monitor Build Process
You'll see a live log. Watch for:

```
==> Installing dependencies from requirements.txt
==> Successfully installed Flask-3.0.2 ...
==> Build successful!
==> Starting service with 'gunicorn app:app...'
```

**Build takes 5-10 minutes** (especially first time due to large dependencies)

### 5.3 Watch for Deployment Success

Look for these messages in the logs:
```
✓ Connected to blockchain network
  Network: sepolia
  Account: 0x...
  Balance: 0.5 ETH
Compiling smart contract...
✓ Contract deployed successfully!
  Contract address: 0x...
  View on Etherscan: https://sepolia.etherscan.io/address/0x...
```

---

## STEP 6: Test Your Deployment

### 6.1 Get Your App URL
Once deployed, you'll see a URL like:
```
https://blockchain-medical-app-xxxx.onrender.com
```

### 6.2 Open Your App
1. Click the URL in Render dashboard
2. You should see the login page
3. Create an account and test signup/login
4. Test the prediction features

### 6.3 Verify on Etherscan
1. Copy the contract address from logs
2. Go to https://sepolia.etherscan.io/
3. Paste your contract address
4. Verify contract is deployed and transactions are recorded

---

## STEP 7: Save Contract Address (Optional but Recommended)

To avoid redeploying the contract every time the app restarts:

### 7.1 Copy Contract Address
From the deployment logs, find:
```
Contract deployed at: 0x1234567890abcdef...
```

### 7.2 Add to Render Environment Variables
1. Go to Render dashboard → Your service → Environment
2. Add new variable:
   - **Key**: `CONTRACT_ADDRESS`
   - **Value**: `0xYourContractAddress`
3. Save changes
4. App will redeploy and reuse the existing contract

---

## Troubleshooting

### Build Fails

**Error: "Could not find a version that satisfies the requirement"**
- Solution: Check requirements.txt for incompatible versions
- Try: Update Python version in environment variables

**Error: "No module named 'web3'"**
- Solution: Ensure requirements.txt includes `web3==6.15.1`

### Deployment Fails

**Error: "Cannot connect to blockchain"**
- Check ALCHEMY_API_KEY is correct
- Verify BLOCKCHAIN_NETWORK is set to `sepolia`
- Test connection locally first

**Error: "Insufficient funds for gas"**
- Get more test ETH from faucets
- Check wallet balance on https://sepolia.etherscan.io/

**Error: "Application timeout"**
- Increase timeout in start command: `--timeout 180`
- Upgrade Render plan for better performance

### App Crashes on Startup

**Check the logs for:**
- Model files missing (ensure models/ directory is in git)
- Environment variables not set
- Database permission issues

**Solutions:**
1. Verify all environment variables are set
2. Check that model files are committed to git
3. Review Render logs for specific error messages

---

## Important Notes

### Free Tier Limitations
- App sleeps after 15 minutes of inactivity
- First request after sleep takes longer (cold start)
- Database is ephemeral (resets on deployment)

### For Production
- Upgrade to paid Render plan ($7+/month)
- Use persistent disk for database
- Switch to mainnet (requires real ETH)
- Implement proper error handling
- Add monitoring and logging

### Security
- NEVER commit .env file
- NEVER share your private key
- Keep limited funds in deployment wallet
- Rotate API keys regularly
- Use different wallets for testnet/mainnet

---

## Post-Deployment Checklist

- [ ] App URL loads successfully
- [ ] Can create account and login
- [ ] Diabetes prediction works
- [ ] Heart disease prediction works
- [ ] Transactions appear on Sepolia Etherscan
- [ ] Contract address saved in environment variables
- [ ] Alchemy dashboard shows API usage
- [ ] No errors in Render logs

---

## Useful Commands

### Update Your App
```bash
# Make changes to your code
git add .
git commit -m "Update description"
git push origin main
# Render auto-deploys on push
```

### View Logs
```bash
# In Render dashboard, click "Logs" tab
# Or use Render CLI (optional)
```

### Redeploy Manually
```bash
# In Render dashboard, click "Manual Deploy" → "Deploy latest commit"
```

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Alchemy Docs**: https://docs.alchemy.com/
- **Sepolia Etherscan**: https://sepolia.etherscan.io/
- **Render Community**: https://community.render.com/
- **Your GitHub Repo**: https://github.com/lifeofr3-svg/medical-block

---

## Summary

1. ✅ Set up Alchemy account and get API key
2. ✅ Create/import wallet and get test ETH
3. ✅ Push code to GitHub
4. ✅ Create Render web service
5. ✅ Configure environment variables
6. ✅ Deploy and monitor logs
7. ✅ Test your app
8. ✅ Save contract address

**Your app should now be live!** 🚀

Access it at: `https://blockchain-medical-app-xxxx.onrender.com`

View transactions at: `https://sepolia.etherscan.io/address/YOUR_CONTRACT_ADDRESS`
