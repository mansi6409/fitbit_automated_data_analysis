# ⚡ Quick Deploy (5 Minutes)

## Streamlit Cloud - Private Repo (FREE)

### Step 1: Push to GitHub (2 min)
```bash
cd /Users/mansigarg/USC/LAB/ocd-research-app/dataanalysis
git add streamlit_app/
git commit -m "Add Streamlit app"
git push
```

### Step 2: Deploy (3 min)

1. Go to: **https://share.streamlit.io/**
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repo:** `your-username/ocd-research-app`
   - **Branch:** `main`
   - **Path:** `dataanalysis/streamlit_app/app.py`
5. Click **"Deploy"**

### Done! 🎉

Your app will be live at: `https://your-app.streamlit.app`

---

## What's Configured ✅

- `.gitignore` - Protects secrets
- `config.toml` - App settings
- `secrets.toml` - Template for AWS (when needed)
- `requirements.txt` - All dependencies

---

## Future: Connect AWS S3

In Streamlit Cloud dashboard:
1. Go to app settings → **Secrets**
2. Add:
```toml
AWS_ACCESS_KEY_ID = "your-key"
AWS_SECRET_ACCESS_KEY = "your-secret"
S3_BUCKET_NAME = "your-bucket"
```

---

## Update App

Just push to GitHub - auto-deploys! ✨
```bash
git push
```

---

**Cost:** FREE forever for private repos!

