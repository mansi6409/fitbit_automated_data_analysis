"""
Authentication module for USC Google SSO
Restricts access to @usc.edu and @med.usc.edu email addresses
"""
import streamlit as st

# Allowed email domains
ALLOWED_DOMAINS = ["usc.edu", "med.usc.edu"]


def check_authentication():
    """
    Check if user is authenticated with a valid USC email.
    Returns True if authenticated, False otherwise.
    """
    # Check if already authenticated in session
    if st.session_state.get("authenticated", False):
        return True
    
    # Try to import and use streamlit-google-auth
    try:
        from streamlit_google_auth import Authenticate
        
        # Initialize authenticator
        authenticator = Authenticate(
            secret_credentials_path='google_credentials.json',
            cookie_name='ocd_research_auth',
            cookie_key=st.secrets.get("auth", {}).get("cookie_key", "ocd_research_secret_key_change_me"),
            redirect_uri=st.secrets.get("auth", {}).get("redirect_uri", "http://localhost:8501"),
        )
        
        # Check authentication status
        authenticator.check_authentification()
        
        # If connected via Google
        if st.session_state.get('connected', False):
            user_email = st.session_state.get('user_info', {}).get('email', '')
            
            # Check if email is from allowed domain
            if is_allowed_email(user_email):
                st.session_state.authenticated = True
                st.session_state.user_email = user_email
                st.session_state.user_name = st.session_state.get('user_info', {}).get('name', 'User')
                return True
            else:
                # Email not from allowed domain
                _show_access_denied(user_email, authenticator)
                return False
        else:
            # Not connected - show login page
            _show_login_page(authenticator)
            return False
            
    except ImportError:
        # Fallback to simple password auth if streamlit-google-auth not installed
        return _fallback_password_auth()
    except FileNotFoundError:
        # google_credentials.json not found - use secrets or fallback
        return _fallback_password_auth()
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return _fallback_password_auth()


def is_allowed_email(email: str) -> bool:
    """Check if email is from an allowed domain."""
    if not email:
        return False
    
    email_lower = email.lower()
    for domain in ALLOWED_DOMAINS:
        if email_lower.endswith(f"@{domain}"):
            return True
    return False


def _show_login_page(authenticator=None):
    """Display the login page."""
    # Custom CSS for login page
    st.markdown("""
    <style>
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 2rem;
            text-align: center;
        }
        .login-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            font-size: 1.1rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }
        .login-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 1rem;
            padding: 2rem;
            color: white;
            margin: 2rem 0;
        }
        .usc-info {
            background-color: #fffbeb;
            border: 1px solid #fbbf24;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔬 OCD Research Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Fitbit Data Analysis for Research</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="usc-info">
        🎓 <strong>USC Researchers Only</strong><br>
        Access is restricted to <code>@usc.edu</code> and <code>@med.usc.edu</code> email addresses.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Sign in to continue")
    
    if authenticator:
        # Show Google login button
        authenticator.login()
    else:
        st.info("Google authentication is being configured. Please use password login below.")
    
    st.markdown('</div>', unsafe_allow_html=True)


def _show_access_denied(email: str, authenticator=None):
    """Show access denied message for non-USC emails."""
    st.markdown("""
    <style>
        .denied-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 2rem;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="denied-container">', unsafe_allow_html=True)
    
    st.error("⛔ Access Denied")
    st.markdown(f"""
    ### You don't have access to this application.
    
    **Your email:** `{email}`
    
    This application is restricted to USC researchers with:
    - `@usc.edu` email addresses
    - `@med.usc.edu` email addresses
    
    If you believe you should have access, please contact the lab administrator.
    """)
    
    if authenticator:
        if st.button("🔄 Sign in with a different account", type="primary"):
            authenticator.logout()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def _fallback_password_auth():
    """Fallback to simple password authentication."""
    
    if st.session_state.get("authenticated", False):
        return True
    
    st.markdown("""
    <style>
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🔬 OCD Research Platform")
    st.markdown("### 🔐 Login Required")
    
    st.info("🎓 Access is restricted to authorized USC researchers.")
    
    # Get password from secrets or use default for development
    correct_password = st.secrets.get("auth", {}).get("password", None)
    
    if correct_password is None:
        st.warning("""
        ⚠️ **Setup Required**: No password configured.
        
        To enable authentication, add to `.streamlit/secrets.toml`:
        ```toml
        [auth]
        password = "your_secure_password"
        ```
        """)
        # Allow access for development if no password set
        if st.button("Continue without authentication (Development only)", type="secondary"):
            st.session_state.authenticated = True
            st.session_state.user_email = "developer@local"
            st.session_state.user_name = "Developer"
            st.rerun()
        return False
    
    # Password input
    with st.form("login_form"):
        password = st.text_input("Enter lab password:", type="password")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submitted:
            if password == correct_password:
                st.session_state.authenticated = True
                st.session_state.user_email = "authenticated@usc.edu"
                st.session_state.user_name = "USC Researcher"
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
    
    return False


def show_user_info():
    """Display current user info in sidebar."""
    if st.session_state.get("authenticated", False):
        user_name = st.session_state.get("user_name", "User")
        user_email = st.session_state.get("user_email", "")
        
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"👤 **{user_name}**")
            if user_email:
                st.caption(f"📧 {user_email}")


def logout_button():
    """Show logout button in sidebar."""
    if st.session_state.get("authenticated", False):
        with st.sidebar:
            if st.button("🚪 Logout", use_container_width=True):
                # Clear all auth-related session state
                for key in ['authenticated', 'user_email', 'user_name', 'connected', 'user_info']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()


def require_auth(func):
    """Decorator to require authentication for a function."""
    def wrapper(*args, **kwargs):
        if not check_authentication():
            st.stop()
        return func(*args, **kwargs)
    return wrapper

