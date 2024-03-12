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
        return
    if acc.in_session is True:
        print("user is already in session")
        return


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

    group.remove_host()
    group.find_new_host()


# Session gets deleted
# ! ! Run test_06 before running this test ! !
def test_07():
    session.delete_session("test_06")


# test_08 is how to add fields for a document in a collection thats in a document in a collection
# for example: 'success' document is in 'songs' collection, 'songs' document is in 'test_03' document.
# And 'test_03' is in 'sessions' collections
def test_08():
    db = firestore.client()
    test3_ref = db.collection('sessions').document('test_03')
    print(test3_ref.get().exists)  # this needs to be True to do the rest

    message_ref = test3_ref.collection('songs').document('success')  # make sure 'songs' exist
    print(message_ref.get().exists)  # False or True won't matter, it will still add the fields
    message_ref.set({'money': 'mr_krabs'})

    # for new collections like 'songs' add them in google firebase rather than implement them here

def test_09():
    db = firestore.client()

    session.create_session("test_09", "abc123")

def test_10():
    db = firestore.client()
    test6_ref = db.collection('sessions').document('test_06')
    message_ref = message_ref = test6_ref.collection('songs').document('success')
    message_ref.set({})
    print(message_ref.get().exists)




if __name__ == "__main__":
    cred = credentials.Certificate(r"database-access-key.json")
    firebase_admin.initialize_app(cred)

    # account.create_account("riley", "pancakes")
    test_10()
