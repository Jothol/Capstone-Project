import firebase_admin
from firebase_admin import credentials
from database import account
from database import session

cred = credentials.Certificate(r"database-access-key.json")
firebase_admin.initialize_app(cred)

# Tests that get and delete don't work since "test" hasn't been created
session.get_session("test")
session.delete_session("test", "joe")

# Get an account name to become the host of the session
# user bob is just for testing
user = account.create_account("bob", "bob_backwards")

# Creates the session
group = session.create_session("mix", "bob")  # fix host_name issue
# print("Session created: " + group.get_name())
# print("Hosted by: " + group.get_host())

# Session name is returned
session.get_session("mix")

# Retrieve the name of the host
host = session.get_host("mix")

# Deletes the session and the host from that session
session.delete_session("mix", "bob")
account.delete_account("bob")
