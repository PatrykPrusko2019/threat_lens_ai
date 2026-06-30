import os

from app.core.security import hash_password
from app.db.models.user import User
from app.db.session import SessionLocal


def main() -> None:
    email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    password = os.getenv("ADMIN_PASSWORD", "admin123")

    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            print(f"Admin user already exists: {email}")
            return

        admin = User(
            email=email,
            password_hash=hash_password(password),
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print(f"Admin user created: {email}")

    finally:
        db.close()


if __name__ == "__main__":
    main()