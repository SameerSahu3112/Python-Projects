# 🏦 Bank Management System

A comprehensive, console-based **Bank Management System** built using **Python 3 and MySQL**.
This project models real-world core banking and ATM operations: customer registration, accounts, inter-account fund transfers, transaction auditing, loan management with EMI calculations, Fixed Deposits (FD), Recurring Deposits (RD), and administrative oversight.

---

## 🚀 Features

### 👤 Customer Module (`Model.py`)
* 📝 **Customer Registration**: New user onboarding with 10-digit phone verification, DOB, email, and password confirmation.
* 🆔 **Automated Account Creation**: Automatically creates your bank account with unique `aacount_number` and links to the local branch.
* 🔐 **Authentication**: Secure Customer ID and password-based login.
* 💰 **Account Operations**:
  * Check live balance, account status, and IFSC branch details
  * Cash deposits and withdrawals
  * Inter-account fund transfers with beneficiary verification
  * Detailed passbook statement (`bank_transaction` history)
* 💳 **Loan Management (`loan`)**:
  * Apply for Personal, Home, Car, or Education loans
  * Dynamic EMI calculations
  * Auto-disbursement for eligible loans into account balance
  * Track loan repayment progress
* 📈 **Fixed & Recurring Deposits**:
  * Open FD with compound quarterly returns (6 to 60 months)
  * Open RD with monthly installment tracking

---

### 🏧 ATM Simulation Module (`Atm.py`)
* 🔢 **Account Number & PIN Check**: Account lookup and password/PIN verification with **3-attempt security lockout**.
* 💵 **Balance Inquiry**: Live account balance check.
* 💸 **Cash Withdrawal**: Currency denomination validation (Rs. 100 multiples) and instant balance update.
* 📥 **Cash Deposit**: Deposit cash directly into the linked account.
* 🔁 **ATM Fund Transfer**: Instant account-to-account transfer.
* 📜 **Mini Statement**: Displays the last 5 transactions with timestamps and types.
* 🔑 **PIN Management**: Reset password/PIN directly from the ATM.

---

### 👨‍💼 Bank Manager / Admin Module (`Admin.py`)
* 🔐 **Admin Authentication**: 4-digit PIN (`1234` by default) with 3-attempt lockout.
* 👥 **Customer Directory**: View all registered customers from `customer`.
* 📊 **Bank Reserves**: View all customer accounts and calculate total bank deposits in `accounts`.
* 🔎 **Customer Search**: Search records across Customer ID, Name, Phone Number, or Account Number.
* 📑 **Loan Approvals**: Review pending customer loan requests with one-click **Approve** (with automated fund disbursement) or **Reject**.
* 📜 **Transaction Audit**: Inspect recent bank transaction logs.
* 🛡️ **Account Controls**: Review and unblock blocked customer accounts.
* 🏢 **Branch Directory**: View all branches, cities, and IFSC codes from `branch`.

---

## 🗄️ Database Design

The system runs on your MySQL `bank` database schema:

### 1. `customer`
| Column | Type | Description |
|---|---|---|
| `customer_id` | BIGINT (PK, AUTO_INCREMENT) | Unique Customer ID |
| `customer_name` | VARCHAR(100) | Full Name |
| `date_of_birth` | DATE | Date of Birth |
| `email` | VARCHAR(25) (UNIQUE) | Email Address |
| `phone` | VARCHAR(20) (UNIQUE) | Contact Number |
| `address` | TEXT | Address |
| `account_status` | VARCHAR(20) | Status (`active`/`inactive`) |
| `customer_password` | VARCHAR(100) | Login Password |

### 2. `branch`
| Column | Type | Description |
|---|---|---|
| `branch_id` | INT (PK, AUTO_INCREMENT) | Unique Branch ID |
| `branch_name` | VARCHAR(100) | Branch Name |
| `branch_address` | VARCHAR(255) | Branch Location |
| `city` | VARCHAR(50) | City |
| `phone` | VARCHAR(15) | Contact Number |
| `ifsc_code` | VARCHAR(11) (UNIQUE) | Branch IFSC Code |

### 3. `accounts`
| Column | Type | Description |
|---|---|---|
| `account_id` | BIGINT (PK, AUTO_INCREMENT) | Internal Account ID |
| `customer_id` | BIGINT (FK -> customer) | Linked Customer |
| `aacount_number` | VARCHAR(20) (UNIQUE) | 10-digit Account Number |
| `balance` | DECIMAL(19,4) | Current Account Balance |
| `customer_account_status` | VARCHAR(20) | Status (`active`/`blocked`) |
| `branch_id` | INT (FK -> branch) | Home Branch |

### 4. `bank_transaction`
| Column | Type | Description |
|---|---|---|
| `transaction_id` | INT (PK, AUTO_INCREMENT) | Unique Transaction ID |
| `account_id` | BIGINT (FK -> accounts) | Associated Account |
| `transaction_type` | VARCHAR(20) | Deposit / Withdrawal / Transfer / Loan |
| `amount` | DECIMAL(12,2) | Transaction Amount |
| `transaction_date` | DATETIME | Timestamp |
| `description_customer` | VARCHAR(255) | Remarks / Narrative |

### 5. `loan`
| Column | Type | Description |
|---|---|---|
| `loan_id` | INT (PK, AUTO_INCREMENT) | Unique Loan ID |
| `customer_id` | BIGINT (FK -> customer) | Applicant Customer |
| `loan_type` | VARCHAR(50) | Home, Personal, Car, Education |
| `loan_amount` | DECIMAL(12,2) | Loan Principal Amount |
| `interest_rate` | DECIMAL(5,2) | Interest Rate % |
| `loan_date` | DATE | Application Date |
| `loan_status` | VARCHAR(20) | Pending / Approved / Rejected |

---

## ▶️ Running the Project

Run the application launcher:
```bash
python3 "Bank Management/Main_Menu.py"
```

### Credentials & Keys:
* **Default Admin PIN**: `1234`
* **Customer Login**: Enter your `customer_id` and `customer_password` (e.g. ID `2` with password `12345`).

---

## 👨‍💻 Author

**Sameer Sahu**  
A Python 3 + MySQL core banking project designed for academic learning and real-world database system implementation.
