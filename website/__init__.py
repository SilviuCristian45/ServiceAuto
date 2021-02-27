from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_uploads import UploadSet,configure_uploads,IMAGES,DOCUMENTS
from flask_mail import Mail, Message

db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
cv = UploadSet('cv',DOCUMENTS)
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'silviu.dinca20@gmail.com'
    app.config['MAIL_PASSWORD'] = '23SDFFFxx323'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.secret_key = 'the random string'
    db.init_app(app)
    mail.init_app(app)

    from .views import views
    from .auth import auth
    from .models import Client,Fix,FixDetail,User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.config['UPLOADED_PHOTOS_DEST'] = 'website/static/fiximg'
    app.config['UPLOADED_CV_DEST'] = 'website/static/cv'
    configure_uploads(app,photos)
    configure_uploads(app,cv)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app

