
# 🧠 NetBot: Chatbot for Internet Café Order System

A natural language-driven chatbot that automates food ordering and game account top-ups for internet cafés, designed for seamless integration in local desktop environments.

![Python](https://img.shields.io/badge/Made%20With-Python-3670A0?style=flat&logo=python&logoColor=white)
![ANTLR4](https://img.shields.io/badge/Powered%20By-ANTLR4-red)
![License](https://img.shields.io/github/license/koitran14/PPL-Project)

---

## 📽 Demo

👉 [Click here to watch the demo video](https://youtu.be/L75SCaAraMw)

The video walks through:
- Greeting the chatbot naturally
- Ordering food and beverages using flexible commands
- Recharging game accounts with customizable inputs
- Checking order and top-up history
- Using both CLI and GUI interfaces

---

## 📌 Introduction

**NetBot** is a smart assistant designed for Internet Cafés to:
- Simplify food and beverage orders
- Enable self-service top-ups for game accounts
- Streamline customer service with an intuitive chatbot interface

Built with **Python**, **ANTLR4**, and **Supabase**, NetBot helps reduce staff workload, improve service speed, and deliver a better customer experience—especially in high-traffic gaming environments.

---

## ✨ Features

- 🗨 **Natural Language Chatbot** for order and top-up interactions
- 🍔 **Menu-Based Ordering** with support for multiple items
- 💳 **Game Account Top-up** with currency and amount recognition
- 📜 **Order and Top-up History Tracking**
- 🎛 **Command-line (CLI) and GUI Interface** using CustomTkinter
- 📦 **Modular Grammar & Processor Design** for easy maintenance
- 🔐 **User Authentication** and account-specific transactions
- 🧩 **Extendable via Supabase (PostgreSQL)** backend

---

## ⚙ Installation

### 1. Clone Repository
```bash
git clone https://github.com/koitran14/PPL-Project.git
cd PPL-Project
````

### 2. Create Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Compile ANTLR Grammar

Ensure ANTLR is installed and generate parser files:

```bash
antlr4 -Dlanguage=Python3 -o src/generated src/grammar/Command.g4
```

### 5. Set Up Database

Use [Supabase](https://supabase.com) and apply the schema in `src/database/migrations/schema.sql`.

### 6. Run the GUI Application

```bash
python src/interfaces/gui.py
```

To use the CLI instead:

```bash
python src/interfaces/cli.py
```

---

## 🚀 Usage

* **Place Orders**:

  ```
  I want 2 pizzas and 1 coffee please
  ```
* **Top-up Game Account**:

  ```
  top up 50 dollars to my account
  ```
* **Check Top-up History**:

  ```
  show my topup history
  ```
* **Review Past Orders**:

  ```
  what did I order?
  ```

GUI users can log in, view the full menu, and interact with the chatbot via a user-friendly interface.

---

## 🛠 Configuration / Customization

* **Grammar Rules**:
  Modify `src/grammar/Command.g4` to update language patterns.
* **Menu Items**:
  Located in `src/database/models/menu.py`.
* **Theme and Layout**:
  Update GUI components in `src/interfaces/gui.py` and `MenuPopup` classes.

---

## 🧱 Architecture Overview

```text
src/
├── core/             # Parser & Business Logic
├── grammar/          # ANTLR grammar (.g4)
├── generated/        # ANTLR-generated Python files
├── interfaces/       # GUI (CustomTkinter) & CLI
├── database/         # Models & Supabase client
└── hooks/            # Session & authentication
```

> 🔄 Grammar → Parser → Processor → Database → Response

---

## 🧠 Prompt Engineering Principles Applied

This project applies advanced prompt design embedded via ANTLR grammar, including:

* **Clear Instructions**: Each command follows deterministic patterns with optional polite tokens (e.g., `please`, `thanks`).
* **Contextual Flexibility**: Rules support free-form user expressions such as `"order 1 coffee"` or `"i want to add 10 dollars"`.
* **Chain-of-Thought Parsing**: Commands are parsed into syntax trees and semantically interpreted by `CommandProcessor`.
* **Default Fallbacks**: Missing account specs or invalid values are handled gracefully with friendly suggestions.
* **Reference Text Integration**: Data is validated and persisted using relational models for user, order, and top-up operations.

Refer to [Appendix 1](./PPL-Final-Report.pdf) of the report for full `Command.g4` grammar implementation.

---

## 🤝 Contributing

1. Fork this repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Feel free to suggest improvements to grammar, features, or UI.

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## 🙌 Credits

* Developed by:

  * Trần Ngọc Đăng Khôi (Team Lead)
  * Phạm Đình Anh Tuấn
  * Nguyễn Hoàng Việt

* Advisor: Ph.D. Lê Thị Ngọc Hạnh

* Supported by: International University – Vietnam National University, HCMC

**Tech Stack**:

* 🐍 Python 3.12
* 🧬 ANTLR4
* 💾 PostgreSQL via Supabase
* 🖼 CustomTkinter GUI
* 🧠 NLP Grammar + Parsing

---

> “NetBot redefines the café experience—one order at a time.”

