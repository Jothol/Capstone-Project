import firebase_admin
from firebase_admin import credentials, firestore
from src.database import session, account


# Tests that get and delete don't work since "test" hasn't been created
def test_01():
    session.get_session("test")
    session.delete_session("test", "joe")


def test_02():
    group = session.create_session("test_02", "peter")


# Makes a session
def test_03():
    # Get an account name to become the host of the session
    user = account.create_account("bob", "bob_backwards")

    # Creates the session
    group = session.create_session("test_03", "bob")  # fix host_name issue

    print("Session created: " + group.get_name())
    print("Hosted by: " + group.get_host())

    # Session name is returned & Retrieve the name of the host
    session.get_session("test_03")
    host = session.get_host("test_03")

    account.create_account("U1_test03", "b")
    account.create_account("U2_test03", "m")
    account.create_account("U3_test03", "s")

    # Add three friends to the session
    group.add_user("U1_test03")
    group.add_user("U2_test03")
    group.add_user("U3_test03")


# Host is already part of another section
def test_04():
    db = firestore.client()
    acc = db.collection('users').document('bob')
    if not acc.get().exists:
        raise Exception
    if acc.get().to_dict().get('in_session') is True:
        raise Exception

    user = account.get_account("bob")


if __name__ == "__main__":
    cred = credentials.Certificate(r"database-access-key.json")
    firebase_admin.initialize_app(cred)

    test_03()
