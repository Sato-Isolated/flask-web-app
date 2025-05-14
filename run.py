from app import app, db
from dotenv import load_dotenv
import os

# Charge les variables d'environnement depuis .env
load_dotenv()
# Configuration de l'application Flask
if __name__ == '__main__':
    with app.app_context():
        # Crée la base de données
        db.create_all()
    # Démarre le serveur Flask
    app.run(debug=True)