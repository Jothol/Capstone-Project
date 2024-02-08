import firebase_admin
from firebase_admin import credentials
from database import user

cred = credentials.Certificate(r"database-access-key.json")
firebase_admin.initialize_app(cred)

new_user = user.User()
new_user.add_user()
