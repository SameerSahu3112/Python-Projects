import os
import sys

# Ensure local modules in Bank Management directory are always resolvable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_db():
    from Connection_Bank import create_connection
    return create_connection()

def pin_check(pin="1234", attempt=3):
    """Admin PIN authentication with 3 attempts limit."""
    print("\n" + "=" * 45)
    print("          BANK MANAGER / ADMIN LOGIN         ")
    print("=" * 45)
    while attempt > 0:
        user_pin = input(f"Enter 4-Digit Admin PIN ({attempt} attempt(s) left): ").strip()
        if user_pin == pin:
            print("[SUCCESS] Admin Access Granted!\n")
            admin_menu()
            break
        else:
            attempt -= 1
            print(f"[ERROR] Incorrect PIN. You have {attempt} attempt(s) left.")
            if attempt == 0:
                print("[ALERT] Security Lockout: Maximum attempts exceeded. Returning to main menu.")
                break

def view_all_customers():
    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    cursor.execute(
        "SELECT customer_id, customer_name, phone, email, date_of_birth, address, account_status FROM customer ORDER BY customer_id ASC"
    )
    customers = cursor.fetchall()
    cursor.close()
    db.close()

    print("\n" + "=" * 95)
    print("                                REGISTERED CUSTOMERS                                   ")
    print("=" * 95)
    print(f"{'ID':<4} | {'Name':<22} | {'Phone':<12} | {'Email':<25} | {'DOB':<10} | {'Status'}")
    print("-" * 95)
    if not customers:
        print("No registered customers found.")
    else:
        for c in customers:
            print(f"{c[0]:<4} | {c[1]:<22} | {c[2] or 'N/A':<12} | {c[3] or 'N/A':<25} | {str(c[4]):<10} | {c[6]}")
    print("=" * 95)

def view_all_accounts():
    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    query = """
    SELECT a.account_id, a.aacount_number, c.customer_name, a.balance, a.customer_account_status, b.branch_name
    FROM accounts a
    JOIN customer c ON a.customer_id = c.customer_id
    LEFT JOIN branch b ON a.branch_id = b.branch_id
    ORDER BY a.account_id ASC
    """
    cursor.execute(query)
    accounts = cursor.fetchall()

    cursor.execute("SELECT SUM(balance), COUNT(account_id) FROM accounts")
    total_row = cursor.fetchone()
    total_balance = float(total_row[0]) if total_row and total_row[0] is not None else 0.0
    total_accounts = total_row[1] if total_row else 0

    cursor.close()
    db.close()

    print("\n" + "=" * 90)
    print("                             ALL BANK ACCOUNTS                                 ")
    print("=" * 90)
    print(f"{'A/C ID':<8} | {'Account Number':<16} | {'Customer Name':<22} | {'Balance (Rs.)':<14} | {'Status'}")
    print("-" * 90)
    if not accounts:
        print("No accounts created yet.")
    else:
        for acc in accounts:
            print(f"{acc[0]:<8} | {acc[1]:<16} | {acc[2]:<22} | Rs.{float(acc[3]):<11,.2f} | {acc[4]}")
    print("-" * 90)
    print(f"Total Accounts: {total_accounts} | Total Bank Reserves: Rs. {total_balance:,.2f}")
    print("=" * 90)

def search_customer():
    search_term = input("\nEnter Customer ID, Name, Phone, or Account Number to search: ").strip()
    if not search_term:
        print("[ERROR] Search term cannot be empty.")
        return

    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    query = """
    SELECT c.customer_id, c.customer_name, c.phone, c.email, a.aacount_number, a.balance, a.customer_account_status
    FROM customer c
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    WHERE c.customer_id = %s OR c.customer_name LIKE %s OR c.phone = %s OR a.aacount_number = %s
    """
    cursor.execute(query, (search_term, f"%{search_term}%", search_term, search_term))
    results = cursor.fetchall()
    cursor.close()
    db.close()

    print("\n" + "=" * 95)
    print("                                SEARCH RESULTS                                        ")
    print("=" * 95)
    print(f"{'Cust ID':<8} | {'Name':<22} | {'Phone':<12} | {'Account No':<16} | {'Balance':<12} | {'Status'}")
    print("-" * 95)
    if not results:
        print("No matching customer records found.")
    else:
        for r in results:
            acc_str = str(r[4]) if r[4] else "No Account"
            bal_str = f"Rs.{float(r[5]):,.2f}" if r[5] is not None else "N/A"
            status_str = r[6] or "N/A"
            print(f"{r[0]:<8} | {r[1]:<22} | {r[2] or 'N/A':<12} | {acc_str:<16} | {bal_str:<12} | {status_str}")
    print("=" * 95)

