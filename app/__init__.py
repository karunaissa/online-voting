from flask import Flask
from redis import Redis
import os

redis_host = os.getenv("REDIS_HOST", "redis")

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Redis client
    app.redis = Redis(host=redis_host, port=6379, decode_responses=True)

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    return app
