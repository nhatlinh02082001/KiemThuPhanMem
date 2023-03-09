from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = '^TDYGF^&FD&S7dft7dg7&TFđ)TIE)FUIUWGF^&S'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@localhost/quanlyhocsinh?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

cloudinary.config(
        cloud_name='metavere',
        api_key='861726529933798',
        api_secret='-YjT4_flbgKHC4B9lhvkR4Hz87w'
)

login = LoginManager(app=app)

# babel = Babel(app=app)

# @babel.localeselector
# def get_locale():
#         return 'vi'

