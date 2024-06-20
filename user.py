from flask_login import UserMixin

class User(UserMixin):
  """
  User class for Flask-Login integration. Inherits from UserMixin.

  Attributes:
      id (str): User identifier, typically the company ID.
  """

  def __init__(self, user_id):
      self.id = user_id

  @staticmethod
  def get(user):
      """
      Static method to get the user ID.

      Args:
          user (User): User object.

      Returns:
          str: User ID.
      """
      return user.id

