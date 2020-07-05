from . import db
from .user import User
from .user_dao import UserDAO

class PostgresUserDAO(UserDAO):
  def __init__(self):
    pass
  def get_users(self):
    result = []
    cursor = db.execute("select username, password, full_name from users")
    username = cursor.fetchall()
    for t in username:
      result.append(User(t[0], t[1], t[2]))
    return result