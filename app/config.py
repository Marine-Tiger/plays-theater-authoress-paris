import dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config():
    DEBUG = os.environ.get("DEBUG")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    WTF_CSRF_ENABLE=os.environ.get("WTF_CSRF_ENABLE")
    SECRET_KEY=os.environ.get("SECRET_KEY")
    AUTRICES_PER_PAGE = int(os.environ.get("AUTRICES_PER_PAGE"))
    PIECES_PER_PAGE= int(os.environ.get("PIECES_PER_PAGE"))
    THEATRES_PER_PAGE= int(os.environ.get("THEATRES_PER_PAGE"))
