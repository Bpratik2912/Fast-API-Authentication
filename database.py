from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# settings to configure database.
settings = {
    "database": {
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "dbname": "sqlalchemydb2"
    }
}

# create engine instance.
def get_engine(user, password, host, port, dbname):
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

# Connects to the database.
engine = get_engine(
    settings['database']['user'], settings['database']['password'],
    settings['database']['host'], settings['database']['port'],
    settings['database']['dbname']
)

# Executes operations like inserting, querying, and updating data.
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session generator
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# Test connection
def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
