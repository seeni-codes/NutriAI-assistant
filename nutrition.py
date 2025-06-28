
import streamlit as st
st.set_page_config(page_title="NutriAI Assistant", layout="wide")

from diet_bot import ask_diet_bot, generate_diet_plan
from database import save_user_profile, get_user_profile, register_user, get_user_by_email
from firebase import sign_up, sign_in, get_user_info, send_password_reset_email, verify_id_token
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- IMAGE PATH (Used for general background, not specific login/register page now) ---
BACKGROUND_IMAGE_PATH = "background_salad.jpg" # <--- Change this to your image file name
# Make sure this image is in the same directory as your Python script,
# or provide the correct relative/absolute path.

# Custom CSS for modern UI and background image
def load_custom_css():
    st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Main theme colors - **NAVY BLUE AND RED** */
    :root {{
        --primary-color: #003f5c; /* Dark Navy Blue */
        --secondary-color: #e0f2f7; /* Light Blue/Gray */
        --accent-color: #d62839; /* Red */
        --text-primary: #264653; /* Dark Gray-Blue */
        --text-secondary: #457b9d; /* Medium Blue */
        --background-light: #f8f9fa; /* Very Light Gray */
        --background-dark: #1d3557; /* Darker Navy Blue for login */
        --border-color: #adb5bd; /* Medium Gray Border */
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --dark-overlay: rgba(0,0,0,0.4); /* For text readability over images */
        --light-overlay: rgba(255,255,255,0.7); /* For boxes over images */
        --auth-background-color: #eceff1; /* Light Gray-Blue for login page background */
    }}

    /* General App Background */
    .stApp {{
        font-family: 'Inter', sans-serif;
        background-color: var(--background-light); /* Default light background */
        background-image: url('file/{BACKGROUND_IMAGE_PATH}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed; /* Fixed background */
    }}

    /* Specific background for login/register pages */
    .stApp.login-bg, .stApp.register-bg {{
        background-image: none; /* Remove image for auth pages */
        background-color: var(--auth-background-color); /* Solid color for auth pages */
    }}

    /* Apply a translucent overlay to the main content area for readability */
    .main .block-container {{
        background: rgba(255, 255, 255, 0.95); /* Slightly transparent white background for content */
        border-radius: 15px;
        padding: 2rem; /* Add some padding */
        margin-top: 2rem; /* Push content down slightly from top */
        box-shadow: var(--shadow);
    }}

    /* Header styling */
    .main-header {{
        background: rgba(255, 255, 255, 0.95); /* Slightly more opaque for header */
        padding: 2rem 0;
        border-radius: 20px;
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(5px); /* Frosty glass effect */
        -webkit-backdrop-filter: blur(5px);
    }}

    .main-title {{
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color), #457b9d); /* Navy to Medium Blue gradient */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}

    .main-subtitle {{
        font-size: 1.2rem;
        color: var(--text-secondary);
        font-weight: 400;
    }}

    /* Authentication form styling - Adjusted for image look */
    .auth-container {{
        background: #FFFFFF; /* Solid white background for the card */
        padding: 3rem 2rem;
        border-radius: 15px; /* Slightly less rounded */
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15); /* More prominent shadow */
        border: none; /* No border for the card itself */
        max-width: 380px; /* Narrower card */
        margin: 6rem auto; /* Center vertically and horizontally */
        text-align: center; /* Center content within the card */
    }}

    .auth-logo {{
        font-size: 3rem; /* Larger icon */
        margin-bottom: 1rem;
        color: var(--primary-color); /* Navy Blue logo */
    }}

    .auth-welcome-text {{
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-primary); /* Dark Gray-Blue text */
        margin-bottom: 0.5rem;
    }}

    .auth-tagline {{
        color: var(--text-secondary); /* Medium Blue tagline */
        font-size: 0.9rem;
        margin-bottom: 2.5rem; /* More space before inputs */
    }}

    /* Streamlit's form container alignment within auth-container */
    .auth-container > form {{
        text-align: left; /* Align form elements to the left within the card */
    }}

    /* Input fields within auth-container */
    .auth-container .stTextInput > label,
    .auth-container .stNumberInput > label,
    .auth-container .stTextArea > label,
    .auth-container .stSelectbox > label {{
        color: var(--text-primary); /* Dark Gray-Blue labels */
        font-weight: 500;
        margin-bottom: 0.5rem;
        display: block; /* Make label a block for proper spacing */
    }}

    .auth-container .stTextInput > div > div > input,
    .auth-container .stTextArea > div > div > textarea,
    .auth-container .stNumberInput > div > div > input {{
        background: var(--background-light); /* Lighter background for inputs */
        border: 1px solid var(--border-color); /* Medium Gray border */
        border-radius: 8px;
        padding: 0.85rem 1rem; /* More padding */
        font-size: 1rem;
        width: 100%; /* Ensure full width */
        margin-bottom: 1.2rem; /* Spacing between inputs */
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); /* Subtle inner shadow */
    }}

    .auth-container .stTextInput > div > div > input:focus,
    .auth-container .stTextArea > div > div > textarea:focus,
    .auth-container .stNumberInput > div > div > input:focus {{
        border-color: var(--primary-color); /* Navy Blue focus */
        box-shadow: 0 0 0 2px rgba(0, 63, 92, 0.2); /* Slightly transparent Navy focus glow */
    }}

    /* Auth buttons */
    .auth-container .stButton > button {{
        background: linear-gradient(90deg, #0077b6, #00a8e8); /* Blue gradient for login/register buttons */
        color: white;
        border: none;
        padding: 0.85rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(0, 119, 182, 0.3);
        margin-top: 1rem; /* Space above button */
    }}
    
    .auth-container .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 119, 182, 0.4);
        background: linear-gradient(90deg, #00a8e8, #0077b6); /* Hover reverse gradient */
    }}

    /* OR separator */
    .auth-separator {{
        color: var(--text-secondary); /* Medium Blue OR */
        margin: 2rem 0;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        text-align: center;
    }}
    .auth-separator::before, .auth-separator::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid var(--border-color); /* Medium Gray border */
    }}
    .auth-separator:not(:empty)::before {{
        margin-right: .5em;
    }}
    .auth-separator:not(:empty)::after {{
        margin-left: .5em;
    }}

    /* Password Reset / Signup links */
    .auth-link-text {{
        font-size: 0.9rem;
        color: var(--text-secondary); /* Medium Blue links */
        margin-top: 1.5rem;
    }}
    .auth-link-text a {{
        color: var(--primary-color); /* Navy Blue link */
        text-decoration: none;
        font-weight: 500;
    }}
    .auth-link-text a:hover {{
        text_decoration: underline;
        color: var(--accent-color); /* Red hover on links */
    }}

    /* Card styling */
    .feature-card {{
        background: rgba(255, 255, 255, 0.9); /* Slightly transparent */
        padding: 2rem;
        border-radius: 16px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color); /* Medium Gray border */
        margin: 1rem 0;
        transition: transform 0.2s ease;
        backdrop-filter: blur(3px);
        -webkit-backdrop-filter: blur(3px);
    }}

    .feature-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.15);
        border-color: var(--primary-color); /* Navy Blue hover border */
    }}

    .card-title {{
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary-color); /* Navy Blue title */
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    /* Stats display */
    .stats-container {{
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }}

    .stat-card {{
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        flex: 1;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color); /* Medium Gray border */
        backdrop-filter: blur(3px);
        -webkit-backdrop-filter: blur(3px);
    }}

    .stat-number {{
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent-color); /* Red stat number */
    }}

    .stat-label {{
        color: var(--text-secondary); /* Medium Blue label */
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }}

    /* Button styling (general, for internal app pages) */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary-color), #457b9d); /* Navy to Medium Blue gradient */
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: var(--shadow);
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 8px 25px -5px rgba(0, 63, 92, 0.3); /* Navy Blue hover shadow */
        background: linear-gradient(135deg, #457b9d, var(--primary-color)); /* Hover reverse gradient */
    }}

    /* Form styling (general, for internal app pages) */
    .stSelectbox > div > div {{
        background: white;
        border: 2px solid var(--border-color); /* Medium Gray border */
        border-radius: 8px;
    }}

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {{
        background: white;
        border: 2px solid var(--border-color); /* Medium Gray border */
        border-radius: 8px;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--accent-color); /* Red focus */
        box_shadow: 0 0 0 3px rgba(214, 40, 57, 0.1); /* Red focus glow */
    }}

    /* Success/Error messages */
    .stSuccess {{
        background: var(--secondary-color); /* Light Blue/Gray success */
        border: 1px solid var(--primary-color); /* Navy Blue success border */
        color: var(--text-primary); /* Dark Gray-Blue success text */
        border-radius: 8px;
        padding: 1rem;
    }}

    .stError {{
        background: #ffe0b2; /* Light Orange-Red error background */
        border: 1px solid var(--accent-color); /* Red error border */
        color: var(--accent-color); /* Red error text */
        border-radius: 8px;
        padding: 1rem;
    }}

    .stWarning {{
        background: #fff8e1; /* Light Yellow warning background */
        border: 1px solid #ffc107; /* Yellow warning border */
        color: #ffc107; /* Yellow warning text */
        border-radius: 8pt;
        padding: 1rem;
    }}

    /* Navigation styling */
    .nav-container {{
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem 2rem;
        border-radius: 12px;
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border-bottom: 1px solid var(--border-color); /* Medium Gray bottom border */
    }}

    .user-info {{
        display: flex;
        align-items: center;
        gap: 1rem;
        color: var(--text-primary); /* Dark Gray-Blue user info */
        font-weight: 500;
    }}

    /* Hero Section (for initial landing if not logged in) */
    .hero-section {{
        text-align: center;
        padding: 6rem 2rem; /* More vertical padding */
        color: white; /* Text color over dark background */
        background: var(--dark-overlay); /* Overlay to make text readable */
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('file/{BACKGROUND_IMAGE_PATH}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .hero-title {{
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5); /* Text shadow for readability */
    }}

    .hero-subtitle {{
        font-size: 1.8rem;
        font-weight: 500;
        margin-bottom: 2rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }}

    .hero-buttons .stButton > button {{
        background: var(--primary-color); /* Navy Blue hero button */
        border: 2px solid var(--primary-color); /* Navy Blue hero button border */
        font-size: 1.2rem;
        padding: 1rem 3rem;
        margin: 0 1rem;
    }}
    .hero-buttons .stButton > button:hover {{
        background: var(--accent-color); /* Red hero button hover */
        border-color: var(--accent-color); /* Red hero button hover border */
    }}

    /* Sidebar styling */
    .st-emotion-cache-1ldf151 > div:first-child {{
        background: rgba(255, 255, 255, 0.95); /* Sidebar background */
        border-right: 1px solid var(--border-color); /* Medium Gray sidebar border */
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }}
    .st-emotion-cache-1ldf151 > div > section.main {{
        background: none; /* Reset main content background if needed */
    }}

    /* Specific overrides for Streamlit's default container backgrounds */
    .st-emotion-cache-gh2jqy, .st-emotion-cache-1y4pz8r {{
        background: none;
    }}

    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    </style>
    """, unsafe_allow_html=True)

# Authentication functions
def show_login_page():
    # Add class to body for specific background color
    st.markdown('<script>document.body.classList.add("login-bg");</script>', unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-logo">🥗</div>', unsafe_allow_html=True) # Simple logo icon
    st.markdown('<h2 class="auth-welcome-text">Welcome Back!</h2>', unsafe_allow_html=True)
    st.markdown('<p class="auth-tagline">Sign in to your account</p>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="your.email@example.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        # Removed key from st.form_submit_button
        login_button = st.form_submit_button("LOGIN", use_container_width=True)
        
        if login_button:
            email = email.strip() 
            if email and password:
                if "@" not in email or "." not in email:
                    st.error("❌ Please enter a valid email address format.")
                else:
                    success, result = sign_in(email, password)
                    if success:
                        st.session_state['logged_in'] = True
                        st.session_state['firebase_user'] = result
                        st.session_state['user_email'] = result['email']
                        st.session_state['user_id'] = result['localId']
                        st.session_state['id_token'] = result['idToken']
                        
                        local_user = get_user_by_email(email)
                        if local_user:
                            st.session_state['user_name'] = local_user['name']
                            st.session_state['local_user_id'] = local_user['id']
                        else:
                            st.session_state['user_name'] = email.split('@')[0]
                            st.session_state['local_user_id'] = None
                        
                        st.success("✅ Login successful!")
                        st.rerun() # Replaced st.experimental_rerun()
                    else:
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
    
    st.markdown('<p class="auth-link-text">', unsafe_allow_html=True)
    st.markdown('<a href="#" onclick="window.parent.document.querySelector(\'button[key=forgot_password_link]\').click(); return false;">Forgot Password?</a>', unsafe_allow_html=True)
    st.markdown('</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="auth-link-text" style="margin-top: 2rem;">Don\'t have an account? <a href="#" onclick="window.parent.document.querySelector(\'button[key=register_link_from_login]\').click(); return false;">Sign Up</a></p>', unsafe_allow_html=True)
    
    # Hidden buttons to trigger page navigation
    st.button("Register", key="register_link_from_login", on_click=lambda: st.session_state.update(page='Register'), help="Hidden", disabled=True)
    st.button("Forgot Password Link Trigger", key="forgot_password_link", on_click=lambda: st.session_state.update(show_forgot_password=True), help="Hidden", disabled=True)

    if st.session_state.get('show_forgot_password'):
        with st.expander("🔑 Reset Password", expanded=True):
            reset_email = st.text_input("Enter your email for password reset", key="reset_email_auth_page", placeholder="your.email@example.com")
            # Removed key from st.form_submit_button
            if st.button("Send Reset Email"):
                if reset_email:
                    success, msg = send_password_reset_email(reset_email.strip())
                    if success:
                        st.success("✅ Password reset email sent! Check your inbox.")
                        st.session_state['show_forgot_password'] = False # Collapse after sending
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.warning("⚠️ Please enter your email.")


    st.markdown("</div>", unsafe_allow_html=True)

def show_register_page():
    # Add class to body for specific background color
    st.markdown('<script>document.body.classList.add("register-bg");</script>', unsafe_allow_html=True)

    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-logo">📝</div>', unsafe_allow_html=True) # Simple logo icon
    st.markdown('<h2 class="auth-welcome-text">Create Account</h2>', unsafe_allow_html=True)
    st.markdown('<p class="auth-tagline">Join us for personalized nutrition guidance</p>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        name = st.text_input("Full Name", key="reg_name", placeholder="John Doe")
        email = st.text_input("Email", key="reg_email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", key="reg_password", placeholder="Choose a strong password")
        confirm_password = st.text_input("Verify Password", type="password", key="reg_confirm_password", placeholder="Re-enter your password")
        
        # Removed key from st.form_submit_button
        register_button = st.form_submit_button("REGISTER", use_container_width=True)
        
        if register_button:
            name_stripped = name.strip()
            email_stripped = email.strip()
            password_stripped = password.strip()
            confirm_password_stripped = confirm_password.strip()

            if not (name_stripped and email_stripped and password_stripped and confirm_password_stripped):
                st.warning("⚠️ Please fill in all fields.")
            elif "@" not in email_stripped or "." not in email_stripped:
                st.error("❌ Please enter a valid email address format.")
            elif password_stripped != confirm_password_stripped:
                st.warning("⚠️ Passwords do not match.")
            elif len(password_stripped) < 6:
                st.warning("⚠️ Password should be at least 6 characters long.")
            else:
                success, msg = sign_up(email_stripped, password_stripped)
                if success:
                    user = get_user_by_email(email_stripped) # Check if user already exists locally
                    local_user_id = None
                    if user:
                        local_user_id = user['id']
                    else:
                        # Register in local DB (using a dummy phone number as it's required by DB schema)
                        # The password_hash is also a dummy as Firebase handles actual auth
                        local_user_id = register_user(name_stripped, email_stripped, "N/A", "firebase_registered_user") 
                        local_user = get_user_by_email(email_stripped) # Fetch again to get the full row
                        local_user_id = local_user['id'] if local_user else None
                    
                    if local_user_id:
                        save_user_profile(
                            local_user_id,
                            {
                                "age": None, "gender": None, "height": None, "weight": None,
                                "activity_level": None, "medical_conditions": None,
                                "food_preferences": None, "allergies": None, "health_goal": None
                            }
                        )

                    st.success("✅ Registration successful! Please login.")
                    st.session_state['page'] = 'Login'
                    st.rerun() # Replaced st.experimental_rerun()
                else:
                    st.error(f"❌ {msg}")
    
    st.markdown('<p class="auth-link-text" style="margin-top: 2rem;">Already have an account? <a href="#" onclick="window.parent.document.querySelector(\'button[key=login_link_from_register]\').click(); return false;">Log In</a></p>', unsafe_allow_html=True)
    
    # Hidden button to trigger page navigation
    st.button("Login", key="login_link_from_register", on_click=lambda: st.session_state.update(page='Login'), help="Hidden", disabled=True)

    st.markdown("</div>", unsafe_allow_html=True)

def show_logout_button():
    col_user, col_logout = st.columns([4, 1])
    with col_user:
        st.markdown(f'<div class="user-info">👤 Logged in as <strong>{st.session_state.get("user_name", "User")}</strong></div>', unsafe_allow_html=True)
    with col_logout:
        # Removed key from st.form_submit_button (this is not a form button, but a regular button)
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.clear()
            st.rerun() # Replaced st.experimental_rerun()

def main_app():
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">NutriAI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Your AI-powered personalized nutrition assistant</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    show_logout_button()

    menu = ["Home", "Diet Plan Generator", "Ask Nutrition Bot", "My Profile", "Stats"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("Welcome to NutriAI!")
        st.write("""
            NutriAI is your personal AI-powered nutrition assistant designed to help you achieve your health and fitness goals.
            Here's what you can do:
            * **Generate Diet Plans:** Get customized diet plans based on your age, weight, height, and goals.
            * **Ask Nutrition Questions:** Have instant answers to your nutrition queries from our AI bot.
            * **Manage Your Profile:** Keep your health details updated for precise recommendations.
            * **Track Your Stats:** Visualize your progress over time.
            
            Start by navigating through the sidebar menu!
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "Diet Plan Generator":
        st.subheader("Create Your Personalized Diet Plan")
        with st.form("diet_plan_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=10, max_value=100, value=25, placeholder="e.g., 30", key="dp_age")
                # FIXED: min_value and max_value now floats
                weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=70.0, step=0.1, placeholder="e.g., 75.5", key="dp_weight")
                height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175, placeholder="e.g., 170", key="dp_height")
            with col2:
                goal = st.selectbox("Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"], key="dp_goal")
                activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"], key="dp_activity")
                gender = st.selectbox("Gender", ["Male", "Female"], key="dp_gender")
            
            # Removed key from st.form_submit_button
            generate_button = st.form_submit_button("Generate Diet Plan", use_container_width=True)

            if generate_button:
                user_data = f"""
                Age: {age}
                Weight: {weight} kg
                Height: {height} cm
                Gender: {gender}
                Goal: {goal}
                Activity Level: {activity_level}
                """
                with st.spinner("Generating your personalized diet plan... This may take a moment."):
                    diet_plan = generate_diet_plan(user_data)
                    st.success("✅ Here is your personalized diet plan:")
                    st.markdown(diet_plan)

    elif choice == "Ask Nutrition Bot":
        st.subheader("Ask the Nutrition Assistant")
        with st.form("ask_bot_form", clear_on_submit=False): # FIXED: Form added
            question = st.text_area("Your Question", placeholder="e.g., What are good sources of protein for vegetarians?", height=100, key="ask_bot_question")
            # Removed key from st.form_submit_button
            ask_button = st.form_submit_button("Ask")

            if ask_button:
                if question.strip():
                    with st.spinner("Thinking..."):
                        answer = ask_diet_bot(question)
                        st.info("--- Nutrition Assistant's Answer ---")
                        st.markdown(answer)
                else:
                    st.warning("Please enter a question.")

    elif choice == "My Profile":
        st.subheader("Your Profile")
        user_email = st.session_state.get('user_email')
        if user_email:
            local_user = get_user_by_email(user_email)
            if local_user:
                local_user_id = local_user['id']
                profile = get_user_profile(local_user_id)
                
                default_age = profile.get('age') if profile and profile.get('age') is not None else 25
                default_weight = profile.get('weight') if profile and profile.get('weight') is not None else 70.0
                default_height = profile.get('height') if profile and profile.get('height') is not None else 175
                default_gender = profile.get('gender') if profile and profile.get('gender') is not None else "Not specified"
                default_goal = profile.get('health_goal') if profile and profile.get('health_goal') is not None else "Maintain Weight"
                default_activity_level = profile.get('activity_level') if profile and profile.get('activity_level') is not None else "Sedentary"
                default_medical_conditions = profile.get('medical_conditions') if profile and profile.get('medical_conditions') is not None else ""
                default_food_preferences = profile.get('food_preferences') if profile and profile.get('food_preferences') is not None else ""
                default_allergies = profile.get('allergies') if profile and profile.get('allergies') is not None else ""

                st.markdown('<div class="feature-card">', unsafe_allow_html=True)
                st.markdown(f"**Name:** {local_user.get('name', 'N/A')}")
                st.markdown(f"**Email:** {local_user.get('email', 'N/A')}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                with st.expander("Update Your Health Profile", expanded=True):
                    with st.form("profile_update_form", clear_on_submit=False): # FIXED: Form key added
                        col_p1, col_p2 = st.columns(2)
                        with col_p1:
                            new_age = st.number_input("Age", min_value=1, max_value=120, value=default_age, key="profile_age_input")
                            new_weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=default_weight, step=0.1, key="profile_weight_input")
                            new_height = st.number_input("Height (cm)", min_value=50, max_value=250, value=default_height, key="profile_height_input")
                            new_gender = st.selectbox("Gender", ["Male", "Female", "Not specified"], index=["Male", "Female", "Not specified"].index(default_gender), key="profile_gender_input")
                        with col_p2:
                            new_activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"], index=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"].index(default_activity_level), key="profile_activity_input")
                            new_goal = st.selectbox("Health Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"], index=["Lose Weight", "Maintain Weight", "Gain Weight"].index(default_goal), key="profile_goal_input")
                            new_medical_conditions = st.text_area("Medical Conditions (e.g., Diabetes, Hypertension)", value=default_medical_conditions, key="profile_med_conditions")
                            new_food_preferences = st.text_area("Food Preferences (e.g., Vegetarian, Vegan, Halal)", value=default_food_preferences, key="profile_food_pref")
                            new_allergies = st.text_area("Allergies (e.g., Peanuts, Dairy)", value=default_allergies, key="profile_allergies")

                        # Removed key from st.form_submit_button
                        save_button = st.form_submit_button("Save Profile", use_container_width=True)

                        if save_button:
                            profile_data = {
                                "age": new_age,
                                "gender": new_gender,
                                "height": new_height,
                                "weight": new_weight,
                                "activity_level": new_activity_level,
                                "medical_conditions": new_medical_conditions,
                                "food_preferences": new_food_preferences,
                                "allergies": new_allergies,
                                "health_goal": new_goal
                            }
                            success_save = save_user_profile(local_user_id, profile_data)
                            if success_save:
                                st.success("✅ Profile updated successfully!")
                                st.rerun() # Replaced st.experimental_rerun()
                            else:
                                st.error("❌ Failed to save profile. Please check your inputs.")
            else:
                st.warning("User profile not found in local database. This might happen if you registered via Firebase but your local profile wasn't fully set up. Please update your profile details below.")
                
                with st.expander("Create Your Health Profile", expanded=True):
                    st.warning("Please fill in your profile details to get started.")
                    
                    with st.form("create_profile_form", clear_on_submit=False): # FIXED: Form key added
                        col_pc1, col_pc2 = st.columns(2)
                        with col_pc1:
                            pc_age = st.number_input("Age", min_value=1, max_value=120, value=25, key="pc_age")
                            pc_weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1, key="pc_weight")
                            pc_height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170, key="pc_height")
                            pc_gender = st.selectbox("Gender", ["Male", "Female", "Not specified"], key="pc_gender")
                        with col_pc2:
                            pc_activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"], key="pc_activity")
                            pc_goal = st.selectbox("Health Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"], key="pc_goal")
                            pc_medical_conditions = st.text_area("Medical Conditions", key="pc_med_conditions")
                            pc_food_preferences = st.text_area("Food Preferences", key="pc_food_pref")
                            pc_allergies = st.text_area("Allergies", key="pc_allergies")

                        # Removed key from st.form_submit_button
                        create_profile_button = st.form_submit_button("Create Profile", use_container_width=True)

                        if create_profile_button:
                            user_from_db = get_user_by_email(user_email)
                            if user_from_db:
                                local_id = user_from_db['id']
                                profile_data = {
                                    "age": pc_age,
                                    "gender": pc_gender,
                                    "height": pc_height,
                                    "weight": pc_weight,
                                    "activity_level": pc_activity_level,
                                    "medical_conditions": pc_medical_conditions,
                                    "food_preferences": pc_food_preferences,
                                    "allergies": pc_allergies,
                                    "health_goal": pc_goal
                                }
                                success_save = save_user_profile(local_id, profile_data)
                                if success_save:
                                    st.success("✅ Profile created and saved successfully!")
                                    st.rerun() # Replaced st.experimental_rerun()
                                else:
                                    st.error("❌ Failed to create profile. Please try again.")
                            else:
                                st.error("❌ Could not find local user record to associate profile with. Please contact support.")

        else:
            st.info("Please log in to manage your profile.")


    elif choice == "Stats":
        st.subheader("Your Nutrition Stats")
        data = {
            "Date": ["2025-05-01", "2025-05-08", "2025-05-15", "2025-05-22", "2025-05-29"],
            "Weight": [70, 69, 68, 67.5, 67],
            "Calories": [2000, 1950, 1900, 1850, 1800]
        }
        df = pd.DataFrame(data)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### Weight Tracking")
        fig = px.line(df, x="Date", y="Weight", title="Weight Over Time", 
                      labels={"Weight": "Weight (kg)", "Date": "Date"},
                      line_shape="spline", markers=True)
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### Calorie Intake")
        fig2 = px.bar(df, x="Date", y="Calories", title="Calories Intake Over Time", color="Calories",
                      labels={"Calories": "Calories (kcal)", "Date": "Date"},
                      color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def main():
    load_custom_css()

    if 'page' not in st.session_state:
        st.session_state['page'] = 'Home_Auth_Landing' # Initial state
    if 'show_forgot_password' not in st.session_state:
        st.session_state['show_forgot_password'] = False
    
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        if st.session_state['page'] == 'Home_Auth_Landing':
            # This hero section will now apply the general background image
            st.markdown('<div class="hero-section">', unsafe_allow_html=True)
            st.markdown('<h1 class="hero-title">Your AI-Powered Nutrition Partner</h1>', unsafe_allow_html=True)
            st.markdown('<p class="hero-subtitle">Achieve your health goals with personalized diet plans, instant nutrition advice, and progress tracking.</p>', unsafe_allow_html=True)
            
            st.markdown('<div class="hero-buttons">', unsafe_allow_html=True)
            col_hero_login, col_hero_register = st.columns(2)
            with col_hero_login:
                # Removed key from st.form_submit_button (this is a regular button, but for consistency)
                if st.button("Log In", use_container_width=True):
                    st.session_state['page'] = 'Login'
                    st.rerun() # Replaced st.experimental_rerun()
            with col_hero_register:
                # Removed key from st.form_submit_button (this is a regular button, but for consistency)
                if st.button("Sign Up", use_container_width=True):
                    st.session_state['page'] = 'Register'
                    st.rerun() # Replaced st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state['page'] == 'Login':
            show_login_page() # Show the regular login page
        elif st.session_state['page'] == 'Register':
            show_register_page()
    else:
        # Remove login-bg/register-bg class when logged in
        st.markdown('<script>document.body.classList.remove("login-bg", "register-bg");</script>', unsafe_allow_html=True)
        main_app()

if __name__ == "__main__":
    from database import create_tables
    create_tables()
    main()