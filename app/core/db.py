import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="stock_ai",
        user="stockuser",
        password="stockpass",
        host="localhost",
        port="5432"
    )