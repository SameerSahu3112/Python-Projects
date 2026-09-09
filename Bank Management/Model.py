import os
import sys
import random
from datetime import datetime, date, timedelta

# Ensure local modules in Bank Management directory are always resolvable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_db():
    from Connection_Bank import create_connection
    return create_connection()

class Customer:
    """Handles customer registration and initial account generation based on your exact MySQL schema."""
    def __init__(self, customer_name, date_of_birth, email, phone, address, customer_password, initial_deposit=500.0):
        self.result = Customer.register(customer_name, date_of_birth, email, phone, address, customer_password, initial_deposit)

    @staticmethod
    def register(customer_name, date_of_birth, email, phone, address, customer_password, initial_deposit=500.0):
        db = get_db()
        if not db:
            print("[ERROR] Database connection unavailable. Cannot complete registration.")
            return None

        cursor = db.cursor()
        try:
            # 1. Check if phone or email is already registered
            cursor.execute("SELECT customer_id FROM customer WHERE phone = %s OR email = %s", (phone, email))
            if cursor.fetchone():
                print("[ERROR] A customer with this phone number or email is already registered!")
                return None

            # 2. Insert Customer into `customer` table
            query = """
            INSERT INTO customer (customer_name, date_of_birth, email, phone, address, account_status, customer_password)
            VALUES (%s, %s, %s, %s, %s, 'active', %s)
            """
            cursor.execute(query, (customer_name, date_of_birth, email, phone, address, customer_password))
            customer_id = cursor.lastrowid

            # 3. Retrieve default branch if available
            cursor.execute("SELECT branch_id FROM branch LIMIT 1")
            branch_row = cursor.fetchone()
            branch_id = branch_row[0] if branch_row else None

            # 4. Generate 10-digit Account Number: 1001000000 + customer_id
            aacount_number = str(1001000000 + int(customer_id))

            # 5. Insert Account into `accounts` table
            cursor.execute(
                """
                INSERT INTO accounts (customer_id, aacount_number, balance, customer_account_status, branch_id)
                VALUES (%s, %s, %s, 'active', %s)
                """,
                (customer_id, aacount_number, initial_deposit, branch_id)
            )
            account_id = cursor.lastrowid

            # 6. Record initial deposit transaction into `bank_transaction` if > 0
            if initial_deposit > 0:
                cursor.execute(
                    """
                    INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (account_id, "Deposit", initial_deposit, "Account opening initial balance")
                )

            db.commit()
            return customer_id, aacount_number, initial_deposit
        except Exception as e:
            db.rollback()
            print(f"[ERROR] Registration failed: {e}")
            return None
        finally:
            cursor.close()
            db.close()


def get_info():
    print("\n" + "=" * 45)
    print("        CUSTOMER REGISTRATION (SIGN UP)       ")
    print("=" * 45)
    customer_name = input("Enter Your Full Name: ").strip()
    if not customer_name:
        print("[ERROR] Name cannot be empty.")
        return

    date_of_birth = input("Enter Date Of Birth (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        print("[ERROR] Invalid date format! Please use YYYY-MM-DD.")
        return

    email = input("Enter Your Email Address: ").strip()
    phone = input("Enter Your 10-Digit Phone Number: ").strip()

    if len(phone) != 10 or not phone.isdigit():
        print("[ERROR] Phone number must be exactly 10 digits.")
        return

    address = input("Enter Your Address: ").strip()
    customer_password = input("Create Login Password: ").strip()
    confirm_password = input("Confirm Login Password: ").strip()

    if not customer_password:
        print("[ERROR] Password cannot be empty.")
        return
    if customer_password != confirm_password:
        print("[ERROR] Passwords do not match!")
        return

    try:
        deposit_input = input("Enter Initial Deposit Amount (Minimum Rs. 500) [Default 500]: ").strip()
        initial_deposit = float(deposit_input) if deposit_input else 500.0
        if initial_deposit < 0:
            print("[ERROR] Initial deposit cannot be negative.")
            return
    except ValueError:
        print("[ERROR] Invalid amount entered. Defaulting to Rs. 500.")
        initial_deposit = 500.0

    result = Customer.register(customer_name, date_of_birth, email, phone, address, customer_password, initial_deposit)
    if result:
        cust_id, acc_no, initial_bal = result
        print("\n" + "*" * 50)
        print("      REGISTRATION COMPLETED SUCCESSFULLY!        ")
        print("*" * 50)
        print(f" Customer ID    : {cust_id}  <-- Save this for Login!")
        print(f" Account Number : {acc_no}")
        print(f" Initial Balance: Rs. {initial_bal:,.2f}")
        print("*" * 50)

        proceed = input("\nWould you like to log in now? (y/n): ").strip().lower()
        if proceed == 'y':
            login()


def login():
    print("\n" + "=" * 45)
    print("              CUSTOMER LOGIN                 ")
    print("=" * 45)
    try:
        customer_id = int(input("Enter Your Customer ID: ").strip())
    except ValueError:
        print("[ERROR] Customer ID must be a numeric value.")
        return

    password = input("Enter Your Password: ").strip()

    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    query = "SELECT customer_id, customer_name, customer_password, account_status FROM customer WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    customer = cursor.fetchone()
    cursor.close()
    db.close()

    if customer and customer[2] == password:
        if customer[3] != 'active':
            print("[ALERT] Your customer account is not active. Please contact the branch.")
            return
        print(f"\n[SUCCESS] Welcome back, {customer[1]}!")
        bank_customer_menu(customer_id)
    else:
        print("[ERROR] Invalid Customer ID or Password. Please try again.")


def get_or_create_primary_account(customer_id):
    """Fetches customer primary account from `accounts`, or offers to create one if none exists."""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    cursor.execute(
        """
        SELECT a.account_id, a.aacount_number, a.balance, a.customer_account_status, a.branch_id, b.branch_name, b.ifsc_code
        FROM accounts a
        LEFT JOIN branch b ON a.branch_id = b.branch_id
        WHERE a.customer_id = %s LIMIT 1
        """,
        (customer_id,)
    )
    account = cursor.fetchone()

    if not account:
        print("\n[NOTICE] You do not have a bank account created yet.")
        create = input("Would you like to open your Bank Account now? (y/n): ").strip().lower()
        if create == 'y':
            try:
                dep = input("Enter initial deposit (Rs.) [Default 500]: ").strip()
                initial_dep = float(dep) if dep else 500.0
            except ValueError:
                initial_dep = 500.0

            cursor.execute("SELECT branch_id FROM branch LIMIT 1")
            b_row = cursor.fetchone()
            b_id = b_row[0] if b_row else None

            acc_num = str(1001000000 + int(customer_id))
            cursor.execute(
                "INSERT INTO accounts (customer_id, aacount_number, balance, customer_account_status, branch_id) VALUES (%s, %s, %s, 'active', %s)",
                (customer_id, acc_num, initial_dep, b_id)
            )
            acc_id = cursor.lastrowid
            if initial_dep > 0:
                cursor.execute(
                    "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, 'Deposit', %s, 'Initial Deposit')",
                    (acc_id, initial_dep)
                )
            db.commit()
            print(f"[SUCCESS] Bank Account opened successfully! Account Number: {acc_num}")

            cursor.execute(
                """
                SELECT a.account_id, a.aacount_number, a.balance, a.customer_account_status, a.branch_id, b.branch_name, b.ifsc_code
                FROM accounts a
                LEFT JOIN branch b ON a.branch_id = b.branch_id
                WHERE a.account_id = %s
                """,
                (acc_id,)
            )
            account = cursor.fetchone()
        else:
            cursor.close()
            db.close()
            return None

    cursor.close()
    db.close()
    return account


# =========================================================
# Sub-Service: Account Operations
# =========================================================
def account_services(customer_id):
    account = get_or_create_primary_account(customer_id)
    if not account:
        return

    account_id = account[0]
    aacount_number = account[1]

    while True:
        account = get_or_create_primary_account(customer_id)
        if not account:
            break
        current_balance = float(account[2])

        print("\n" + "-" * 42)
        print(f" ACCOUNT SERVICES | A/C: {aacount_number}")
        print("-" * 42)
        print("1. View Account Details & Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Funds (Inter-Account)")
        print("5. View Account Statement (Passbook)")
        print("6. Back to Main Customer Menu")
        print("-" * 42)

        choice = input("Enter Your Choice (1-6): ").strip()

        if choice == "1":
            branch_name = account[5] or "MANIT Main Branch"
            ifsc = account[6] or "MANIT000101"
            print("\n" + "=" * 45)
            print("             ACCOUNT DETAILS                 ")
            print("=" * 45)
            print(f" Account ID     : {account[0]}")
            print(f" Account Number : {account[1]}")
            print(f" Current Balance: Rs. {current_balance:,.2f}")
            print(f" Account Status : {account[3]}")
            print(f" Branch         : {branch_name}")
            print(f" IFSC Code      : {ifsc}")
            print("=" * 45)

        elif choice == "2":
            try:
                amount = float(input("Enter Amount to Deposit (Rs.): "))
            except ValueError:
                print("[ERROR] Invalid numeric amount.")
                continue
            if amount <= 0:
                print("[ERROR] Deposit amount must be positive.")
                continue

            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, 'Deposit', %s, %s)",
                (account_id, amount, "Cash deposit at branch")
            )
            db.commit()
            cursor.close()
            db.close()

            new_balance = current_balance + amount
            print(f"[SUCCESS] Rs. {amount:,.2f} deposited successfully. New Balance: Rs. {new_balance:,.2f}")

        elif choice == "3":
            try:
                amount = float(input("Enter Amount to Withdraw (Rs.): "))
            except ValueError:
                print("[ERROR] Invalid numeric amount.")
                continue
            if amount <= 0:
                print("[ERROR] Withdrawal amount must be positive.")
                continue
            if amount > current_balance:
                print(f"[ERROR] Insufficient funds. Available balance: Rs. {current_balance:,.2f}")
                continue

            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, 'Withdrawal', %s, %s)",
                (account_id, amount, "Cash withdrawal from branch")
            )
            db.commit()
            cursor.close()
            db.close()

            new_balance = current_balance - amount
            print(f"[SUCCESS] Rs. {amount:,.2f} withdrawn successfully. Remaining Balance: Rs. {new_balance:,.2f}")

        elif choice == "4":
            recipient_acc = input("Enter Beneficiary Account Number: ").strip()
            if recipient_acc == aacount_number:
                print("[ERROR] Cannot transfer funds to your own account.")
                continue

            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                "SELECT account_id, balance, customer_account_status FROM accounts WHERE aacount_number = %s",
                (recipient_acc,)
            )
            recipient = cursor.fetchone()
            if not recipient:
                print("[ERROR] Beneficiary account number not found.")
                cursor.close()
                db.close()
                continue
            if recipient[2] != "active":
                print("[ERROR] Beneficiary account is not active.")
                cursor.close()
                db.close()
                continue

            try:
                amount = float(input("Enter Transfer Amount (Rs.): "))
            except ValueError:
                print("[ERROR] Invalid numeric amount.")
                cursor.close()
                db.close()
                continue

            if amount <= 0:
                print("[ERROR] Amount must be greater than zero.")
                cursor.close()
                db.close()
                continue
            if amount > current_balance:
                print(f"[ERROR] Insufficient funds! Available balance: Rs. {current_balance:,.2f}")
                cursor.close()
                db.close()
                continue

            recipient_account_id = recipient[0]
            remarks = input("Enter Remarks (optional): ").strip() or "Fund Transfer"

            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, recipient_account_id))

            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, 'Transfer-Debit', %s, %s)",
                (account_id, amount, f"Transferred to A/C {recipient_acc}: {remarks}")
            )
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, 'Transfer-Credit', %s, %s)",
                (recipient_account_id, amount, f"Received from A/C {aacount_number}: {remarks}")
            )
            db.commit()
            cursor.close()
            db.close()

            new_balance = current_balance - amount
            print(f"[SUCCESS] Transferred Rs. {amount:,.2f} to Account {recipient_acc}!")
            print(f"Updated Balance: Rs. {new_balance:,.2f}")

        elif choice == "5":
            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                "SELECT transaction_id, transaction_type, amount, transaction_date, description_customer FROM bank_transaction WHERE account_id = %s ORDER BY transaction_id DESC",
                (account_id,)
            )
            records = cursor.fetchall()
            cursor.close()
            db.close()

            print("\n" + "=" * 80)
            print("                           ACCOUNT STATEMENT                          ")
            print("=" * 80)
            print(f"{'Txn ID':<8} | {'Date/Time':<19} | {'Type':<16} | {'Amount (Rs.)':<12} | {'Description'}")
            print("-" * 80)
            if not records:
                print("No transactions recorded yet.")
            else:
                for r in records:
                    t_date = r[3].strftime("%Y-%m-%d %H:%M") if hasattr(r[3], 'strftime') else str(r[3])
                    t_type = r[1]
                    t_amt = f"{float(r[2]):,.2f}"
                    desc = r[4] or ""
                    print(f"{r[0]:<8} | {t_date:<19} | {t_type:<16} | {t_amt:<12} | {desc}")
            print("=" * 80)

        elif choice == "6":
            break
        else:
            print("[ERROR] Invalid choice. Please choose 1-6.")


# =========================================================
# Sub-Service: Loan Management (Matches `loan` table)
# =========================================================
def calculate_emi(principal, annual_rate, term_months):
    """Calculates standard monthly EMI."""
    r = (annual_rate / 12) / 100
    if r == 0:
        return principal / term_months
    emi = principal * r * ((1 + r) ** term_months) / (((1 + r) ** term_months) - 1)
    return emi

def loan_services(customer_id):
    account = get_or_create_primary_account(customer_id)
    if not account:
        return
    account_id = account[0]

    while True:
        print("\n" + "-" * 40)
        print("           LOAN MANAGEMENT SERVICES          ")
        print("-" * 40)
        print("1. Apply for a New Loan")
        print("2. View My Loan Applications & Status")
        print("3. Pay Loan Repayment / Installment")
        print("4. Back to Main Customer Menu")
        print("-" * 40)

        choice = input("Enter Your Choice (1-4): ").strip()

        if choice == "1":
            print("\nAvailable Loan Products:")
            print("1. Personal Loan   (Interest Rate: 11.5% p.a.)")
            print("2. Home Loan       (Interest Rate:  8.5% p.a.)")
            print("3. Car/Auto Loan   (Interest Rate:  9.0% p.a.)")
            print("4. Education Loan  (Interest Rate:  7.5% p.a.)")

            type_choice = input("Select Loan Product (1-4): ").strip()
            loan_rates = {
                "1": ("Personal Loan", 11.5),
                "2": ("Home Loan", 8.5),
                "3": ("Car Loan", 9.0),
                "4": ("Education Loan", 7.5)
            }
            if type_choice not in loan_rates:
                print("[ERROR] Invalid loan product selected.")
                continue

            loan_type, interest_rate = loan_rates[type_choice]

            try:
                amount = float(input(f"Enter Desired Loan Amount for {loan_type} (Rs.): "))
                term_months = int(input("Enter Repayment Term (in months, e.g. 12, 24, 36): "))
            except ValueError:
                print("[ERROR] Invalid input. Numbers required.")
                continue

            if amount < 5000 or term_months < 6:
                print("[ERROR] Minimum loan amount is Rs. 5,000 and minimum term is 6 months.")
                continue

            emi = calculate_emi(amount, interest_rate, term_months)
            total_payable = emi * term_months

            print("\n" + "=" * 45)
            print("            LOAN EMI QUOTATION               ")
            print("=" * 45)
            print(f" Loan Type       : {loan_type}")
            print(f" Principal Amount: Rs. {amount:,.2f}")
            print(f" Annual Interest : {interest_rate}%")
            print(f" Term (Months)   : {term_months}")
            print(f" Monthly EMI     : Rs. {emi:,.2f}")
            print(f" Total Repayment : Rs. {total_payable:,.2f}")
            print("=" * 45)

            confirm = input("Confirm and submit this loan application? (y/n): ").strip().lower()
            if confirm == 'y':
                db = get_db()
                if not db:
                    continue
                cursor = db.cursor()
                # Auto-approve loans under 50,000; otherwise Pending for Manager review
                initial_status = "Approved" if amount <= 50000 else "Pending"
                cursor.execute(
                    """
                    INSERT INTO loan (customer_id, loan_type, loan_amount, interest_rate, loan_date, loan_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (customer_id, loan_type, amount, interest_rate, date.today(), initial_status)
                )
                loan_id = cursor.lastrowid

                # If auto-approved, disburse funds directly to account balance!
                if initial_status == "Approved":
                    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
                    cursor.execute(
                        "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                        (account_id, "Loan-Disbursal", amount, f"Disbursement for Loan #{loan_id} ({loan_type})")
                    )
                    print(f"\n[CONGRATULATIONS] Loan #{loan_id} Auto-Approved! Rs. {amount:,.2f} disbursed to your account.")
                else:
                    print(f"\n[INFO] Loan #{loan_id} Application Submitted! Awaiting Bank Manager approval.")

                db.commit()
                cursor.close()
                db.close()

        elif choice == "2":
            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                "SELECT loan_id, loan_type, loan_amount, interest_rate, loan_date, loan_status FROM loan WHERE customer_id = %s",
                (customer_id,)
            )
            loans = cursor.fetchall()
            cursor.close()
            db.close()

            print("\n" + "=" * 80)
            print("                             MY LOAN APPLICATIONS                              ")
            print("=" * 80)
            print(f"{'Loan ID':<8} | {'Type':<18} | {'Amount (Rs.)':<14} | {'Rate':<8} | {'Date':<12} | {'Status'}")
            print("-" * 80)
            if not loans:
                print("No loan records found.")
            else:
                for l in loans:
                    l_date = str(l[4]) if l[4] else "N/A"
                    print(f"{l[0]:<8} | {l[1]:<18} | Rs.{float(l[2]):<10,.2f} | {float(l[3]):<4}%  | {l_date:<12} | {l[5]}")
            print("=" * 80)

        elif choice == "3":
            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                "SELECT loan_id, loan_type, loan_amount, loan_status FROM loan WHERE customer_id = %s AND loan_status = 'Approved'",
                (customer_id,)
            )
            active_loans = cursor.fetchall()

            if not active_loans:
                print("[INFO] You have no active approved loans requiring repayment.")
                cursor.close()
                db.close()
                continue

            print("\nActive Loans:")
            for l in active_loans:
                print(f"Loan ID: {l[0]} | Type: {l[1]} | Loan Amount: Rs. {float(l[2]):,.2f} | Status: {l[3]}")

            try:
                target_loan_id = int(input("Enter Loan ID to repay: "))
                pay_amt = float(input("Enter Repayment Amount (Rs.): "))
            except ValueError:
                print("[ERROR] Invalid numeric input.")
                cursor.close()
                db.close()
                continue

            acc = get_or_create_primary_account(customer_id)
            current_bal = float(acc[2])
            if current_bal < pay_amt:
                print(f"[ERROR] Insufficient account balance (Rs. {current_bal:,.2f}) to make repayment.")
                cursor.close()
                db.close()
                continue

            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (pay_amt, account_id))
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                (account_id, "Loan-Repayment", pay_amt, f"Repayment installment for Loan #{target_loan_id}")
            )
            db.commit()
            cursor.close()
            db.close()

            print(f"\n[SUCCESS] Rs. {pay_amt:,.2f} repaid towards Loan #{target_loan_id} successfully!")

        elif choice == "4":
            break


