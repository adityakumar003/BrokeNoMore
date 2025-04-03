# BrokeNoMore
# BrokeNoMore

BrokeNoMore is a finance tracking web application built using **Streamlit**. It allows users to manage their expenses, track debts, and even get financial insights via an AI-powered chatbot using the **Google Gemini API**.

## Features 🚀
- **User Authentication** (Register/Login)
- **Expense Management** (Add, View, and Categorize expenses)
- **Debt Tracking** (Borrow/Lend money tracking)
- **Expense Reports** (Visualize spending trends)
- **AI-Powered Chatbot** (Get personalized financial advice)

---

## Installation 🛠️
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/adityakumar003/BrokeNoMore.git
cd BrokeNoMore
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv .venv
source .venv/bin/activate  # On Mac/Linux
# OR
.venv\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up API Key
Replace the placeholder API key in `main.py` with your **Google Gemini API Key**:
```python
genai.configure(api_key="YOUR_GOOGLE_GEMINI_API_KEY")
```

### 5️⃣ Run the Application
```sh
streamlit run main.py
```

---

## Database Structure 📂
This app uses **SQLite** for data storage. The following tables are created:
1. **Users** (`email`, `password`)
2. **Expenses** (`id`, `user`, `category`, `amount`, `date`)
3. **Debts** (`id`, `user`, `friend`, `amount`, `status`, `date`)

---

## How to Use 📝
1. **Register/Login** with an email and password.
2. **Add Expenses** under categories like Food, Transport, Shopping, etc.
3. **View Reports** to analyze spending trends via charts.
4. **Manage Debts** by recording borrowed or lent money.
5. **Use Chatbot** to get AI-based financial advice based on your spending habits.

---

## Technologies Used 🛠️
- **Python** 🐍
- **Streamlit** (Frontend & UI)
- **SQLite** (Database)
- **Google Gemini API** (AI Chatbot)
- **Pandas & Matplotlib** (Data Analysis & Visualization)

---

## Contributing 🤝
Want to contribute? Follow these steps:
1. **Fork** the repository
2. Create a **new branch** (`git checkout -b feature-branch`)
3. **Commit changes** (`git commit -m "Added a new feature"`)
4. **Push** to GitHub (`git push origin feature-branch`)
5. Create a **Pull Request** 🚀

---

## License 📜
This project is licensed under the **MIT License**.

---

## Author 👨‍💻
**Aditya Kumar Singh**,
Ayush Ranjan and
Vishal Kumar

For any queries, feel free to connect! 🚀
The link for the ppt is:-https://www.canva.com/design/DAGjkPdlSVk/rZ_uR8t-3OGSUxXorptH0A/view?utm_content=DAGjkPdlSVk&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h5dc4d9373f

