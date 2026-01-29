# Deployment Guide for Render (Python 3.11)

This guide will help you deploy the Blockchain Medical Application to Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. A GitHub account to host your code
3. A blockchain node URL (if using Ganache locally, you'll need to expose it or use a public testnet)

## Step 1: Prepare Your Repository

1. Initialize a git repository (if not already done):
   ```bash
   git init
   ```

2. Add all files:
   ```bash
   git add .
   git commit -m "Initial commit for Render deployment"
   ```

3. Create a new repository on GitHub and push your code:
   ```bash
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

## Step 2: Set Up Render

### Option A: Using render.yaml (Recommended)

1. Go to https://render.com/dashboard
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Review the configuration and click "Apply"

### Option B: Manual Setup

1. Go to https://render.com/dashboard
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: blockchain-medical-app
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2`
   - **Instance Type**: Free (or select a paid plan for better performance)

## Step 3: Configure Environment Variables

In the Render dashboard, go to your service and add the following environment variables:

### Required Variables:

1. **PYTHON_VERSION**: `3.11.0`
2. **SECRET_KEY**: Generate a random secret key (use https://randomkeygen.com/ or run `python -c "import secrets; print(secrets.token_hex(32))"`)
3. **FLASK_ENV**: `production`

### Blockchain Variables (Update these with your values):

4. **GANACHE_URL**: Your blockchain node URL
   - If using local Ganache, you'll need to expose it via ngrok or use a public testnet
   - For testing, consider using Infura (https://infura.io/) or Alchemy (https://www.alchemy.com/)
   - Example: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`

5. **ACCOUNT_ADDRESS**: Your Ethereum account address
   - Example: `0x22859a802657c4012d90Ba3259a707aD4559f6A9`

6. **PRIVATE_KEY**: Your private key (KEEP THIS SECRET!)
   - Example: `0xbb92e4d51d7947e632be0fb260f4dd9aba3e7b63a50e466259ff800889d49305`
   - **Important**: Never commit this to GitHub!

### Optional Variables:

7. **UPLOAD_FOLDER**: `uploads` (default)
8. **DATABASE_PATH**: `users.db` (default)

## Step 4: Important Notes

### Model Files

Your ML models in the `models/` directory need to be present:
- `diabetes_xgboost_model.pkl`
- `diabetes_scaler.pkl`
- `heart_xgboost_model.pkl`
- `heart_scaler.pkl`
- `diabetes_retinal_model.pth`
- `heart_ecg_model.pth`

If these files are large (>100MB), consider:
1. Using Git LFS (Large File Storage)
2. Uploading them to cloud storage (S3, Google Cloud Storage) and downloading them during build
3. Using a persistent disk on Render

### Smart Contract Deployment

The app will attempt to deploy the smart contract on startup. Make sure:
1. Your blockchain node is accessible from Render
2. Your account has sufficient funds for gas fees
3. The `contracts/MedicalRecord.sol` file is in your repository

### Database Persistence

The SQLite database (`users.db`) will be ephemeral on Render's free tier. For production:
1. Upgrade to a paid plan with persistent disks
2. Use an external database (PostgreSQL, MySQL)

### Blockchain Considerations

For production deployment:
1. **Don't use local Ganache** - it won't be accessible from Render
2. **Use a public testnet** (Sepolia, Goerli) or mainnet
3. **Use Infura or Alchemy** for reliable blockchain access
4. **Secure your private keys** - use Render's secret environment variables

## Step 5: Deploy

1. Click "Create Web Service" or "Apply" (if using Blueprint)
2. Render will build and deploy your application
3. Monitor the logs for any errors
4. Once deployed, you'll get a URL like: `https://blockchain-medical-app.onrender.com`

## Step 6: Verify Deployment

1. Visit your Render URL
2. Try signing up and logging in
3. Test the prediction functionality
4. Check the Render logs for any errors

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version is 3.11

### App Won't Start
- Check the application logs
- Verify all environment variables are set correctly
- Ensure the blockchain node URL is accessible

### Smart Contract Issues
- Verify your blockchain node is accessible
- Check that your account has funds
- Review the contract deployment logs

### Model Loading Errors
- Ensure all model files are present in the `models/` directory
- Check file permissions
- Verify PyTorch models are compatible with CPU (use `map_location='cpu'`)

## Security Recommendations

1. **Never commit sensitive data** to GitHub
2. **Use environment variables** for all secrets
3. **Regenerate SECRET_KEY** for production
4. **Use a secure blockchain node** (not localhost)
5. **Enable HTTPS** (Render provides this by default)
6. **Regularly update dependencies** for security patches

## Scaling

For better performance:
1. Upgrade to a paid Render plan
2. Increase the number of workers: `--workers 4`
3. Use a CDN for static files
4. Enable database connection pooling
5. Consider using Redis for caching

## Support

If you encounter issues:
1. Check Render documentation: https://render.com/docs
2. Review the application logs in Render dashboard
3. Test locally first before deploying

## Local Testing Before Deployment

Test your deployment configuration locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your-secret-key"
export FLASK_ENV="production"
export PORT=5000

# Run with gunicorn (same as Render)
gunicorn app:app --bind 0.0.0.0:5000 --timeout 120 --workers 2
```

Good luck with your deployment!
