import os

try:
    import mysql.connector
    from mysql.connector import Error
    HAS_MYSQL = True
except ImportError:
    mysql = None
    Error = Exception
    HAS_MYSQL = False

# Default database configurations matching your local MySQL setup
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "hda77063"),
    "database": os.environ.get("DB_NAME", "bank")
}

def check_mysql_driver():
    """Checks if mysql-connector-python is installed."""
    if not HAS_MYSQL:
        print("\n" + "!" * 68)
        print(" [DEPENDENCY ERROR] 'mysql-connector-python' is not installed.")
        print(" Please run the following command in your terminal to install it:")
        print("     pip install mysql-connector-python")
        print("     or: python3 -m pip install mysql-connector-python")
        print("!" * 68 + "\n")
        return False
    return True

def create_connection(include_database=True):
    """Establishes and returns a connection to the MySQL database."""
    if not check_mysql_driver():
        return None

    config = DB_CONFIG.copy()
    if not include_database:
        config.pop("database", None)

    try:
        db = mysql.connector.connect(**config)
        return db
    except Error as e:
        errno = getattr(e, 'errno', None)
        if include_database and errno == 1049:  # Unknown database error
            success = initialize_database()
            if success:
                try:
                    return mysql.connector.connect(**DB_CONFIG)
                except Error as err:
                    print(f"\n[ERROR] Failed to connect after initialization: {err}")
                    return None
        print(f"\n[ERROR] Database connection failed: {e}")
        print("Please verify that your MySQL server is running and credentials in Connection_Bank.py are correct.")
        return None

def initialize_database():
    """Ensures database and any auxiliary tables exist and creates default branch if empty."""
    if not check_mysql_driver():
        return False

    print("\n[INFO] Verifying Bank Management Database tables...")
    try:
        # Step 1: Connect to server without database to ensure 'bank' exists
        conn = create_connection(include_database=False)
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS bank")
        conn.commit()
        cursor.close()
        conn.close()

        # Step 2: Connect to 'bank' database
        db = create_connection(include_database=True)
        if not db:
            return False
        cursor = db.cursor()

        # Create extension tables if they don't exist yet
        extensions = [
            """
            CREATE TABLE IF NOT EXISTS branch (
              branch_id INT NOT NULL AUTO_INCREMENT,
              branch_name VARCHAR(100) DEFAULT NULL,
              branch_address VARCHAR(255) DEFAULT NULL,
              city VARCHAR(50) DEFAULT NULL,
              phone VARCHAR(15) DEFAULT NULL,
              ifsc_code VARCHAR(11) NOT NULL,
              PRIMARY KEY (branch_id),
              UNIQUE KEY ifsc_code (ifsc_code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS fixed_deposit (
              fd_id INT NOT NULL AUTO_INCREMENT,
              customer_id BIGINT NOT NULL,
              account_id BIGINT NOT NULL,
              amount DECIMAL(12,2) NOT NULL,
              term_months INT NOT NULL,
              interest_rate DECIMAL(5,2) NOT NULL,
              maturity_amount DECIMAL(12,2) NOT NULL,
              start_date DATE NOT NULL,
              maturity_date DATE NOT NULL,
              status VARCHAR(20) DEFAULT 'Active',
              PRIMARY KEY (fd_id),
              KEY customer_id (customer_id),
              KEY account_id (account_id),
              CONSTRAINT fd_customer_fk FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
              CONSTRAINT fd_account_fk FOREIGN KEY (account_id) REFERENCES accounts (account_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS recurring_deposit (
              rd_id INT NOT NULL AUTO_INCREMENT,
              customer_id BIGINT NOT NULL,
              account_id BIGINT NOT NULL,
              monthly_amount DECIMAL(12,2) NOT NULL,
              term_months INT NOT NULL,
              interest_rate DECIMAL(5,2) NOT NULL,
              maturity_amount DECIMAL(12,2) NOT NULL,
              total_deposited DECIMAL(12,2) DEFAULT '0.00',
              months_paid INT DEFAULT '1',
              start_date DATE NOT NULL,
              status VARCHAR(20) DEFAULT 'Active',
              PRIMARY KEY (rd_id),
              KEY customer_id (customer_id),
              KEY account_id (account_id),
              CONSTRAINT rd_customer_fk FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
              CONSTRAINT rd_account_fk FOREIGN KEY (account_id) REFERENCES accounts (account_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        ]

        for q in extensions:
            cursor.execute(q)

        # Seed default branch if branch table is empty
        cursor.execute("SELECT COUNT(*) FROM branch")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(
                "INSERT INTO branch (branch_name, branch_address, city, phone, ifsc_code) VALUES (%s, %s, %s, %s, %s)",
                ("MANIT Main Campus Branch", "Link Road Number 3, MANIT", "Bhopal", "0755-2670327", "MANIT000101")
            )

        db.commit()
        cursor.close()
        db.close()
        print("[SUCCESS] Database tables verified successfully!\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to verify database: {e}\n")
        return False

if __name__ == "__main__":
    initialize_database()