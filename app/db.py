import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"erreur: {e}")
        return None


def save_tweet(tweet, positive, negative):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)", (tweet, positive, negative))
        connection.commit()
        connection.close()
        return True
    return False
