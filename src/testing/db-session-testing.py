import firebase_admin
from firebase_admin import credentials, firestore
from src.database import session, account


# Both methods fail since "test" hasn't been created
def test_01():
    session.get_session("test")
    session.delete_session("test")


# Cannot create session since account "peter" is not created
def test_02():
    session.create_session("test_02", "peter")


# Makes a session
def test_03():
    # Get an account name to become the host of the session
    account.create_account("bob", "bob_backwards")

    # Creates the session
    group = session.create_session("test_03", "bob")  # fix host_name issue

    print("Session created: " + group.get_name())
    print("Hosted by: " + group.host.username)

    temp1 = account.create_account("U1_test03", "b")
    temp2 = account.create_account("U2_test03", "m")
    temp3 = account.create_account("U3_test03", "s")

    # Add three friends to the session
    group.add_user(temp1)
    group.add_user(temp2)
    group.add_user(temp3)


# Host is already part of another session
# Test fails since user "bob" is already in a session
def test_04():
    acc = account.get_account("bob")
    if acc.username == "":
        print("username is not found")
        raise Exception
    if acc.in_session is True:
        print("user is already in session")
        raise Exception

    user = account.get_account("bob")


# Session not found for get_host()
def test_05():
    session.get_host("session_name_entry")


# Host gets replaced in session once they leave
def test_06():
    db = firestore.client()

    host = account.create_account("U1_test06", "bird")
    group = session.create_session("test_06", host.username)
    guest1 = account.create_account("U2_test06", "pig")
    guest2 = account.create_account("U3_test06", "skunk")
    group.add_user(guest1)
    group.add_user(guest2)

    # host leaves session
    host.leave_session()
    db.collection('users').document(host.username).update({'in_session': False})

    # ! ! Currently trying to get the field deleted in firebase ! !
    # ! ! Just setting it to None for now ! !
    db.collection('sessions').document(group.name.id).update({host.username: None})

    group.host = None
    group.find_new_host()


if __name__ == "__main__":
    cred = credentials.Certificate(r"database-access-key.json")
    firebase_admin.initialize_app(cred)

    account.create_account("riley", "pancakes")
    test_06()
