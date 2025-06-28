# Firebase authentication fallback using REST API (no pyrebase needed)
import requests

FIREBASE_API_KEY = ""
FIREBASE_AUTH_URL = ""


def sign_up(email: str, password: str):
    url = f"{FIREBASE_AUTH_URL}/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return True, "Sign-up successful!"
    except requests.exceptions.RequestException as e:
        # Improved error parsing for sign_up
        try:
            error_data = res.json()
            error_message = error_data.get("error", {}).get("message", str(e))
            return False, error_message
        except ValueError:
            return False, f"Server error: {res.text}"


def sign_in(email: str, password: str):
    url = f"{FIREBASE_AUTH_URL}/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status() # This will raise an HTTPError for bad responses (4xx or 5xx)
        return True, res.json()
    except requests.exceptions.HTTPError as e:
        # Catch specific HTTP errors from requests and parse Firebase error JSON
        try:
            error_data = res.json()
            error_message = error_data.get("error", {}).get("message", str(e))
            return False, error_message
        except ValueError: # If response is not valid JSON
            return False, f"Server error: {res.text}"
    except requests.exceptions.RequestException as e:
        # Catch other request-related errors (network issues, etc.)
        return False, f"Network or connection error: {str(e)}"


def get_user(id_token):
    url = f"{FIREBASE_AUTH_URL}/accounts:lookup?key={FIREBASE_API_KEY}"
    payload = {"idToken": id_token}
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException:
        return None


def get_user_info(id_token):
    return get_user(id_token)


def verify_id_token(id_token):
    info = get_user(id_token)
    return bool(info and "users" in info)


def send_password_reset_email(email):
    url = f"{FIREBASE_AUTH_URL}/accounts:sendOobCode?key={FIREBASE_API_KEY}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return True, "Password reset email sent successfully."
    except requests.exceptions.RequestException as e:
        # Improved error parsing for password reset
        try:
            error_data = res.json()
            error_message = error_data.get("error", {}).get("message", str(e))
            return False, error_message
        except ValueError:
            return False, f"Server error: {res.text}"
