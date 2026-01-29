# Fix: Force Python 3.11 on Render

## Problem
Render is using Python 3.13.4 instead of Python 3.11

## Solution - Push Updated Code

I've created a `runtime.txt` file that forces Python 3.11. Follow these steps:

### Step 1: Push the Fix to GitHub
```bash
cd "/home/sk/Downloads/C472_Blockchain_medical-20260128T081948Z-3-001 (2)/C472_Blockchain_medical/Blockchain_Medical"

git add runtime.txt render.yaml
git commit -m "Force Python 3.11 with runtime.txt"
git push origin main
```

### Step 2: Redeploy on Render

**Option A - Automatic (if auto-deploy is enabled):**
- Render will automatically redeploy after you push
- Wait 2-3 minutes and check the logs

**Option B - Manual:**
1. Go to https://render.com/dashboard
2. Select your service
3. Click "Manual Deploy" → "Deploy latest commit"

### Step 3: Verify Python Version

In the Render logs, you should now see:
```
==> Installing Python version 3.11.0...
```

Instead of:
```
==> Installing Python version 3.13.4...
```

---

## What Changed?

### Created: `runtime.txt`
```
python-3.11.0
```

This file is the standard way to specify Python version on Render (and Heroku).

### Updated: `render.yaml`
Removed the `PYTHON_VERSION` environment variable (not needed with runtime.txt)

---

## Alternative: Update Environment Variable in Render Dashboard

If you prefer not to push code, you can also:

1. Go to Render Dashboard → Your Service → Environment
2. Delete the `PYTHON_VERSION` variable if it exists
3. Go to Settings
4. Under "Build & Deploy" you might see Python version selector
5. Select Python 3.11

But using `runtime.txt` is the recommended approach.

---

## Verify It Worked

After redeployment, check the logs for:
```
==> Installing Python version 3.11.0...
==> Installing dependencies from requirements.txt
```

If you still see 3.13, contact Render support or try:
- Clearing build cache: Dashboard → Settings → "Clear build cache & deploy"
- Then trigger a new deployment
