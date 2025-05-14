from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Classe représentant un utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
    
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self, db):
        query = "INSERT INTO users (email, password) VALUES (?, ?)"
        db.execute(query, (self.email, self.password_hash))
        db.commit()

    @staticmethod
    def validate_password(stored_password, provided_password):
        return stored_password == provided_password