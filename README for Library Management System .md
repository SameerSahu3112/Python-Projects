# 📚 Library Management System

A console-based **Library Management System** built using **Python and MySQL**.
This project helps manage books, students, borrowing history, and administrative operations through a simple command-line interface.

The project focuses on implementing real-world concepts like database connectivity, CRUD operations, authentication, and relational database management.

---

## 🚀 Features

### 👨‍💼 Admin Module

* 🔐 Admin PIN authentication
* ➕ Add new books
* 🆔 Automatically generate Book ID
* 📖 View/search books
* ✏️ Update book details
* ❌ Delete books
* 📊 Check book availability status
* 📜 View book issue history
* 👥 View registered students
* 🗑️ Delete student records
* 📚 View student borrowing history
* 🔎 Check active students and issued books

---

### 👨‍🎓 Student Module

* 📝 Student registration
* 🔐 Student login authentication
* 📚 Search available books
* 📖 Issue books
* 🔄 Return books
* 📜 View borrowing history
* 👤 Manage student account details

---

## 🛠️ Technologies Used

* **Programming Language:** Python 3
* **Database:** MySQL
* **Connector:** mysql-connector-python
* **IDE:** Visual Studio Code

---

## 📂 Project Structure

```
Library Management System
│
├── Main.py
├── Admin.py
├── Student.py
├── Connection.py
│
└── Database
    ├── students
    ├── books
    └── issued_book
```

---

## 🗄️ Database Design

### Books Table

Stores information about available books.

| Column      | Description           |
| ----------- | --------------------- |
| book_id     | Unique ID of the book |
| book_name   | Name of the book      |
| author_name | Author of the book    |
| series_name | Book category/series  |
| status      | Available/Issued      |

---

### Students Table

Stores student information.

| Column     | Description       |
| ---------- | ----------------- |
| student_id | Unique student ID |
| name       | Student name      |
| phone      | Contact number    |
| DOB        | Date of birth     |
| password   | Login password    |

---

### Issued Book Table

Stores borrowing records.

| Column     | Description            |
| ---------- | ---------------------- |
| issue_id   | Unique issue record ID |
| book_id    | Issued book ID         |
| student_id | Student who borrowed   |
| status     | Issue/Return status    |

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-link>
```

### 2. Install required package

```bash
pip install mysql-connector-python
```

### 3. Setup MySQL Database

Create a database:

```sql
CREATE DATABASE library_db;
```

Create required tables:

* books
* students
* issued_book

Update your MySQL username and password inside:

```
Connection.py
```

---

## ▶️ Running the Project

Run:

```bash
python Main.py
```

The application will start with the main menu:

```
#### Welcome To Library ####

1. Book Management
2. Student Management
3. Exit
```

---

## 🧠 Concepts Implemented

* Python Functions
* Loops and Conditional Statements
* Exception Handling
* Modular Programming
* MySQL CRUD Operations
* SQL Queries
* Database Relationships
* Authentication System
* Data Validation

---

## 🔮 Future Improvements

* GUI using Tkinter/PyQt
* Password encryption
* OTP based password recovery
* Email notifications
* Fine calculation system
* Due date reminders
* Web-based version using Flask/Django

---

## 👨‍💻 Author

**Sameer Sahu**

A Python + MySQL based project developed as a learning project to understand software development and database management.