def manage_loans():
    while True:
        db = get_db()
        if not db:
            return
        cursor = db.cursor()
        query = """
        SELECT l.loan_id, c.customer_name, l.loan_type, l.loan_amount, l.interest_rate, l.loan_date, l.loan_status, l.customer_id
        FROM loan l
        JOIN customer c ON l.customer_id = c.customer_id
        WHERE l.loan_status = 'Pending'
        ORDER BY l.loan_id ASC
        """
        cursor.execute(query)
        pending_loans = cursor.fetchall()
        cursor.close()
        db.close()

        print("\n" + "=" * 90)
        print("                           PENDING LOAN APPLICATIONS                                  ")
        print("=" * 90)
        print(f"{'Loan ID':<8} | {'Applicant':<20} | {'Type':<16} | {'Amount (Rs.)':<14} | {'Rate':<8} | {'Status'}")
        print("-" * 90)
        if not pending_loans:
            print("No pending loan applications awaiting review.")
        else:
            for l in pending_loans:
                print(f"{l[0]:<8} | {l[1]:<20} | {l[2]:<16} | Rs.{float(l[3]):<11,.2f} | {float(l[4]):<4}%  | {l[6]}")
        print("=" * 90)

        print("\nLoan Actions:")
        print("1. Approve Loan Application")
        print("2. Reject Loan Application")
        print("3. Back to Admin Menu")

        act = input("Enter Choice (1-3): ").strip()
        if act == "1":
            try:
                target_id = int(input("Enter Loan ID to APPROVE: "))
            except ValueError:
                print("[ERROR] Invalid Loan ID.")
                continue

            target_loan = next((l for l in pending_loans if l[0] == target_id), None)
            if not target_loan:
                print("[ERROR] Loan ID not found in pending list.")
                continue

            loan_id, applicant, loan_type, amount, rate, l_date, _, customer_id = target_loan

            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            # Update loan status to 'Approved'
            cursor.execute("UPDATE loan SET loan_status = 'Approved' WHERE loan_id = %s", (loan_id,))

            # Find customer's account to disburse funds
            cursor.execute("SELECT account_id FROM accounts WHERE customer_id = %s LIMIT 1", (customer_id,))
            acc_row = cursor.fetchone()
            if acc_row:
                acc_id = acc_row[0]
                cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, acc_id))
                cursor.execute(
                    "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                    (acc_id, "Loan-Disbursal", amount, f"Disbursement for Approved Loan #{loan_id} ({loan_type})")
                )
                print(f"\n[SUCCESS] Loan #{loan_id} APPROVED! Rs. {float(amount):,.2f} disbursed to customer account.")
            else:
                print(f"\n[SUCCESS] Loan #{loan_id} APPROVED! (Customer has no account yet; funds will be credited on account opening).")

            db.commit()
            cursor.close()
            db.close()

        elif act == "2":
            try:
                target_id = int(input("Enter Loan ID to REJECT: "))
            except ValueError:
                print("[ERROR] Invalid Loan ID.")
                continue

            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute("UPDATE loan SET loan_status = 'Rejected' WHERE loan_id = %s AND loan_status = 'Pending'", (target_id,))
            db.commit()
            if cursor.rowcount > 0:
                print(f"[SUCCESS] Loan #{target_id} has been REJECTED.")
            else:
                print("[ERROR] Loan ID not found in pending list.")
            cursor.close()
            db.close()

        elif act == "3":
            break

