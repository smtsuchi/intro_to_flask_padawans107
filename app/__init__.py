from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

from .auth.routes import auth
from .api.routes import api
from .shop.routes import shop

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)

login_manager.login_view='auth.loginPage'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


app.register_blueprint(auth)
app.register_blueprint(api)
app.register_blueprint(shop)



from . import routes
from . import models