from flask import Flask
from app.api.routes import default_routes

app = Flask(__name__)
app.register_blueprint(default_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)