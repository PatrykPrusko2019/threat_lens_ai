from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register_user(self, email: str, password: str) -> User:
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        password_hash = hash_password(password)
        return self.user_repository.create(email=email, password_hash=password_hash)    
    
    def login_user(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")  
        
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        return create_access_token(subject=user.id)