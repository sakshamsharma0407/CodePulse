# CodePulse — Coding Practice and Evaluation Platform

**CodePulse** is a coding practice and evaluation platform designed to help students improve their programming skills through structured coding problems, automated test cases, and performance tracking.

## Features

- **Coding Practice:** Solve programming problems organized by topics and difficulty levels.
- **Automated Evaluation:** Submit C++ solutions and evaluate them against predefined test cases.
- **Instant Results:** View whether a submission is accepted or not accepted.
- **User Authentication:** Login functionality integrated with a C++ backend.
- **Database Integration:** MySQL is used to manage application data.
- **Progress Tracking:** Maintain records of coding attempts and performance.
- **Learning Support:** Designed to help students identify areas where they need more practice.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and interface integration |
| Streamlit | User interface |
| C++ | Backend logic and code evaluation |
| MySQL | Database management |
| Git and GitHub | Version control and collaboration |

## Project Structure


CodePulse/

├── Backend(C++)/

│   ├── judge.cpp

│   ├── login.cpp

│   ├── submission.cpp

│   └── .vscode/

├── Database(MySQL)/

│   ├── database.sql

│   └── database.mwb

├── Docs/

├── Frontend(Python)/

│   ├── app.py

│   └── .vscode/

├── .gitignore

└── README.md


## Getting Started

### Prerequisites

Install the following tools before running the project:

- Python 3
- A C++ compiler such as GCC/G++
- MySQL Server
- Git

### 1. Clone the Repository


git clone https://github.com/sakshamsharma0407/CodePulse.git
cd CodePulse


### 2. Set Up the Python Environment


python -m venv .venv


Activate the environment on Windows:


.venv\Scripts\Activate.ps1


Install the Python packages required by your application. For example:


pip install streamlit mysql-connector-python bcrypt streamlit-ace openai


### 3. Configure MySQL

1. Start your MySQL server.
2. Create or configure the database required by the project.
3. Import the SQL file from Database(MySQL)/database.sql if it contains the required schema.
4. Configure database credentials securely in your application.

### 4. Compile the C++ Backend

Using GCC/G++ on Windows:

powershell
g++ "Backend(C++)/login.cpp" -o "Backend(C++)/login.exe"

g++ "Backend(C++)/submission.cpp" -o "Backend(C++)/submission.exe"

g++ "Backend(C++)/judge.cpp" -o "Backend(C++)/judge.exe"


Check the source files for any additional compiler flags or dependencies required by your setup.

### 5. Run the Application

From the project root, run:


streamlit run "Frontend(Python)/app.py"


Follow the local URL displayed in the terminal to open CodePulse in your browser.

## How It Works

1. The user opens the Streamlit interface.
2. The user selects a coding problem and writes a C++ solution.
3. The backend compiles and evaluates the submission.
4. The submitted solution is checked against predefined test cases.
5. The result is displayed in the interface.
6. Relevant application data can be stored in MySQL for tracking and analysis.

## Future Enhancements

- Expanded coding problem library
- Improved submission history and progress dashboards
- Weak-topic detection and personalized recommendations
- Additional data structures and algorithms practice
- Enhanced evaluation and error reporting

## Repository

**GitHub:** https://github.com/sakshamsharma0407/CodePulse

## Team

CodePulse is developed as part of a team-based academic project.

---

*CodePulse — Think smart. Code better. Keep growing.*
