import streamlit as st
import json
import os

DB_FILE = "utils/auth_db.json"

# -------------------------
# LOAD USERS
# -------------------------
def load_users():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

# -------------------------
# SAVE USERS
# -------------------------
def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# -------------------------
# AUTH FUNCTION (IMPORTANT)
# -------------------------
def auth():
    users = load_users()

    st.sidebar.title("🔐 Authentication")
    option = st.sidebar.radio("Select", ["Login", "Register"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # LOGIN
    if option == "Login":
        if st.sidebar.button("Login"):
            if username in users and users[username] == password:
                st.sidebar.success(f"Welcome {username}")
                return True
            else:
                st.sidebar.error("Invalid credentials")
                return False

    # REGISTER
    if option == "Register":
        if st.sidebar.button("Register"):
            if username in users:
                st.sidebar.warning("User already exists")
            else:
                users[username] = password
                save_users(users)
                st.sidebar.success("User registered! Now login.")

    return False