from http.client import HTTPException
from flask import Flask, jsonify, redirect, current_app
from src.constants.http_status_code import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import os
import traceback
from sqlalchemy import text
from src.auth import auth
from src.about import about
from src.menu import menu
from src.project import project
from src.skill import skill
from src.experience import experience
from src.contact import contact
from src.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from src.configs.swagger import template, swagger_config
from flask_cors import CORS
from flask_migrate import Migrate

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config["DEBUG"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    # Configure CORS for production deployment
    # Allow all origins for now - you can restrict this to specific domains later
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })

    print("FLASK_DB_URI =", os.getenv("FLASK_DB_URI"))

    if test_config is None:
        # Get required environment variables
        secret_key = os.environ.get("SECRET_KEY")
        jwt_secret_key = os.environ.get('JWT_SECRET_KEY')
        db_uri = os.environ.get("FLASK_DB_URI")
        
        # Validate required environment variables
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable is required. Please set it in .env file or environment.")
        if not jwt_secret_key:
            raise ValueError("JWT_SECRET_KEY environment variable is required. Please set it in .env file or environment.")
        if not db_uri:
            raise ValueError("FLASK_DB_URI environment variable is required. Please set it in .env file or environment.")
        
        app.config.from_mapping(
            SECRET_KEY=secret_key,
            SQLALCHEMY_DATABASE_URI=db_uri,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=jwt_secret_key,
            
            # JWT Config
            JWT_ACCESS_TOKEN_EXPIRES=24*60*60,  # 24 hours
            JWT_REFRESH_TOKEN_EXPIRES=30*24*60*60,  # 30 days
            
            # Swagger Config
            SWAGGER={
                'title': "Portfolio API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    # Initialize database
    db.app = app
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize JWT
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(about)
    app.register_blueprint(menu)
    app.register_blueprint(project)
    app.register_blueprint(skill)
    app.register_blueprint(experience)
    app.register_blueprint(contact)

    # Initialize Swagger after registering blueprints
    Swagger(app, template=template, config=swagger_config)

    # Health check endpoint for Render
    @app.get('/health')
    def health_check():
        """Simple health check endpoint - returns API status without DB check"""
        from datetime import datetime
        
        # Simple health response without database check
        # This ensures the endpoint always works even if DB is down
        return jsonify({
            'status': 'healthy',
            'message': 'Portfolio API is running',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        }), HTTP_200_OK
    
    # Health check endpoint for Render
    @app.get("/health/db")
    def health_db():
        db.session.execute(text("SELECT 1"))
        return {"db": "ok"}

    # Default route - redirect to API docs
    @app.get('/')
    def index():
        return redirect('/apidocs')

    # Error handlers
    @app.errorhandler(Exception)
    def handle_exception(e):
        # LOG RA STDERR để Render thấy
        current_app.logger.error(traceback.format_exc())

        if isinstance(e, HTTPException):
            return jsonify({'error': e.description}), e.code

        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e) if current_app.debug else 'Something went wrong'
        }), HTTP_500_INTERNAL_SERVER_ERROR

    return app
