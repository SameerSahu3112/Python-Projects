try:
    import mysql.connector
except ImportError:
    raise ImportError("The mysql-connector-python package is required. Install it with `pip install mysql-connector-python")

def create_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hda77063",
        database="bank"
    )
    return db