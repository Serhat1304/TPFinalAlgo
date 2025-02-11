import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        if connection.is_connected():
            print("Connexion reussie")
            return connection
    except Error as e:
        print(f"erreur: {e}")
        return None


def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tweets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text TEXT NOT NULL,
        positive BOOLEAN NOT NULL,
        negative BOOLEAN NOT NULL
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table créé")
    except Error as e:
        print(f"erreur: {e}")

