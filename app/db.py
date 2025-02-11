import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import pandas as pd

load_dotenv()


def get_annotated_tweets():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT text, positive, negative FROM tweets")
    rows = cursor.fetchall()
    connection.close()

    return pd.DataFrame(rows)


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"erreur: {e}")
        return None


def save_tweet(tweet, positive, negative):
    if positive == True:
        positive = 1
    else:
        positive = 0
    if negative == True:
        negative = 1
    else:
        negative = 0
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)", (tweet, positive, negative))
        connection.commit()
        connection.close()
        return True
    return False
