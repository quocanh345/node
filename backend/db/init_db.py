from psycopg2 import pool
from psycopg2.extras import RealDictCursor

my_pool = None

def pool_create():
    global my_pool
    my_pool = pool.SimpleConnectionPool(
        1, 10,
        user="postgres",
        password="tinuanoi345",
        host="localhost",
        database="mydb"
    )
    
    cur, con = pool_get()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """)
    con.commit()
    pool_put(con)

def pool_get():
    con = my_pool.getconn()
    return con.cursor(cursor_factory=RealDictCursor), con 

def pool_put(con):
    my_pool.putconn(con)

