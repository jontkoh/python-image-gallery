from . import db
import psycopg2
from .user import User
from .user_dao import UserDAO

class PostgresUserDAO(UserDAO):
  def __init__(self):
    pass
  def get_users(self):
    result = []
    result += db.listUsers()
    return result
