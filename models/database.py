import os
from sqlalchemy import create_engine
from sqlalchemy.orm  import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASS = os.getenv("DB_PASSWORD")

engine = create_engine(f'mysql+pymysql://{DB_USERNAME}:{DB_PASS}@{DB_HOST}/{DB_NAME}',echo=True)

Session = sessionmaker(bind=engine)
session = Session()

# try:
#     connection = engine.connect()
#     print("connection successfully")
#     connection.close()
# except Exception as e:
#     print("Connection error", e)