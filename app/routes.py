
from flask import Blueprint, jsonify, request
import joblib
from app.db import get_db_connection, save_tweet
from app.models import entrainer_modele


bp = Blueprint('api', __name__)


@bp.route('/entrainer', methods=['GET'])
def entrainer():
    entrainer_modele()
    return jsonify({"message": "entrainé"})


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

