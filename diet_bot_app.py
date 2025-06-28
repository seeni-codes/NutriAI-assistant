import streamlit as st
from diet_bot import ask_diet_bot, generate_diet_plan
from twilio.rest import Client
from database import register_user, get_user_by_email, verify_password, save_user_profile, get_user_profile

# Twilio configuration (replace with your Twilio credentials)
TWILIO_ACCOUNT_SID = "your_account_sid"
</create_file>
