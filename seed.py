from models import db, User
from app import create_app

flask_app = create_app()
flask_app.app_context().push()

db.drop_all()
db.create_all()


a = User(username='dingo',
         password='test',
         email='hello@why.com',
         first_name='bob',
         last_name='Bobertson')

db.session.add(a)
db.session.commit()