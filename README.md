# TP-Final-Algo

## Description
Un projet pour analyser le sentiment des tweets grâce à un modèle de machine learning. Ce projet utilise Flask pour l'API et MySQL pour la base de données.

## Structure du Projet
- `app/` : Contient les fichiers Flask pour l'API.
  - `__init__.py` : Initialisation de Flask.
  - `routes.py` : Gestion des endpoints.
  - `models.py` : Modèle de machine learning (à implémenter).
  - `db.py` : Connexion à la base de données (à implémenter).
- `setup_db.py` : Script pour configurer la base MySQL.
- `train.py` : Script pour entraîner ou réentraîner le modèle.
- `cronjob.sh` : Script pour automatiser le réentraînement.
- `app.py` : Pour lancer l'application
- `README.md` : Documentation du projet.

## Installation
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/tonutilisateur/api-analyse-sentiments.git
   cd api-analyse-sentiments

2. Créez un environnement virtuel :

   python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Installez les dépendances :
    pip install flask

4. Utilisation : 

   python app.py

   Par défaut, le serveur sera accessible à l’adresse suivante :
   http://127.0.0.1:5000

   Testez l'endpoint : 

   Méthode : POST
   URL : http://127.0.0.1:5000/analyze