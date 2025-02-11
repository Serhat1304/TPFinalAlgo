
from flask import Blueprint, jsonify, request
import joblib
from app.db import get_db_connection, save_tweet
from app.models import entrainer_modele, entrainer_depuis_bdd, evaluate_model

bp = Blueprint('api', __name__)


@bp.route('/entrainer', methods=['GET'])
def entrainer():
    entrainer_modele()
    return jsonify({"message": "entrainé"})

@bp.route('/entrainer-bdd', methods=['GET'])
def entrainer_bdd():
    entrainer_depuis_bdd()
    return jsonify({"message": "entrainé bdd"})
@bp.route('/evaluer', methods=['GET'])
def evaluer():
    evaluate_model()
    return jsonify({"message": "évalué"})

@bp.route('/analyze', methods=['POST'])
def analyze_sentiments():

    model = joblib.load('sentiment.pkl')

    tweets = request.json.get('tweets', [])
    if not tweets:
        return jsonify({"error": "Aucun tweet fourni"}), 400

    predictions = model.predict(tweets)

    scores = {tweet: float(pred) for tweet, pred in zip(tweets, predictions)}

    for score in scores:
        save_tweet(score, scores[score] == 1, scores[score] == -1)

    return jsonify(scores)

