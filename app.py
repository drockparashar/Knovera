from flask import Flask
from config.settings import *
from utils.error_handler import register_error_handlers
from routes.health import health_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(health_bp)

# Error handling
register_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
