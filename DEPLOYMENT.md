# 🚀 Deployment Guide

## Streamlit Community Cloud (FREE - Private Repo)

### Prerequisites
- Private GitHub repository (already done ✅)
- Streamlit account (free)

---

## 📋 Step-by-Step Deployment

### 1. Commit and Push Your Code

```bash
cd /Users/mansigarg/USC/LAB/ocd-research-app/dataanalysis

# Check status
git status

# Add the streamlit app
git add streamlit_app/

# Commit
git commit -m "Add Streamlit OCD Fitbit Analysis App"

# Push to GitHub
git push origin main
```

### 2. Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Grant access** to your private repository when prompted

4. **Click "New app"**

5. **Fill in the form:**
   - **Repository:** `your-username/ocd-research-app`
   - **Branch:** `main` (or your branch name)
   - **Main file path:** `dataanalysis/streamlit_app/app.py`
   - **App URL:** Choose a custom name (optional)

6. **Click "Deploy!"** 🚀

### 3. Wait for Deployment (2-3 minutes)

Streamlit will:
- ✅ Install dependencies from `requirements.txt`
- ✅ Build your app
- ✅ Give you a URL

---

## 🔐 Adding Secrets (For Future AWS Integration)

When you're ready to connect to AWS S3:

1. **In Streamlit Cloud dashboard:**
   - Go to your app settings
   - Click "Secrets"
   - Add your secrets in TOML format:

```toml
AWS_ACCESS_KEY_ID = "your-key-id"
AWS_SECRET_ACCESS_KEY = "your-secret-key"
AWS_DEFAULT_REGION = "us-east-1"
S3_BUCKET_NAME = "your-bucket-name"
```

2. **In your code**, access them like this:

```python
import streamlit as st

aws_key = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret = st.secrets["AWS_SECRET_ACCESS_KEY"]
```

---

## 🔄 Updating Your Deployed App

Super easy - just push to GitHub:

```bash
# Make your changes
git add .
git commit -m "Update analysis features"
git push

# Streamlit auto-deploys! ✅
```

---

## 🎯 Your App URL

After deployment, you'll get a URL like:
```
https://your-app-name.streamlit.app
```

Or custom subdomain:
```
https://ocd-fitbit-analysis.streamlit.app
```

---

## 🛠️ Troubleshooting

### App won't deploy?

**Check:**
1. `requirements.txt` is in `streamlit_app/` folder
2. File path is correct: `dataanalysis/streamlit_app/app.py`
3. All dependencies have version numbers

**View logs:**
- Click "Manage app" in Streamlit Cloud
- Check the terminal output

### Need to restart the app?

1. Go to app settings
2. Click "Reboot app"

### Want to delete and redeploy?

1. Go to app settings
2. Click "Delete app"
3. Deploy again

---

## 💰 Cost Breakdown

### Streamlit Community Cloud (Private Repo)
- **Cost:** FREE
- **Limitations:**
  - 1 GB RAM per app
  - 1 CPU core
  - Can sleep after inactivity (wakes on visit)
  
**This is perfect for your use case!**

### If you need more resources later:

**Streamlit Cloud Teams ($250/month)**
- 4 private apps
- 2 GB RAM per app
- No sleep mode
- Priority support

**AWS Lightsail ($5-10/month)**
- Full control
- More resources
- Manual deployment

---

## 🔒 Security Best Practices

### ✅ Already Done:
- `.gitignore` configured to exclude secrets
- `secrets.toml` excluded from git

### ⚠️ Important:
- Never commit AWS credentials to git
- Always use Streamlit secrets for sensitive data
- Keep your repo private for research data

---

## 📊 Monitoring Your App

**Streamlit Cloud provides:**
- Real-time logs
- Resource usage metrics
- Error tracking
- Analytics (views, users)

**Access:** Dashboard → Your App → Analytics

---

## 🎓 For Lab Research Assistants

### Accessing the App:
Share the URL with your RAs:
```
https://your-app.streamlit.app
```

### No login required!
- Anyone with the URL can access
- Consider adding basic password protection if needed

### Adding Password Protection (Optional):

Add to `app.py`:
```python
import streamlit as st

def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", key="password")
        if st.session_state.password == st.secrets["app_password"]:
            st.session_state.password_correct = True
            st.rerun()
        elif st.session_state.password:
            st.error("Incorrect password")
        return False
    return True

if not check_password():
    st.stop()
```

---

## 📞 Need Help?

**Streamlit Community Forum:**
https://discuss.streamlit.io/

**Documentation:**
https://docs.streamlit.io/streamlit-community-cloud

**GitHub Issues:**
https://github.com/streamlit/streamlit/issues

---

## ✨ You're All Set!

Your deployment is configured and ready to go. Just follow the steps above and you'll have your app live in 5 minutes! 🚀

