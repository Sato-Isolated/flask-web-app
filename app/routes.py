from flask import Flask, render_template, request, redirect, url_for, flash, session

from . import app, db
from .models import User
# Route pour la page login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # check si la méthode de la requête est POST
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form['email']
        password = request.form['password']
        # Vérifier si l'utilisateur existe et si le mot de passe est correct
        user = User.find_by_email(email)
        if user and user.check_password(password):
            # Si l'utilisateur est trouvé et le mot de passe est correct, on le connecte
            session['user_email'] = user.email
            flash('Connexion réussie !', 'success')
            return redirect(url_for('home'))
        else:
            flash('Identifiants invalides. Veuillez réessayer.', 'danger')
    return render_template('login.html', user_email=session.get('user_email'))
# Route pour la page d'inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Check si la méthode de la requête est POST
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']
        # Vérifier si tous les champs sont remplis
        if not email or not password or not password_confirmation:
            flash('Tous les champs sont obligatoires.', 'danger')
            # Verifier si le mot de passe correspond à la confirmation
        elif password != password_confirmation:
            flash('Les mots de passe ne correspondent pas.', 'danger')
        # Vérifier si l'email est déjà utilisé
        elif User.find_by_email(email):
            flash('Cet email est déjà utilisé.', 'danger')
        else:
            # Créer un nouvel utilisateur
            user = User(email=email)
            # Ajouter le mot de passe
            user.set_password(password)
            # Ajouter l'utilisateur à la base de données
            db.session.add(user)
            # Enregistrer les modifications
            db.session.commit()
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html', user_email=session.get('user_email'))

# Route pour la page d'accueil
@app.route('/', methods=['GET'])
def home():
    email = session.get('user_email', None)
    return render_template('home.html', user_email=email)
# Route pour se déconnecter
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_email', None)
    return redirect(url_for('home'))