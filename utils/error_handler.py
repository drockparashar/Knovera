from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({"error": str(e)}), 500
