import sqlite3

def query_db(sql_query):
    with sqlite3.connect("movies.db") as conn:
        cur = conn.cursor()
        cur.execute(sql_query)
        return cur.fetchall()

def read(table = "users"):
    return query_db(f"SELECT * FROM {table}")

def select(column, table):
    return query_db(f"SELECT {column} FROM {table}")

def write(table ,name, password):
    return query_db (f"INSERT INTO {table}(name,password) VALUES ('{name}','{password}')")

def update( table, column, text, column2, user_n):
    query_db(f"UPDATE {table} SET {column} = '{text}' WHERE {column2} = '{user_n}'")

def delete(table,id2):
    return query_db (f"DELETE FROM {table} WHERE id = {id2}")

def check_password(name):
    return query_db (f"SELECT password FROM users WHERE name = '{name}'")


def show_something(column, name):
    return query_db(f"SELECT {column} FROM users WHERE name = '{name}' ")

def show_something2(column, table, column2, name):
    return query_db(f"SELECT {column} FROM {table} WHERE {column2} = '{name}' ")




