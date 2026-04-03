import streamlit as st
import json
import os

DB_FILE = "utils/auth_db.json"

# ensure file exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

def auth():
    st.sidebar.title("🔐 Authentication")

    menu = st.sidebar.radio("Select", ["Login", "Register"])

    users = load_users()

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if menu == "Register":
        if st.sidebar.button("Register"):
            if username in users:
                st.sidebar.error("User already exists")
            else:
                users[username] = password
                save_users(users)
                st.sidebar.success("Registered successfully")

    elif menu == "Login":
        if st.sidebar.button("Login"):
            if users.get(username) == password:
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.sidebar.success(f"Welcome {username}")
            else:
                st.sidebar.error("Invalid credentials")

    return st.session_state.get("logged_in", False)