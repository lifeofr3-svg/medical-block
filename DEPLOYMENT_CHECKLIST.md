# Quick Deployment Checklist

## Before You Start - Gather These

### 1. Alchemy Setup
- [ ] Alchemy account created at https://www.alchemy.com/
- [ ] New app created (Ethereum → Sepolia network)
- [ ] **API Key copied**: `___________________________________`

### 2. Wallet Setup
- [ ] MetaMask installed OR wallet generated
- [ ] **Wallet Address**: `0x_____________________________________`
- [ ] **Private Key**: `0x_____________________________________` (KEEP SECRET!)
- [ ] Test ETH received (from https://www.alchemy.com/faucets/ethereum-sepolia)
- [ ] Balance verified: `_____ ETH` (need at least 0.1 ETH)

### 3. Accounts Ready
- [ ] GitHub account
- [ ] Render account at https://render.com/

---

## Deployment Steps

### Step 1: Push to GitHub
```bash
cd "/home/sk/Downloads/C472_Blockchain_medical-20260128T081948Z-3-001 (2)/C472_Blockchain_medical/Blockchain_Medical"
git add .
git commit -m "Configure for Alchemy and Render deployment"
git push origin main
```

### Step 2: Create Render Service
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect to `lifeofr3-svg/medical-block`
4. Configure:
   - **Name**: `blockchain-medical-app`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2`
   - **Instance Type**: `Free`

### Step 3: Add Environment Variables

In Render, add these variables (click "Add Environment Variable" for each):

```
FLASK_ENV = production
ALCHEMY_API_KEY = [paste your Alchemy API key]
BLOCKCHAIN_NETWORK = sepolia
ACCOUNT_ADDRESS = [paste your wallet address]
PRIVATE_KEY = [paste your private key]
SECRET_KEY = [click Generate]
```

**Note:** Python 3.11 is set via `.python-version` file (already in repo)

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for build
3. Watch logs for "✓ Contract deployed successfully!"
4. Copy your app URL

### Step 5: Test
1. Open your Render app URL
2. Create account and login
3. Test predictions
4. Verify on https://sepolia.etherscan.io/

---

## What You'll See

### Successful Build Logs:
```
==> Installing dependencies...
==> Build successful!
==> Starting service...
✓ Connected to blockchain network
  Balance: 0.5 ETH
✓ Contract deployed successfully!
  Contract address: 0x...
```

### Your App URL:
```
https://blockchain-medical-app-xxxx.onrender.com
```

---

## Quick Reference

| Need | Get From |
|------|----------|
| Alchemy API Key | https://dashboard.alchemy.com/ → Your App → View Key |
| Test ETH | https://www.alchemy.com/faucets/ethereum-sepolia |
| Wallet (MetaMask) | Install from https://metamask.io/ |
| View Transactions | https://sepolia.etherscan.io/ |
| Render Dashboard | https://render.com/dashboard |
| GitHub Repo | https://github.com/lifeofr3-svg/medical-block |

---

## Emergency Contacts

**Build failing?**
- Read full guide: `RENDER_DEPLOYMENT_STEPS.md`

**Alchemy setup issues?**
- Read: `ALCHEMY_SETUP.md` or `MIGRATION_GUIDE.md`

**Need to test locally first?**
- Run: `python test_alchemy_connection.py`

---

## Common Issues

### "Insufficient funds for gas"
→ Get more test ETH from faucets

### "Cannot connect to blockchain"
→ Check ALCHEMY_API_KEY is correct

### "Build failed"
→ Verify all environment variables are set

### App timeout
→ Wait for cold start (free tier sleeps after inactivity)

---

**Ready? Start with Step 1!** 🚀
