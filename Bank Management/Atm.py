import os
import sys

# Ensure local modules in Bank Management directory are always resolvable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_db():
    from Connection_Bank import create_connection
    return create_connection()

def verify_account(aacount_number):
    """Checks if account exists and returns (account_id, aacount_number, balance, customer_account_status, customer_name, customer_password)."""
    db = get_db()
    if not db:
        return None
    cursor = db.cursor()
    query = """
    SELECT a.account_id, a.aacount_number, a.balance, a.customer_account_status, c.customer_name, c.customer_password
    FROM accounts a
    JOIN customer c ON a.customer_id = c.customer_id
    WHERE a.aacount_number = %s
    """
    cursor.execute(query, (aacount_number,))
    account = cursor.fetchone()
    cursor.close()
    db.close()
    return account

def get_balance(account_id):
    """Returns current balance of account."""
    db = get_db()
    if not db:
        return None
    cursor = db.cursor()
    cursor.execute("SELECT balance, customer_account_status FROM accounts WHERE account_id = %s", (account_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result

def atm_menu(default_account_number=None):
    print("\n" + "=" * 45)
    print("           MANIT BANK ATM SYSTEM            ")
    print("=" * 45)

    if default_account_number:
        acc_num = str(default_account_number).strip()
    else:
        acc_num = input("Please Enter Your 10-Digit Account Number: ").strip()

    acc = verify_account(acc_num)
    if not acc:
        print("[ERROR] Account Number Not Found! Please check and try again.")
        return

    account_id, aacount_number, balance, account_status, customer_name, actual_password = acc

    if account_status != 'active':
        print("[ALERT] This bank account is currently BLOCKED or INACTIVE.")
        print("Please contact your branch to unblock.")
        return

    # Security Authentication (3 attempts)
    remaining_attempts = 3
    authenticated = False
    while remaining_attempts > 0:
        entered_pin = input(f"Enter Your ATM PIN / Password ({remaining_attempts} attempt(s) left): ").strip()
        if entered_pin == actual_password:
            authenticated = True
            print(f"[SUCCESS] Access Granted! Welcome, {customer_name}.")
            break
        else:
            remaining_attempts -= 1
            if remaining_attempts == 0:
                db = get_db()
                if db:
                    cursor = db.cursor()
                    cursor.execute("UPDATE accounts SET customer_account_status = 'blocked' WHERE account_id = %s", (account_id,))
                    db.commit()
                    cursor.close()
                    db.close()
                print("[ALERT] 3 Incorrect PIN attempts! Your account has been temporarily BLOCKED for security.")
                return
            else:
                print(f"[ERROR] Incorrect PIN. You have {remaining_attempts} attempt(s) left.")

    if not authenticated:
        return

    # Main ATM Operations Loop
    while True:
        print("\n" + "-" * 42)
        print(f" ATM OPERATIONS | A/C: {aacount_number}")
        print("-" * 42)
        print("1. Check Balance / Fast Cash")
        print("2. Cash Withdrawal")
        print("3. Cash Deposit")
        print("4. Fund Transfer (Account to Account)")
        print("5. Mini Statement (Last 5 Transactions)")
        print("6. Change ATM PIN / Password")
        print("7. Eject & Exit ATM")
        print("-" * 42)

        choice = input("Please Select an Option (1-7): ").strip()

        if choice == "1":
            acc_info = get_balance(account_id)
            if acc_info:
                curr_bal, status = acc_info
                print("\n" + "=" * 38)
                print("           BALANCE INQUIRY            ")
                print("=" * 38)
                print(f" Account Number : {aacount_number}")
                print(f" Account Holder : {customer_name}")
                print(f" Current Balance: Rs. {float(curr_bal):,.2f}")
                print(f" Account Status : {status}")
                print("=" * 38)

        elif choice == "2":
            try:
                amount = float(input("Enter Amount to Withdraw (Rs.): "))
            except ValueError:
                print("[ERROR] Please enter a valid numeric amount.")
                continue

            if amount <= 0:
                print("[ERROR] Withdrawal amount must be greater than zero.")
                continue
            if int(amount) % 100 != 0:
                print("[ERROR] ATM dispenses only notes in multiples of Rs. 100 (100, 200, 500).")
                continue

            acc_info = get_balance(account_id)
            if not acc_info:
                print("[ERROR] Account not found.")
                continue

            current_balance = float(acc_info[0])
            if current_balance < amount:
                print(f"[ERROR] Insufficient Funds! Current balance is Rs. {current_balance:,.2f}")
                continue

            db = get_db()
            if not db:
                continue
            new_balance = current_balance - amount
            cursor = db.cursor()
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                (account_id, "ATM-Withdrawal", amount, "Cash withdrawn via ATM")
            )
            db.commit()
            cursor.close()
            db.close()

            print("\n[SUCCESS] Please collect your cash!")
            print(f"Withdrawn Amount : Rs. {amount:,.2f}")
            print(f"Available Balance: Rs. {new_balance:,.2f}")

        elif choice == "3":
            try:
                amount = float(input("Enter Amount to Deposit (Rs.): "))
            except ValueError:
                print("[ERROR] Please enter a valid numeric amount.")
                continue

            if amount <= 0:
                print("[ERROR] Deposit amount must be greater than zero.")
                continue
            if int(amount) % 100 != 0:
                print("[ERROR] ATM accepts notes in multiples of Rs. 100.")
                continue

            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                (account_id, "ATM-Deposit", amount, "Cash deposited via ATM")
            )
            db.commit()
            cursor.close()
            db.close()

            acc_info = get_balance(account_id)
            new_bal = float(acc_info[0]) if acc_info else 0.0
            print(f"\n[SUCCESS] Successfully deposited Rs. {amount:,.2f}")
            print(f"Updated Balance: Rs. {new_bal:,.2f}")

        elif choice == "4":
            recipient_acc = input("Enter Recipient Account Number: ").strip()
            if recipient_acc == aacount_number:
                print("[ERROR] Cannot transfer funds to the same account.")
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
                print("[ERROR] Recipient Account Number not found.")
                cursor.close()
                db.close()
                continue
            if recipient[2] != 'active':
                print("[ERROR] Recipient account is not active.")
                cursor.close()
                db.close()
                continue

            try:
                amount = float(input("Enter Transfer Amount (Rs.): "))
            except ValueError:
                print("[ERROR] Please enter a valid numeric amount.")
                cursor.close()
                db.close()
                continue

            if amount <= 0:
                print("[ERROR] Transfer amount must be greater than zero.")
                cursor.close()
                db.close()
                continue

            acc_info = get_balance(account_id)
            current_balance = float(acc_info[0])
            if current_balance < amount:
                print(f"[ERROR] Insufficient funds. Available balance: Rs. {current_balance:,.2f}")
                cursor.close()
                db.close()
                continue

            recipient_account_id = recipient[0]

            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, recipient_account_id))

            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                (account_id, "ATM-Transfer-Debit", amount, f"ATM transfer to A/C {recipient_acc}")
            )
            cursor.execute(
                "INSERT INTO bank_transaction (account_id, transaction_type, amount, description_customer) VALUES (%s, %s, %s, %s)",
                (recipient_account_id, "ATM-Transfer-Credit", amount, f"ATM transfer from A/C {aacount_number}")
            )
            db.commit()
            cursor.close()
            db.close()

            new_sender_bal = current_balance - amount
            print(f"\n[SUCCESS] Rs. {amount:,.2f} transferred successfully to Account: {recipient_acc}!")
            print(f"Remaining Balance: Rs. {new_sender_bal:,.2f}")

        elif choice == "5":
            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                "SELECT transaction_id, transaction_type, amount, transaction_date, description_customer FROM bank_transaction WHERE account_id = %s ORDER BY transaction_id DESC LIMIT 5",
                (account_id,)
            )
            records = cursor.fetchall()
            cursor.close()
            db.close()

            print("\n" + "=" * 75)
            print("                         ATM MINI STATEMENT                            ")
            print("=" * 75)
            print(f"{'Txn ID':<8} | {'Date/Time':<19} | {'Type':<18} | {'Amount (Rs.)':<12}")
            print("-" * 75)
            if not records:
                print("No recent transactions found.")
            else:
                for r in records:
                    t_date = r[3].strftime("%Y-%m-%d %H:%M") if hasattr(r[3], 'strftime') else str(r[3])
                    t_amt = f"{float(r[2]):,.2f}"
                    print(f"{r[0]:<8} | {t_date:<19} | {r[1]:<18} | Rs. {t_amt:<12}")
            print("=" * 75)

        elif choice == "6":
            old_pass = input("Enter Current PIN / Password: ").strip()
            if old_pass != actual_password:
                print("[ERROR] Incorrect Current PIN/Password!")
                continue

            new_pass = input("Enter New PIN / Password: ").strip()
            confirm_pass = input("Confirm New PIN / Password: ").strip()

            if not new_pass:
                print("[ERROR] Password cannot be empty.")
                continue
            if new_pass != confirm_pass:
                print("[ERROR] Passwords do not match!")
                continue

            db = get_db()
            if not db:
                continue
            cursor = db.cursor()
            cursor.execute(
                """
                UPDATE customer c
                JOIN accounts a ON c.customer_id = a.customer_id
                SET c.customer_password = %s
                WHERE a.account_id = %s
                """,
                (new_pass, account_id)
            )
            db.commit()
            cursor.close()
            db.close()

            actual_password = new_pass
            print("[SUCCESS] PIN / Password updated successfully!")

        elif choice == "7":
            print("\n[INFO] Thank you for using MANIT Bank ATM. Please take your receipt!")
            break
        else:
            print("[ERROR] Invalid choice. Please choose 1-7.")

if __name__ == "__main__":
    atm_menu()
