from flask import Blueprint, request, jsonify

bp = Blueprint('api', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze_sentiments():
    data = request.get_json()
    if not data or 'tweets' not in data:
        return jsonify({"error": "No tweets provided"}), 400

    tweets = data['tweets']

    # Placeholder: affecte "positive" à chaque tweet reçu
    results = [
        {
            "tweet": tweet,
            "sentiment": "positive"
        }
        for tweet in tweets
    ]

    return jsonify({"results": results})
