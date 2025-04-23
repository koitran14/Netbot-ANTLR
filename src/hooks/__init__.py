_current_user = None

def set_current_user(user):
    global _current_user
    _current_user = user

def get_current_user():
    return _current_user

def clear_current_user():
    global _current_user
    _current_user = None