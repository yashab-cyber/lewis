from flask import Flask
from flask_cors import CORS
from routes.api import api_blueprint
from routes.auth import auth_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_blueprint, url_prefix="/api")
app.register_blueprint(auth_blueprint, url_prefix="/auth")

@app.route("/")
def index():
    return "<h1>LEWIS Flask Backend Running</h1>"

if __name__ == "__main__":
    app.run(debug=True)
