from flask import Flask

def create_app():

    app = Flask(__name__)

    try:
        from backend.routes.auth_routes import auth_bp
        from backend.routes.product_routes import product_bp
        from backend.routes.user_routes import user_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(product_bp)
        app.register_blueprint(user_bp)

        return app
    except Exception as e:
        print(f"Error: {e}")