from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'&\t\xed\xb8\xe8\xba\xae(K\x82\xe0\xfdz\xdf$\x80'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tenant_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
db.init_app(app)
Migrate(app, db)

bcrypt = Bcrypt(app)
api = Api(app)
CORS(app)
jwt = JWTManager(app)
