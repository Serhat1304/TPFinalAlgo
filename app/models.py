import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd
from app.db import get_db_connection, get_annotated_tweets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from flask import jsonify

matplotlib.use('Agg')



def entrainer_modele():
    data = pd.DataFrame({
        'text': [
            "J'adore ce produit, il est fantastique et de haute qualité.",
            "Ce service client est exemplaire, je suis vraiment satisfait.",
            "C'est un excellent film, l'histoire et la réalisation sont remarquables.",
            "Une expérience incroyable, je recommande vivement.",
            "La nourriture était délicieuse, un vrai régal pour les papilles.",
            "J'ai passé un moment merveilleux grâce à ce service.",
            "La qualité de ce produit dépasse largement mes attentes.",
            "Ce restaurant offre une ambiance chaleureuse et une cuisine exquise.",
            "Le personnel était accueillant et professionnel, expérience top.",
            "Une prestation exceptionnelle, le meilleur que j'aie jamais vu.",
            "Je suis enchanté par la rapidité et l'efficacité du service.",
            "L'application est intuitive et agréable à utiliser.",
            "Un produit fiable et performant, je le recommande sans hésiter.",
            "Le design est élégant et moderne, j'adore ce produit.",
            "Ce spectacle était impressionnant, un vrai moment de bonheur.",
            "Je suis ravi de mon achat, il répond parfaitement à mes attentes.",
            "Une expérience sensorielle unique, je suis conquis.",
            "La livraison a été rapide et le produit est arrivé en parfait état.",
            "Une performance époustouflante, le meilleur de la saison.",
            "Je recommande ce service, c'est une véritable perle rare.",

            "Le produit est arrivé à l'heure, rien de spécial.",
            "Le service était correct, sans plus.",
            "Le film était moyen, ni mauvais ni exceptionnel.",
            "L'expérience a été acceptable, sans enthousiasme particulier.",
            "La nourriture était correcte, mais sans saveur marquante.",
            "J'ai trouvé l'application standard, ni bien ni mal.",
            "Le restaurant est moyen, sans particularité.",
            "La qualité du produit est passable, rien d'extra.",
            "Le spectacle était neutre, sans émotions fortes.",
            "Le service client a répondu, mais sans enthousiasme.",
            "La prestation était simplement correcte.",
            "L'expérience était ordinaire, sans surprise.",
            "Le design est classique, rien d'innovant.",
            "L'achat était conforme à mes attentes, ni plus ni moins.",
            "Le produit fonctionne, sans éclat particulier.",
            "Le film était standard, avec des moments prévisibles.",
            "Le service a été rendu, sans fioritures.",
            "La livraison était dans les temps, sans accrocs.",
            "L'application fonctionne bien, sans se démarquer.",
            "Le service est moyen, sans aspects remarquables.",

            "Je déteste ce produit, il est de très mauvaise qualité.",
            "Le service client est catastrophique, je ne recommanderai jamais.",
            "C'était un film décevant, l'histoire était confuse et mal réalisée.",
            "Une expérience désastreuse, à éviter absolument.",
            "La nourriture était immangeable, une grosse déception.",
            "J'ai passé un moment pénible à cause de ce service médiocre.",
            "La qualité de ce produit laisse vraiment à désirer.",
            "Ce restaurant offre une ambiance désagréable et un service déplorable.",
            "Le personnel était froid et peu accueillant, très décevant.",
            "Une prestation lamentable, rien à recommander.",
            "Je suis mécontent de la lenteur et de l'inefficacité du service.",
            "L'application est complexe et peu intuitive, une vraie galère.",
            "Un produit peu fiable et défectueux, à éviter absolument.",
            "Le design est dépassé et peu attrayant, je n'aime pas du tout.",
            "Ce spectacle était ennuyeux, un véritable gâchis de temps.",
            "Je regrette mon achat, il ne répond pas du tout à mes attentes.",
            "Une expérience sensorielle négative, totalement décevante.",
            "La livraison a été extrêmement lente et le produit était abîmé.",
            "Une performance médiocre, bien en dessous des attentes.",
            "Je déconseille ce service, une perte de temps et d'argent."
        ],
        'label': [1] * 20 + [0] * 20 + [-1] * 20
    })

    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2), lowercase=True)),
        ('clf', LogisticRegression(C=1.0, solver='liblinear', multi_class='ovr', class_weight='balanced'))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        data['text'], data['label'], test_size=0.5, random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    joblib.dump(model, 'sentiment.pkl')
    print("ok terminé.")


def entrainer_depuis_bdd():
    connection = get_db_connection()
    if connection:
        query = "SELECT text, positive, negative FROM tweets"
        data = pd.read_sql(query, connection)
        data['label'] = data.apply(lambda row: 1 if row['positive'] else -1, axis=1)
        model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2), lowercase=True)),
            ('clf', LogisticRegression(C=1.0, solver='liblinear', class_weight='balanced'))
        ])

        X_train, X_test, y_train, y_test = train_test_split(
            data['text'], data['label'], test_size=0.5, random_state=42
        )

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

        joblib.dump(model, 'sentiment.pkl')




def evaluate_model():

    df = get_annotated_tweets()
    if df is None or df.empty:
        return jsonify({"error": "pas de données"}), 400

    try:
        model = joblib.load('sentiment.pkl')
    except FileNotFoundError:
        print("Erreur : pas de modèle")
        return jsonify({"error": "pas de modèle"}), 500

    predictions = model.predict(df["text"])

    true_labels = []
    for _, row in df.iterrows():
        if row['positive'] == 1:
            true_labels.append(1)
        elif row['negative'] == 1:
            true_labels.append(-1)
        else:
            true_labels.append(0)

    true_labels = np.array(true_labels)

    conf_matrix = confusion_matrix(true_labels, predictions, labels=[1, 0, -1])

    try:
        plt.figure(figsize=(6, 5))
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
                    xticklabels=['Positif', 'Neutre', 'Négatif'],
                    yticklabels=['Positif', 'Neutre', 'Négatif'])
        plt.xlabel("Prédictions")
        plt.ylabel("Vraies valeurs")
        plt.title("Matrice de confusion des prédictions")
        plt.savefig("confusion_matrix.png")
    except Exception as e:
        return jsonify({"error": "ko sauvegarde de l'image."}), 500

    report = classification_report(true_labels, predictions, target_names=['Positif', 'Neutre', 'Négatif'])
    print(report)

    return jsonify({"message": "ok", "rapport": report})