# =========================================================
# Sub-Service: Fixed Deposit (FD)
# =========================================================
def fixed_deposit_services(customer_id):
    account = get_or_create_primary_account(customer_id)
    if not account:
        return
    account_id = account[0]

    while True:
        print("\n" + "-" * 40)
        print("        FIXED DEPOSIT (FD) SERVICES          ")
        print("-" * 40)
        print("1. Open New Fixed Deposit")
        print("2. View My Fixed Deposits")
        print("3. Premature Liquidation / Close FD")
        print("4. Back to Main Customer Menu")
        print("-" * 40)

        choice = input("Enter Your Choice (1-4): ").strip()

        if choice == "1":
            print("\nFD Tenure & Interest Rates:")
            print("1. 6 Months  ->  5.5% p.a.")
            print("2. 12 Months ->  6.5% p.a.")
            print("3. 36 Months ->  7.2% p.a.")
            print("4. 60 Months ->  7.5% p.a.")

            t_choice = input("Select Tenure (1-4): ").strip()
            fd_rates = {
                "1": (6, 5.5),
                "2": (12, 6.5),
                "3": (36, 7.2),
                "4": (60, 7.5)
            }
            if t_choice not in fd_rates:
                print("[ERROR] Invalid tenure option.")
                continue

            term_months, interest_rate = fd_rates[t_choice]

            try:
                amount = float(input("Enter FD Principal Deposit Amount (Minimum Rs. 1,000): "))
            except ValueError:
                print("[ERROR] Invalid numeric amount.")
                continue

            if amount < 1000:
                print("[ERROR] Minimum deposit for Fixed Deposit is Rs. 1,000.")
                continue

            acc = get_or_create_primary_account(customer_id)
            curr_bal = float(acc[2])
            if curr_bal < amount:
                print(f"[ERROR] Insufficient balance (Rs. {curr_bal:,.2f}) to open FD.")
                continue

            # Quarterly Compounding formula
            t_years = term_months / 12
            maturity_amount = amount * ((1 + (interest_rate / 400)) ** (4 * t_years))

            start_d = date.today()
            maturity_d = start_d + timedelta(days=term_months * 30)

            print("\n" + "=" * 45)
            print("           FIXED DEPOSIT ESTIMATE             ")
            print("=" * 45)
            print(f" Principal Amount : Rs. {amount:,.2f}")
            print(f" Tenure           : {term_months} Months")
            print(f" Interest Rate    : {interest_rate}% p.a.")
            print(f" Maturity Date    : {maturity_d}")
            print(f" Maturity Return  : Rs. {maturity_amount:,.2f}")
            print("=" * 45)

            confirm = input("Confirm creating this Fixed Deposit? (y/n): ").strip().lower()
            if confirm == 'y':
                db = get_db()
                if not db:
                    continue
                cursor = db.cursor()
                cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
                cursor.execute(
                    """
                    INSERT INTO fixed_deposit (customer_id, account_id, amount, term_months, interest_rate, maturity_amount, start_date, maturity_date, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Active')
                    """,
                    (customer_id, account_id, amount, term_months, interest_rate, maturity_amount, start_d, maturity_d)
                )
                fd_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                    (account_id, "FD-Creation", amount, f"Opened FD #{fd_id} for {term_months} months")
                )
                db.commit()
                cursor.close()
                db.close()

                print(f"\n[SUCCESS] Fixed Deposit #{fd_id} created successfully!")

        elif choice == "2":
            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                "SELECT fd_id, amount, term_months, interest_rate, maturity_amount, start_date, maturity_date, status FROM fixed_deposit WHERE customer_id = %s",
                (customer_id,)
            )
            records = cursor.fetchall()
            cursor.close()
            db.close()

            print("\n" + "=" * 85)
            print("                            MY FIXED DEPOSITS                                  ")
            print("=" * 85)
            print(f"{'FD ID':<6} | {'Principal':<12} | {'Rate':<6} | {'Maturity Amt':<14} | {'Maturity Date':<14} | {'Status'}")
            print("-" * 85)
            if not records:
                print("No Fixed Deposit records found.")
            else:
                for r in records:
                    print(f"{r[0]:<6} | Rs.{float(r[1]):<9,.0f} | {float(r[3]):<4}% | Rs.{float(r[4]):<11,.2f} | {str(r[6]):<14} | {r[7]}")
            print("=" * 85)

        elif choice == "3":
            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute("SELECT fd_id, amount, status FROM fixed_deposit WHERE customer_id = %s AND status = 'Active'", (customer_id,))
            active_fds = cursor.fetchall()
            if not active_fds:
                print("[INFO] You have no active Fixed Deposits to close.")
                cursor.close()
                db.close()
                continue

            try:
                target_fd = int(input("Enter FD ID to liquidate / close: "))
            except ValueError:
                print("[ERROR] Invalid FD ID.")
                cursor.close()
                db.close()
                continue

            fd = next((f for f in active_fds if f[0] == target_fd), None)
            if not fd:
                print("[ERROR] FD not found or already closed.")
                cursor.close()
                db.close()
                continue

            refund_amt = float(fd[1])
            cursor.execute("UPDATE fixed_deposit SET status = 'Closed' WHERE fd_id = %s", (target_fd,))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (refund_amt, account_id))
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                (account_id, "FD-Liquidation", refund_amt, f"Closed FD #{target_fd} (Principal credited back)")
            )
            db.commit()
            cursor.close()
            db.close()

            print(f"\n[SUCCESS] FD #{target_fd} closed. Rs. {refund_amt:,.2f} credited back to your account!")

        elif choice == "4":
            break


