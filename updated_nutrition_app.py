import streamlit as st
st.set_page_config(page_title="NutriAI Assistant", layout="wide")  # ✅ Must be first

from diet_bot import ask_diet_bot, generate_diet_plan
from database import save_user_profile, get_user_profile, register_user, get_user_by_email
from firebase_auth_fixed import sign_up, sign_in, get_user_info, send_password_reset_email, verify_id_token
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Custom CSS for modern UI
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --primary-color: #10B981;
        --secondary-color: #F0FDF4;
        --accent-color: #059669;
        --text-primary: #111827;
        --text-secondary: #6B7280;
        --background: #FFFFFF;
        --border-color: #E5E7EB;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Reset and base styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
    }
    
    /* Header styling */
    .main-header {
        background: white;
        padding: 2rem 0;
        border-radius: 20px;
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid var(--border-color);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        font-weight: 400;
    }
    
    /* Authentication form styling */
    .auth-container {
        background: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        max-width: 500px;
        margin: 2rem auto;
    }
    
    .auth-title {
        font-size: 2rem;
        font-weight: 600;
        color: var(--text-primary);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .auth-subtitle {
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        margin: 1rem 0;
        transition: transform 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Stats display */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        flex: 1;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 25px -5px rgba(16, 185, 129, 0.3);
    }
    
    /* Form styling */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid var(--border-color);
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: white;
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: var(--secondary-color);
        border: 1px solid var(--primary-color);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Navigation styling */
    .nav-container {
        background: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        box_shadow: var(--shadow);
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: var(--text-primary);
        font-weight: 500;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

# Authentication functions
def show_login_page():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="auth-title">🥗 Welcome Back</h2>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Sign in to access your personalized nutrition assistant</p>', unsafe_allow_html=True)
    
    # Google Sign-In button
    if st.button("🔵 Sign In with Google", use_container_width=True):
        st.warning("⚠️ Google Sign-In is not implemented in this environment.")
        # You would add here the Google OAuth popup flow or redirect for real app
    
    with st.form("login_form"):
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_button = st.form_submit_button("Sign In", use_container_width=True)
        
        if login_button:
            email = email.strip() # Remove leading/trailing whitespace

            if email and password:
                # Basic email format check (optional, Firebase will do its own)
                if "@" not in email or "." not in email:
                    st.error("❌ Please enter a valid email address format.")
                else:
                    success, result = sign_in(email, password)
                    if success:
                        # Store Firebase user data in session state
                        st.session_state['logged_in'] = True
                        st.session_state['firebase_user'] = result
                        st.session_state['user_email'] = result['email']
                        st.session_state['user_id'] = result['localId']
                        st.session_state['id_token'] = result['idToken']
                        
                        # Try to get user from local database
                        local_user = get_user_by_email(email)
                        if local_user:
                            st.session_state['user_name'] = local_user['name']
                            st.session_state['local_user_id'] = local_user['id']
                        else:
                            st.session_state['user_name'] = email.split('@')[0]  # Use email prefix as name
                            st.session_state['local_user_id'] = None
                        
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        # More descriptive error messages from Firebase
                        if "EMAIL_NOT_FOUND" in result:
                            st.error("❌ No account found with this email. Please sign up.")
                        elif "INVALID_PASSWORD" in result:
                            st.error("❌ Incorrect password. Please try again.")
                        elif "INVALID_EMAIL" in result:
                            st.error("❌ Invalid email format or unverified email. Please check your email or sign up.")
                        elif "USER_DISABLED" in result:
                            st.error("❌ Your account has been disabled. Please contact support.")
                        else:
                            st.error(f"❌ Login failed: {result}")
            else:
                st.warning("⚠️ Please fill in all fields")
    
    # Password reset
    with st.expander("🔑 Forgot Password?"):
        reset_email = st.text_input("Enter your email for password reset", key="reset_email")
        if st.button("Send Password Reset Email"):
            if reset_email:
                res = send_password_reset_email(reset_email)
                if res:
                    st.success("✅ Password reset email sent! Check your inbox.")
                else:
                    st.error("❌ Failed to send reset email. Please try again.")
            else:
                st.warning("⚠️ Please enter your email.")

    st.markdown("</div>", unsafe_allow_html=True)

def show_register_page():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="auth-title">👋 Create Account</h2>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Join us for personalized nutrition guidance</p>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        register_button = st.form_submit_button("Register", use_container_width=True)
        
        if register_button:
            if not (name and email and password and confirm_password):
                st.warning("⚠️ Please fill in all fields")
            elif password != confirm_password:
                st.warning("⚠️ Passwords do not match")
            else:
                success, msg = sign_up(email, password)
                if success:
                    # Register in local DB
                    user_id = register_user(name, email)
                    st.success("✅ Registration successful! Please login.")
                    st.session_state['page'] = 'Login'
                    st.experimental_rerun()
                else:
                    st.error(f"❌ {msg}")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_logout_button():
    if st.button("🚪 Log Out"):
        st.session_state.clear()
        st.experimental_rerun()

def show_navigation():
    st.markdown("""
    <div class="nav-container">
        <div class="user-info">
            👤 Logged in as <strong>{}</strong>
        </div>
        <div>
    """.format(st.session_state.get('user_name', 'User')), unsafe_allow_html=True)
    show_logout_button()
    st.markdown("</div></div>", unsafe_allow_html=True)

def main_app():
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">NutriAI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Your AI-powered personalized nutrition assistant</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    show_navigation()

    menu = ["Home", "Diet Plan Generator", "Ask Nutrition Bot", "My Profile", "Stats"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("Welcome to NutriAI!")
        st.write("Generate your personalized diet plans, ask your nutrition assistant questions, and track your progress — all in one place.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "Diet Plan Generator":
        st.subheader("Create Your Personalized Diet Plan")
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)
        goal = st.selectbox("Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"])
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])
        
        if st.button("Generate Diet Plan"):
            diet_plan = generate_diet_plan(age, weight, height, goal, activity_level)
            st.success("Here is your diet plan:")
            st.write(diet_plan)
            # Optionally save to DB

    elif choice == "Ask Nutrition Bot":
        st.subheader("Ask the Nutrition Assistant")
        question = st.text_area("Your Question")
        if st.button("Ask"):
            if question.strip():
                answer = ask_diet_bot(question)
                st.markdown(f"**Answer:** {answer}")
            else:
                st.warning("Please enter a question.")

    elif choice == "My Profile":
        st.subheader("Your Profile")
        profile = get_user_profile(st.session_state.get('user_email'))
        if profile:
            st.write(f"**Name:** {profile['name']}")
            st.write(f"**Email:** {profile['email']}")
            st.write(f"**Age:** {profile['age']}")
            st.write(f"**Weight:** {profile['weight']} kg")
            st.write(f"**Height:** {profile['height']} cm")
            st.write(f"**Goal:** {profile['goal']}")
            st.write(f"**Activity Level:** {profile['activity_level']}")
        else:
            st.info("No profile found. Please create one.")
            if st.button("Create Profile"):
                save_user_profile(
                    st.session_state.get('user_name'),
                    st.session_state.get('user_email'),
                    25, 70, 175, "Maintain Weight", "Sedentary"
                )
                st.success("Profile created!")
                st.experimental_rerun()

    elif choice == "Stats":
        st.subheader("Your Nutrition Stats")
        # Example static data - replace with real user stats if available
        data = {
            "Date": ["2025-05-01", "2025-05-08", "2025-05-15", "2025-05-22", "2025-05-29"],
            "Weight": [70, 69, 68, 67.5, 67],
            "Calories": [2000, 1950, 1900, 1850, 1800]
        }
        df = pd.DataFrame(data)
        fig = px.line(df, x="Date", y="Weight", title="Weight Over Time")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.bar(df, x="Date", y="Calories", title="Calories Intake Over Time", color="Calories")
        st.plotly_chart(fig2, use_container_width=True)

def main():
    load_custom_css()
    # The st.set_page_config() call has been moved to the very top of the script
    # to adhere to Streamlit's requirement.

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        page = st.sidebar.radio("Choose Authentication", ["Login", "Register"])
        if page == "Login":
            show_login_page()
        else:
            show_register_page()
    else:
        main_app()

if __name__ == "__main__":
    main()