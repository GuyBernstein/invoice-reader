import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connection for creating the DB
DB_HOST = "node128.codingbc.com"
DB_PORT = "9001"
DB_USER = "postgres"
DB_PASSWORD = "Lesson2017890"
DB_NAME = "[yourname]_invoice_db"

# SQLAlchemy connection to the app's database
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_connection = None

def get_db_connection():
    global db_connection
    try:
        db_connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        db_connection.autocommit = True
        return db_connection
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        db_connection = None
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE {DB_NAME};")
                print("Database initialized successfully.")
                return True
        except psycopg2.Error as e:
            if "already exists" in str(e):
                print("Database already exists.")
                return True
            print(f"Error initializing database: {e}")
            return False
        finally:
            if conn:
                conn.close()
    return False
if __name__ == "__main__":
    init_db()





import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connection configuration
DB_HOST = "node128.codingbc.com"
DB_PORT = "9001"
DB_USER = "postgres"
DB_PASSWORD = "Lesson2017890"
DB_NAME = "guy_invoice_db" 

# SQLAlchemy connection to the app's database
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = None
SessionLocal = None

db_connection = None

def get_db_connection():
    """Get connection to the application database"""
    global db_connection
    try:
        db_connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        db_connection.autocommit = True
        return db_connection
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        db_connection = None
        return None

def init_db():
    """Initialize the database - create it if it doesn't exist"""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname="postgres"  # Connect to default postgres database
        )
        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (DB_NAME,)
            )
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
                print(f"Database '{DB_NAME}' created successfully.")
            else:
                print(f"Database '{DB_NAME}' already exists.")

        global engine, SessionLocal
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        return True

    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        if conn:
            conn.close()

def test_connection():
    """Test if we can connect to the application database"""
    conn = get_db_connection()
    if conn:
        print(f"Successfully connected to database '{DB_NAME}'")
        conn.close()
        return True
    return False

if __name__ == "__main__":
    if init_db():
        test_connection()