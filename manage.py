import os

from dotenv import load_dotenv
from flask_migrate import Migrate

from app import blueprint
from app.main import create_app
from app.main.model.models import db

load_dotenv()

app = create_app(os.getenv('CONFIG_ENV') or 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(blueprint)

app.app_context().push()


def run():
    app.run()


if __name__ == '__main__':
    run()
