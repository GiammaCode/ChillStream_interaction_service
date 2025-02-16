from flask import Blueprint

from .notifications import notifications_bp
from .reactions import reactions_bp
from .views import view_bp
from .recommendeds import recommended_bp


def init_routes(app):
    app.register_blueprint(view_bp, url_prefix="/users", name="views_blueprint")
    app.register_blueprint(recommended_bp, url_prefix="/users", name="recommendeds_blueprint")
    app.register_blueprint(notifications_bp, url_prefix="/users", name="notifications-blueprint")
    app.register_blueprint(reactions_bp, url_prefix="/users", name="reactions-blueprint")
