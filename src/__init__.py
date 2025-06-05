from http.client import HTTPException
from flask import Flask, jsonify, redirect
from src.constants.http_status_code import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import os
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
    CORS(app)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("FLASK_DB_URI", "postgresql+psycopg2://postgres:MB1301%40dev@db.axlydpdhwrswmnvigbfy.supabase.co:5432/postgres?sslmode=require"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', "dev"),
            
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

    # Default route
    @app.get('/')
    def index():
        return redirect('/apidocs')

    # Error handlers
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({'error': e.description}), e.code
        return jsonify({'error': 'Internal Server Error'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
