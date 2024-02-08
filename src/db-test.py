import firebase_admin
from firebase_admin import credentials
from database import account

cred = credentials.Certificate(r"database-access-key.json")
firebase_admin.initialize_app(cred)

account.get_account("test")
account.delete_account("test")

user = account.create_account("test", "password")

print(account.try_login("test", "password"))
account.try_login("wrong", "password")
account.try_login("test", "wrong")

print(user.get_username() + " " + user.get_password())

user.reset_password("new_password")
print(user.get_username() + " " + user.get_password())

account.delete_account("test")

account.get_account("test")
