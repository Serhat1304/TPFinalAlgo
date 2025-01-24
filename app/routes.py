from flask import Blueprint, jsonify

bp = Blueprint('api', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze_sentiments():
    return jsonify({"message": "Test d'endpoint"})