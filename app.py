import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.routes import bp
from flask import Flask

app = Flask(__name__)

app.register_blueprint(bp)
if __name__ == "__main__":
    app.run(debug=True)