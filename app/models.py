import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd


def entrainer_modele():
    data = pd.DataFrame({
        'text': [
            "J'aime ce produit",
            "Je déteste ce service",
            "C'est un bon film",
            "Le temps est horrible",
            "Quelle journée fantastique!"
        ],
        'label': [1, -1, 1, -1, 1]
    })

    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000)),
        ('clf', LogisticRegression())
    ])

    model.fit(data['text'], data['label'])

    joblib.dump(model, 'sentiment.pkl')

    print(" entrainement ok.")
