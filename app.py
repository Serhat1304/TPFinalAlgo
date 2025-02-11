import sys
import os
from flask import Flask
from app.routes import bp

# Permet à Python de retrouver vos modules internes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
