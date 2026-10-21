import sys
import os

# Adiciona o diretório atual ao python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import hash_password

def create_admin():
    # As credenciais vêm do ambiente (veja o .env.example), nunca do código.
    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not (username and email and password):
        print("Defina ADMIN_USERNAME, ADMIN_EMAIL e ADMIN_PASSWORD no ambiente antes de rodar este script.")
        sys.exit(1)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            print(f"Usuário '{username}' já existe. Atualizando privilégios e senha...")
            user.password_hash = hash_password(password)
            user.is_admin = True
            user.is_premium = True
            user.allow_ai = True
        else:
            print(f"Criando novo usuário administrador '{username}'...")
            user = User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                is_admin=True,
                is_premium=True,
                allow_ai=True
            )
            db.add(user)
        
        db.commit()
        print("Sucesso! Conta de administrador configurada com sucesso.")
        print(f"Username: {username}")
        print(f"E-mail: {email}")
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar administrador: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
