import sys

def main():
    while True:
        print("\n" + "=" * 52)
        print("           MANIT BANK MANAGEMENT SYSTEM             ")
        print("=" * 52)
        print("  1. Customer Banking (Sign Up / Login / Services)")
        print("  2. ATM Machine (Withdrawal / Deposit / Transfer)")
        print("  3. Bank Staff / Admin Portal")
        print("  4. Initialize / Verify Database & Tables")
        print("  5. Exit")
        print("=" * 52)

        choice = input("Enter Your Choice (1-5): ").strip()

        if choice == "1":
            try:
                from Model import customer_menu
                customer_menu()
            except ImportError as e:
                print(f"\n[ERROR] Could not load Customer module: {e}")

        elif choice == "2":
            try:
                from Atm import atm_menu
                atm_menu()
            except ImportError as e:
                print(f"\n[ERROR] Could not load ATM module: {e}")

        elif choice == "3":
            try:
                from Admin import pin_check
                pin_check(pin="1234", attempt=3)
            except ImportError as e:
                print(f"\n[ERROR] Could not load Admin module: {e}")

        elif choice == "4":
            try:
                from Connection_Bank import initialize_database
                initialize_database()
            except ImportError as e:
                print(f"\n[ERROR] Could not load Database module: {e}")

        elif choice == "5":
            print("\nThank you for banking with MANIT Bank. Goodbye!\n")
            sys.exit(0)

        else:
            print("[ERROR] Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
