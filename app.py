import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai  # Google Gemini API
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini API (Replace with your actual API key)
genai.configure(os.getenv("API_KEY"))

# Initialize SQLite Database
conn = sqlite3.connect("expenses.db", check_same_thread=False)
c = conn.cursor()

# Create Tables
c.execute('''CREATE TABLE IF NOT EXISTS users (
              email TEXT PRIMARY KEY, 
              password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS expenses (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              user TEXT, 
              category TEXT, 
              amount REAL, 
              date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS debts (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              user TEXT, 
              friend TEXT, 
              amount REAL, 
              status TEXT,  -- "borrowed" or "lent"
              date TEXT)''')
conn.commit()


# User Authentication Functions
def register_user(email, password):
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    if c.fetchone():
        st.error("User already exists! Try logging in.")
    else:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        st.success("User registered successfully! Please login.")


def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    if c.fetchone():
        st.session_state["user"] = email
        st.success("Logged in successfully!")
    else:
        st.error("Invalid login credentials.")


# Expense Functions
def add_expense(user, category, amount, date):
    c.execute("INSERT INTO expenses (user, category, amount, date) VALUES (?, ?, ?, ?)", (user, category, amount, date))
    conn.commit()
    st.success("Expense added successfully!")


def fetch_expense_summary(user):
    c.execute("SELECT category, SUM(amount) FROM expenses WHERE user=? GROUP BY category", (user,))
    expenses = c.fetchall()
    return {category: amount for category, amount in expenses}


def fetch_expenses(user):
    c.execute("SELECT category, amount, date FROM expenses WHERE user=?", (user,))
    return c.fetchall()


def generate_report(expenses):
    df = pd.DataFrame(expenses, columns=["Category", "Amount", "Date"])
    st.write("### Expense Report")
    st.write(df)

    fig, ax = plt.subplots()
    df.groupby("Category")["Amount"].sum().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    fig, ax = plt.subplots()
    df.groupby("Date")["Amount"].sum().plot(kind="line", ax=ax, marker='o')
    ax.set_title("Expense Trend Over Time")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    df.groupby("Category")["Amount"].sum().plot(kind="pie", autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    ax.set_title("Expense Distribution")
    st.pyplot(fig)



# Debt Functions
def add_debt(user, friend, amount, status, date):
    c.execute("INSERT INTO debts (user, friend, amount, status, date) VALUES (?, ?, ?, ?, ?)",
              (user, friend, amount, status, date))
    conn.commit()
    st.success(f"Transaction added: {status.capitalize()} ₹{amount} to {friend} on {date}")


def fetch_debts(user):
    c.execute("SELECT friend, amount, status, date FROM debts WHERE user=?", (user,))
    return c.fetchall()


def fetch_debt_summary(user):
    c.execute("SELECT status, SUM(amount) FROM debts WHERE user=? GROUP BY status", (user,))
    debts = c.fetchall()
    return {status: amount for status, amount in debts}


# Chatbot Function with Personalized Data
def chatbot_response(user, prompt):
    try:
        expenses = fetch_expense_summary(user)
        expense_context = "\n".join([f"{cat}: ₹{amt}" for cat, amt in expenses.items()])


        full_prompt = (
            f"User's expense summary:\n{expense_context}\n\n"
            "Now answer the following finance-related query based on the user's spending habits:\n"
            f"{prompt}"
            "\n\nReply only if the question is related to finance and expenses. Otherwise, say: 'I am here to help you save money! Ask queries related to that.'"
        )

        model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# Streamlit UI
st.title("BrokeNoMore")
menu = ["Login", "Register", "Add Expense📝💰", "View Report📆📊", "Manage Debts💰🤝", "Help Broo🥲"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        register_user(email, password)

elif choice == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login_user(email, password)

elif "user" in st.session_state:
    user = st.session_state["user"]
    st.write(f"Welcome, {user}!")

    if choice == "Add Expense📝💰":
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Others"])
        amount = st.number_input("Amount", min_value=0.0)
        date = st.date_input("Date")
        if st.button("Add Expense"):
            add_expense(user, category, amount, str(date))

    elif choice == "View Report📆📊":
        expenses = fetch_expenses(user)
        if expenses:
            generate_report(expenses)
        else:
            st.warning("No expenses found.")

    elif choice == "Manage Debts💰🤝":
        st.write("### Track Borrowed/Lent Money")
        friend = st.text_input("Friend's Name")
        amount = st.number_input("Amount", min_value=0.0)
        status = st.radio("Transaction Type", ["Borrowed", "Lent"])
        date = st.date_input("Date")

        if st.button("Add Transaction"):
            add_debt(user, friend, amount, status.lower(), str(date))

        debts = fetch_debts(user)
        if debts:
            df = pd.DataFrame(debts, columns=["Friend", "Amount", "Status", "Date"])
            st.write(df)

            summary = fetch_debt_summary(user)
            st.write(f"*Total Borrowed:* ₹{summary.get('borrowed', 0)}")
            st.write(f"*Total Lent:* ₹{summary.get('lent', 0)}")
        else:
            st.warning("No records found.")

    elif choice == "Help Broo🥲":
        user_input = st.text_area("Ask your financial assistant:",height=150)
        if st.button("Get Response"):
            response = chatbot_response(user, user_input)
            st.write(response)
else:
    st.warning("Please login first.")