# =========================================================
# Sub-Service: Recurring Deposit (RD)
# =========================================================
def recurring_deposit_services(customer_id):
    account = get_or_create_primary_account(customer_id)
    if not account:
        return
    account_id = account[0]

    while True:
        print("\n" + "-" * 40)
        print("      RECURRING DEPOSIT (RD) SERVICES        ")
        print("-" * 40)
        print("1. Open New Recurring Deposit")
        print("2. Pay Next Monthly RD Installment")
        print("3. View My Recurring Deposits")
        print("4. Back to Main Customer Menu")
        print("-" * 40)

        choice = input("Enter Your Choice (1-4): ").strip()

        if choice == "1":
            try:
                monthly_amt = float(input("Enter Monthly Installment Amount (Rs.) [Min 500]: "))
                term_months = int(input("Enter Term in Months (e.g. 12, 24, 36) [Min 6]: "))
            except ValueError:
                print("[ERROR] Invalid numeric input.")
                continue

            if monthly_amt < 500 or term_months < 6:
                print("[ERROR] Minimum installment is Rs. 500 and minimum term is 6 months.")
                continue

            acc = get_or_create_primary_account(customer_id)
            curr_bal = float(acc[2])
            if curr_bal < monthly_amt:
                print(f"[ERROR] Insufficient balance for the first monthly installment (Rs. {monthly_amt:,.2f}).")
                continue

            interest_rate = 6.8
            total_invested = monthly_amt * term_months
            approx_interest = monthly_amt * (term_months * (term_months + 1) / (2 * 12)) * (interest_rate / 100)
            est_maturity = total_invested + approx_interest

            print("\n" + "=" * 45)
            print("        RECURRING DEPOSIT PLAN SUMMARY         ")
            print("=" * 45)
            print(f" Monthly Deposit: Rs. {monthly_amt:,.2f}")
            print(f" Tenure         : {term_months} Months")
            print(f" Interest Rate  : {interest_rate}% p.a.")
            print(f" Total Invested : Rs. {total_invested:,.2f}")
            print(f" Est. Maturity  : Rs. {est_maturity:,.2f}")
            print("=" * 45)

            confirm = input("Confirm opening this Recurring Deposit? (y/n): ").strip().lower()
            if confirm == 'y':
                db = get_db()
                if not db:
                    continue
                cursor = db.cursor()
                cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (monthly_amt, account_id))
                cursor.execute(
                    """
                    INSERT INTO recurring_deposit (customer_id, account_id, monthly_amount, term_months, interest_rate, maturity_amount, total_deposited, months_paid, start_date, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 1, %s, 'Active')
                    """,
                    (customer_id, account_id, monthly_amt, term_months, interest_rate, est_maturity, monthly_amt, date.today())
                )
                rd_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                    (account_id, "RD-Installment-1", monthly_amt, f"First installment for RD #{rd_id}")
                )
                db.commit()
                cursor.close()
                db.close()

                print(f"\n[SUCCESS] RD #{rd_id} opened successfully! 1st month installment deducted.")

        elif choice == "2":
            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                "SELECT rd_id, monthly_amount, term_months, months_paid, total_deposited FROM recurring_deposit WHERE customer_id = %s AND status = 'Active'",
                (customer_id,)
            )
            active_rds = cursor.fetchall()

            if not active_rds:
                print("[INFO] You have no active Recurring Deposits.")
                cursor.close()
                db.close()
                continue

            print("\nActive Recurring Deposits:")
            for r in active_rds:
                print(f"RD ID: {r[0]} | Monthly: Rs. {float(r[1]):,.2f} | Months Paid: {r[3]}/{r[2]} | Deposited: Rs. {float(r[4]):,.2f}")

            try:
                target_rd = int(input("Enter RD ID to pay installment: "))
            except ValueError:
                print("[ERROR] Invalid RD ID.")
                cursor.close()
                db.close()
                continue

            rd = next((r for r in active_rds if r[0] == target_rd), None)
            if not rd:
                print("[ERROR] Invalid RD selection.")
                cursor.close()
                db.close()
                continue

            monthly_amt = float(rd[1])
            term_months = rd[2]
            months_paid = rd[3]
            total_dep = float(rd[4])

            if months_paid >= term_months:
                print("[INFO] All installments for this RD have already been paid!")
                cursor.close()
                db.close()
                continue

            acc = get_or_create_primary_account(customer_id)
            curr_bal = float(acc[2])
            if curr_bal < monthly_amt:
                print(f"[ERROR] Insufficient balance (Rs. {curr_bal:,.2f}) to pay installment of Rs. {monthly_amt:,.2f}")
                cursor.close()
                db.close()
                continue

            new_months_paid = months_paid + 1
            new_total_dep = total_dep + monthly_amt
            status = 'Completed' if new_months_paid >= term_months else 'Active'

            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (monthly_amt, account_id))
            cursor.execute(
                "UPDATE recurring_deposit SET months_paid = %s, total_deposited = %s, status = %s WHERE rd_id = %s",
                (new_months_paid, new_total_dep, status, target_rd)
            )
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                (account_id, f"RD-Installment-{new_months_paid}", monthly_amt, f"Installment {new_months_paid}/{term_months} for RD #{target_rd}")
            )
            db.commit()
            cursor.close()
            db.close()

            print(f"\n[SUCCESS] Paid Installment {new_months_paid}/{term_months} for RD #{target_rd}!")
            if status == 'Completed':
                print("[INFO] All installments completed! RD will mature as per schedule.")

        elif choice == "3":
            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                "SELECT rd_id, monthly_amount, term_months, months_paid, total_deposited, maturity_amount, status FROM recurring_deposit WHERE customer_id = %s",
                (customer_id,)
            )
            records = cursor.fetchall()
            cursor.close()
            db.close()

            print("\n" + "=" * 85)
            print("                          MY RECURRING DEPOSITS                                ")
            print("=" * 85)
            print(f"{'RD ID':<6} | {'Monthly':<12} | {'Progress':<12} | {'Total Deposited':<16} | {'Est. Maturity':<14} | {'Status'}")
            print("-" * 85)
            if not records:
                print("No Recurring Deposit records found.")
            else:
                for r in records:
                    prog = f"{r[3]}/{r[2]} Months"
                    print(f"{r[0]:<6} | Rs.{float(r[1]):<9,.0f} | {prog:<12} | Rs.{float(r[4]):<13,.2f} | Rs.{float(r[5]):<11,.2f} | {r[6]}")
            print("=" * 85)

        elif choice == "4":
            break


