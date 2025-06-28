import streamlit as st
from diet_bot import ask_diet_bot, generate_diet_plan
from database import register_user, get_user_by_email, verify_password, save_user_profile

st.set_page_config(page_title="Nutrition AI", page_icon="🥦", layout="wide")

# --- Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

# --- Header UI
st.markdown("<h1 style='text-align: center;'> AI Nutrition Assistant</h1>", unsafe_allow_html=True)

def login_tab():
    st.markdown("### 🔐 Login")
    with st.form("login_form"):
        login_email = st.text_input("Email", key="login_email")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        login_submit = st.form_submit_button("Login")
        if login_submit:
            user = get_user_by_email(login_email)
            if user and verify_password(user['password_hash'], login_pass):
                st.session_state['logged_in'] = True
                st.session_state['user_email'] = user['email']
                st.session_state['user_name'] = user['name']
                st.session_state['user_id'] = user['id']
                st.success(f"Welcome back, {user['name']}!")
            else:
                st.error("Invalid email or password")

def register_tab():
    st.markdown("### 📝 Register")
    with st.form("register_form"):
        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        phone = st.text_input("Phone", key="reg_phone")
        password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
        register_submit = st.form_submit_button("Register")
        if register_submit:
            if password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not name or not email or not phone or not password:
                st.error("❌ All fields are required")
            else:
                success = register_user(name, email, phone, password)
                if success:
                    st.success("✅ Registration successful! Please login.")
                else:
                    st.error("⚠️ User with this email already exists.")

def logout_button():
    if st.button("Logout 🚪", key="logout_button"):
        st.session_state['logged_in'] = False
        st.session_state['user_email'] = None
        st.session_state['user_name'] = None
        st.session_state['user_id'] = None
        st.success("You have been logged out.")

def profile_tab():
    st.write(f"👋 Logged in as: **{st.session_state['user_name']}** ({st.session_state['user_email']})")
    logout_button()
    with st.expander("👤 User Profile Setup", expanded=True):
        with st.form("user_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=1, max_value=120, step=1)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                height = st.number_input("Height (cm)", min_value=30, max_value=250, step=1)
                weight = st.number_input("Weight (kg)", min_value=1, max_value=300, step=1)
            with col2:
                activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"])
                medical_conditions = st.text_area("Medical Conditions (e.g., diabetes, hypertension)", height=68)
                food_preferences = st.text_area("Food Preferences (e.g., vegetarian, vegan, keto)", height=68)
                allergies = st.text_area("Allergies (e.g., nuts, gluten)", height=68)
                health_goal = st.selectbox("Health Goal", ["Weight loss", "Muscle gain", "Maintain health"])
            submitted = st.form_submit_button("Save Profile 💾")
            if submitted:
                profile = {
                    "age": age,
                    "gender": gender,
                    "height": height,
                    "weight": weight,
                    "activity_level": activity_level,
                    "medical_conditions": medical_conditions,
                    "food_preferences": food_preferences,
                    "allergies": allergies,
                    "health_goal": health_goal
                }
                save_user_profile(st.session_state['user_id'], profile)
                st.success("User profile saved successfully!")
        if st.button("🍱 Generate Meal Plan"):
            with st.spinner("Generating your personalized diet plan..."):
                diet_plan = generate_diet_plan({
                    "age": age,
                    "gender": gender,
                    "height": height,
                    "weight": weight,
                    "activity_level": activity_level,
                    "medical_conditions": medical_conditions,
                    "food_preferences": food_preferences,
                    "allergies": allergies,
                    "health_goal": health_goal
                })
                st.subheader("📅 Your Personalized Weekly Diet Plan")
                st.write(diet_plan)

def ask_bot_tab():
    st.write("Ask me anything related to food, nutrition, weight loss, gym diets or healthy eating!")
    user_input = st.text_area("🧠 What would you like to ask?", height=150)
    if st.button("🧪 Get Response"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                reply = ask_diet_bot(user_input)
                st.success("✅ AI Response:")
                st.write(reply)
        else:
            st.warning("Please enter a question or message.")

if not st.session_state['logged_in']:
    tabs = st.tabs(["Login 🔐", "sign up 📝", "AI 🤖"])
    with tabs[0]:
        login_tab()
    with tabs[1]:
        register_tab()
    with tabs[2]:
        ask_bot_tab()
else:
    tabs = st.tabs(["Profile 👤", "AI planner🤖"])
    with tabs[0]:
        profile_tab()
    with tabs[1]:
        ask_bot_tab()
