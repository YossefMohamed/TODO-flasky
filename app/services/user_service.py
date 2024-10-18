from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def register_user(username, email, password):
        existing_user = UserRepository.get_by_username(username)
        if existing_user:
            return None, "Username already exists"
        
        existing_email = UserRepository.get_by_email(email)
        if existing_email:
            return None, "Email already exists"
        
        return UserRepository.create(username, email, password), None

    @staticmethod
    def authenticate_user(username, password):
        user = UserRepository.get_by_username(username)
        if user and user.check_password(password):
            return user
        return None