# =========================================================
# Main Customer Dashboard Menu
# =========================================================
def bank_customer_menu(customer_id):
    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    cursor.execute("SELECT customer_name FROM customer WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if not result:
        print("[ERROR] Customer record not found.")
        return

    customer_name = result[0]

    while True:
        account = get_or_create_primary_account(customer_id)
        balance_str = f"Rs. {float(account[2]):,.2f}" if account else "No Account"

        print("\n" + "=" * 48)
        print(f"   WELCOME TO MANIT BANK, {customer_name.upper()}   ")
        print(f"   Primary A/C Balance: {balance_str}")
        print("=" * 48)
        print("1. Account Services (Deposit, Withdraw, Transfer)")
        print("2. Loan Services (Apply, View, Repay)")
        print("3. Fixed Deposit (Open FD, Returns, Liquidation)")
        print("4. Recurring Deposit (Open RD, Pay Installment)")
        print("5. ATM Machine Simulation")
        print("6. Logout")
        print("=" * 48)

        choice = input("Enter Your Choice (1-6): ").strip()

        if choice == "1":
            account_services(customer_id)
        elif choice == "2":
            loan_services(customer_id)
        elif choice == "3":
            fixed_deposit_services(customer_id)
        elif choice == "4":
            recurring_deposit_services(customer_id)
        elif choice == "5":
            from Atm import atm_menu
            if account:
                atm_menu(default_account_number=account[1])
            else:
                atm_menu()
        elif choice == "6":
            print(f"\n[INFO] Logged out successfully. Have a nice day, {customer_name}!")
            break
        else:
            print("[ERROR] Invalid choice. Please select 1-6.")


def customer_menu():
    """Customer Portal entry point."""
    while True:
        print("\n" + "=" * 45)
        print("           MANIT BANK CUSTOMER PORTAL         ")
        print("=" * 45)
        print("1. Sign Up / Register New Account")
        print("2. Customer Login")
        print("3. Back to Main Menu")
        print("=" * 45)

        choice = input("Enter Your Choice (1-3): ").strip()

        if choice == "1":
            get_info()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("[ERROR] Invalid option. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    customer_menu()
