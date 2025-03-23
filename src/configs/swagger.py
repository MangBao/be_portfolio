template = {
    "swagger": "2.0",
    "info": {
        "title": "Portfolio API",
        "description": """
        API Documentation for Portfolio Backend:
        * Authentication - User management and JWT authentication
        * Menu - Navigation menu management
        * About - Personal information
        * Projects - Portfolio projects
        * Skills - Technical skills
        * Experience - Work experience
        * Contact - Contact form management
        """,
        "version": "1.0"
    },
    "basePath": "/api/v1",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    }
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
            "doc_dir": "src/docs"
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs"
}