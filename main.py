from login_manager import login_manager
from user import User
from app import app


@login_manager.user_loader
def load_user(user_id):
    """
    Load the user from the user ID.

    Args:
        user_id (str): The user ID.

    Returns:
        User: User object with the given user ID.
    """
    return User(user_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
