from app.models import User
from app import db

class AuthController:
    @staticmethod
    def register_user(username, email, password, confirm_password):
        if User.query.filter_by(username=username).first():
            return False, 'Nome de usuário já existe.'
        if User.query.filter_by(email=email).first():
            return False, 'Email já registrado.'
        if password != confirm_password:
            return False, 'As senhas não coincidem.'
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return True, 'Sua conta foi criada com sucesso! Faça login.'

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user, 'Login realizado com sucesso!'
        return None, 'Login ou senha incorretos.'
