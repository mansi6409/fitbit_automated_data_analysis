# Authentication Setup Guide

This app supports two authentication methods:
1. **Simple Password** (Quick, 2 minutes) - Recommended for getting started
2. **Google OAuth** (More secure, 20 minutes) - Recommended for production

---

## Option 1: Simple Password Authentication (Quickest)

This is the easiest way to protect your app. Just set a password and share it with your lab members.

### Step 1: Set Your Password

In Streamlit Cloud:
1. Go to your app dashboard: https://share.streamlit.io
2. Click on your app → **Settings** → **Secrets**
3. Add or update the `[auth]` section:

```toml
[auth]
password = "YourSecurePasswordHere"
```

### Step 2: Share with Lab Members

Tell your lab members:
1. Go to https://fitbit-data-analysis.streamlit.app
2. Enter the password: `YourSecurePasswordHere`
3. Click Login

That's it! ✅

---

## Option 2: Google OAuth (USC Email Restriction)

This option allows users to sign in with their USC Google accounts. Only `@usc.edu` and `@med.usc.edu` emails will have access.

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **New Project**
3. Name it: `OCD Research App`
4. Click **Create**

### Step 2: Enable OAuth Consent Screen

1. In Google Cloud Console, go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (unless you have Google Workspace, then use Internal)
3. Fill in:
   - App name: `OCD Research Data Platform`
   - User support email: Your email
   - Developer contact: Your email
4. Click **Save and Continue**
5. Skip Scopes (click Save and Continue)
6. Add test users (your email and lab members) if using External
7. Click **Save and Continue**

### Step 3: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth 2.0 Client ID**
3. Application type: **Web application**
4. Name: `Streamlit App`
5. Add **Authorized redirect URIs**:
   - `http://localhost:8501` (for local development)
   - `https://fitbit-data-analysis.streamlit.app` (your deployed app URL)
6. Click **Create**
7. **Copy** the Client ID and Client Secret

### Step 4: Configure Streamlit Secrets

#### For Local Development

Create/update `.streamlit/secrets.toml`:

```toml
[auth]
redirect_uri = "http://localhost:8501"
cookie_key = "your_random_secret_key_here_make_it_long"
```

Create `google_credentials.json` in your project root:

```json
{
    "web": {
        "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "client_secret": "YOUR_CLIENT_SECRET",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}
```

#### For Streamlit Cloud

1. Go to your app on [share.streamlit.io](https://share.streamlit.io)
2. Click **Settings** → **Secrets**
3. Add:

```toml
[auth]
redirect_uri = "https://fitbit-data-analysis.streamlit.app"
cookie_key = "your_random_secret_key_here_make_it_long"

[google_oauth]
client_id = "YOUR_CLIENT_ID.apps.googleusercontent.com"
client_secret = "YOUR_CLIENT_SECRET"
```

### Step 5: Update .gitignore

Make sure these files are NOT committed to git:

```
.streamlit/secrets.toml
google_credentials.json
```

---

## How Authentication Works

### With Simple Password:
1. User visits the app
2. Sees a password prompt
3. Enters the shared lab password
4. Gets access to all features

### With Google OAuth:
1. User visits the app
2. Clicks "Sign in with Google"
3. Signs in with their Google account
4. App checks if email ends with `@usc.edu` or `@med.usc.edu`
5. If yes → Access granted
6. If no → Access denied with message

---

## Allowed Email Domains

The app is configured to allow these email domains:
- `@usc.edu`
- `@med.usc.edu`

To modify allowed domains, edit `utils/auth.py`:

```python
ALLOWED_DOMAINS = ["usc.edu", "med.usc.edu"]
```

---

## Troubleshooting

### "Authentication error" message
- Check that your secrets are properly configured in Streamlit Cloud
- Make sure the redirect URI matches exactly

### Google OAuth not working
- Verify the OAuth consent screen is configured
- Check that redirect URIs are correct
- Make sure the app is published (not in testing mode) or users are added as test users

### Password not working
- Check the password in Streamlit Cloud secrets
- Make sure there are no extra spaces

---

## Security Notes

1. **Never commit secrets to git** - Always use `.streamlit/secrets.toml` or Streamlit Cloud secrets
2. **Change default passwords** - Don't use the example passwords
3. **Rotate credentials periodically** - Update passwords/keys regularly
4. **Monitor access** - Check who's using the app

---

## Quick Reference

| Method | Setup Time | Security | Best For |
|--------|------------|----------|----------|
| Password | 2 min | Medium | Quick setup, small teams |
| Google OAuth | 20 min | High | Production, larger teams |