def view_all_transactions():
    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    query = """
    SELECT t.transaction_id, a.aacount_number, t.transaction_type, t.amount, t.transaction_date, t.description_customer
    FROM bank_transaction t
    JOIN accounts a ON t.account_id = a.account_id
    ORDER BY t.transaction_id DESC LIMIT 25
    """
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    db.close()

    print("\n" + "=" * 95)
    print("                             RECENT BANK TRANSACTIONS                                  ")
    print("=" * 95)
    print(f"{'Txn ID':<7} | {'Account No':<16} | {'Type':<18} | {'Amount (Rs.)':<12} | {'Date/Time':<18} | {'Description'}")
    print("-" * 95)
    if not records:
        print("No transactions recorded yet.")
    else:
        for r in records:
            t_date = r[4].strftime("%Y-%m-%d %H:%M") if hasattr(r[4], 'strftime') else str(r[4])
            print(f"{r[0]:<7} | {r[1]:<16} | {r[2]:<18} | {float(r[3]):<12,.2f} | {t_date:<18} | {r[5] or ''}")
    print("=" * 95)

def manage_account_status():
    """Unblock or activate blocked accounts."""
    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT a.account_id, a.aacount_number, c.customer_name, a.customer_account_status
        FROM accounts a
        JOIN customer c ON a.customer_id = c.customer_id
        WHERE a.customer_account_status != 'active'
        """
    )
    blocked = cursor.fetchall()

    print("\n" + "=" * 75)
    print("                        BLOCKED / INACTIVE ACCOUNTS                    ")
    print("=" * 75)
    print(f"{'Account ID':<12} | {'Account Number':<18} | {'Name':<22} | {'Status'}")
    print("-" * 75)
    if not blocked:
        print("All bank accounts are currently active.")
    else:
        for b in blocked:
            print(f"{b[0]:<12} | {b[1]:<18} | {b[2]:<22} | {b[3]}")
    print("=" * 75)

    if blocked:
        target_acc = input("\nEnter Account Number to unblock / set active (or press Enter to cancel): ").strip()
        if target_acc:
            cursor.execute("UPDATE accounts SET customer_account_status = 'active' WHERE aacount_number = %s", (target_acc,))
            db.commit()
            if cursor.rowcount > 0:
                print(f"[SUCCESS] Account {target_acc} is now ACTIVE!")
            else:
                print("[ERROR] Account number not found.")
    cursor.close()
    db.close()

def view_branches():
    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    cursor.execute("SELECT branch_id, branch_name, branch_address, city, phone, ifsc_code FROM branch")
    branches = cursor.fetchall()
    cursor.close()
    db.close()

    print("\n" + "=" * 85)
    print("                               BANK BRANCHES                                  ")
    print("=" * 85)
    print(f"{'ID':<4} | {'Branch Name':<25} | {'City':<12} | {'IFSC Code':<12} | {'Phone'}")
    print("-" * 85)
    if not branches:
        print("No branches configured.")
    else:
        for b in branches:
            print(f"{b[0]:<4} | {b[1]:<25} | {b[3] or 'N/A':<12} | {b[5]:<12} | {b[4] or 'N/A'}")
    print("=" * 85)

def admin_menu():
    while True:
        print("\n" + "=" * 45)
        print("         BANK MANAGER ADMIN CONSOLE          ")
        print("=" * 45)
        print("1. View All Registered Customers")
        print("2. View All Customer Accounts & Reserves")
        print("3. Search Customer")
        print("4. Review & Approve Loan Applications")
        print("5. View Recent Bank Transactions")
        print("6. Manage Inactive / Blocked Accounts")
        print("7. View Bank Branches & IFSC Codes")
        print("8. Logout Admin Console")
        print("=" * 45)

        choice = input("Enter Admin Choice (1-8): ").strip()

        if choice == "1":
            view_all_customers()
        elif choice == "2":
            view_all_accounts()
        elif choice == "3":
            search_customer()
        elif choice == "4":
            manage_loans()
        elif choice == "5":
            view_all_transactions()
        elif choice == "6":
            manage_account_status()
        elif choice == "7":
            view_branches()
        elif choice == "8":
            print("[INFO] Logging out from Admin console...")
            break
        else:
            print("[ERROR] Invalid choice. Please choose 1-8.")

if __name__ == "__main__":
    pin_check()
