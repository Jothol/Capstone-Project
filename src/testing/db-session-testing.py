import firebase_admin
from firebase_admin import credentials, firestore
from src.database import session, account


# Both methods fail since "test" hasn't been created
def test_01():
    session.get_session("test")
    session.delete_session()


# Cannot create session since account "peter" is not created
def test_02():
    session.create_session("test_02", "peter")


# Makes a session
def test_03():
    # Get an account name to become the host of the session
    # account.create_account("bob", "bob_backwards")
    acc = account.get_account('bob')

    # Creates the session
    group = session.create_session("test_03", acc)  # fix host_name issue

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
    sess = session.get_session("session_name_entry")
    print(sess)
    session.get_host(sess)


# Host gets replaced in session once they leave
def test_06():
    db = firestore.client()

    host = account.create_account("U1_test06", "bird")
    group = session.create_session("test_06", host)
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
    session.delete_session()


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

# basic creation of session
def test_09():
    db = firestore.client()
    acc = account.get_account('abc123')

    session.create_session("test_09", acc)

# first testing of subcollections in a session
def test_10():
    db = firestore.client()
    test6_ref = db.collection('sessions').document('test_06')
    message_ref = message_ref = test6_ref.collection('songs').document('success')
    message_ref.set({})
    print(message_ref.get().exists)

# add song test and # of songs saved/played
def test_11():
    sess = session.get_session('test_03')
    count = '1.'
    song_name = 'Smoke and Mirrors'
    sess.add_song(count + ' ' + song_name, 'Imagine Dragons')


def test_12():
    # acc = account.create_account('test_12', 'test')
    # sess = session.create_session('test_12', 'test_12')

    sess = session.get_session('test_12')

    message_ref = sess.name.collection('artists').document('Imagine Dragons')
    message_ref.set({'Smoke and Mirrors': 'song'})

    message_ref = sess.name.collection('artists').document('Coldplay')
    message_ref.set({'The Scientist': 'A Rush of Blood to the Head'})

    message_ref = sess.name.collection('artists').document('Michael Jackson')
    message_ref.set({'Thriller': '1982'})

# song storage idea #1
def test_13():
    # acc = account.create_account('test_13', 'test')
    # sess = session.create_session('test_13', 'test_13')

    sess = session.get_session('test_13')

    message_ref = sess.name.collection('songs').document('Smoke of Mirrors')
    message_ref.set({'Imagine Dragons': 'artist', 'Smoke + Mirrors (Deluxe)': 'album'})

    message_ref = sess.name.collection('songs').document('The Scientist')
    message_ref.set({'Coldplay': 'artist', 'A Rush of Blood to the Head': 'album'})

    message_ref = sess.name.collection('songs').document('Thriller')
    message_ref.set({'Michael Jackson': 'artist', 'Thriller': 'album'})


# song storage idea #2
def test_14():
    acc = account.create_account('test_14', 'test')
    sess = session.create_session('test_14', acc)

    sess = session.get_session('test_14')
    print(sess)

    message_ref = sess.name.collection('albums').document('Smoke + Mirrors (Deluxe')
    message_ref.set({'Smoke and Mirrors': 'song', 'Imagine Dragons': 'artist'})

    message_ref = sess.name.collection('albums').document('A Rush of Blood to the Head')
    message_ref.set({'The Scientist': 'song', 'Coldplay': 'artist'})

    message_ref = sess.name.collection('albums').document('Thriller')
    message_ref.set({'Thriller': 'song', 'Michael Jackson': 'artist'})

# song storage idea #3
def test_15():
    # acc = account.create_account('test_15', 'test')
    acc = account.get_account('test_15')
    sess = session.create_session('test_15', acc)
    sess = session.get_session('test_15')

    sess.add_song('Smoke and Mirrors', 'Imagine Dragons')
    sess.add_song('The Scientist', 'Coldplay')
    sess.add_song('Thriller', 'Michael Jackson')

# testing session with size of 10 users
def test_16():
    # acc1 = account.create_account('t16_1', 'one')
    # acc2 = account.create_account('t16_2', 'two')
    # acc3 = account.create_account('t16_3', 'three')
    # acc4 = account.create_account('t16_4', 'four')
    # acc5 = account.create_account('t16_5', 'five')
    # acc6 = account.create_account('t16_6', 'six')
    # acc7 = account.create_account('t16_7', 'seven')
    # acc8 = account.create_account('t16_8', 'eight')
    # acc9 = account.create_account('t16_9', 'nine')
    # acc10 = account.create_account('t16_10', 'ten')

    acc1 = account.get_account('t16_1')
    acc2 = account.get_account('t16_2')
    acc3 = account.get_account('t16_3')
    acc4 = account.get_account('t16_4')
    acc5 = account.get_account('t16_5')
    acc6 = account.get_account('t16_6')
    acc7 = account.get_account('t16_7')
    acc8 = account.get_account('t16_8')
    acc9 = account.get_account('t16_9')
    acc10 = account.get_account('t16_10')

    user = account.get_account('riley')

    sess = session.create_session('test_16', acc1)
    # sess = session.get_session('test_16')

    sess.add_user(acc2)
    sess.add_user(acc3)
    sess.add_user(acc4)
    sess.add_user(acc5)
    sess.add_user(acc6)
    sess.add_user(acc7)
    sess.add_user(acc8)
    sess.add_user(acc9)
    sess.add_user(acc10)

    sess.add_user(user)
    sess.remove_user(user)

# testing of retrieving uri and changing uri of current song
def test_17():
    acc = account.get_account('riley')
    sess = session.create_session('temp', acc)
    # sess = session.get_session("temp")
    print(sess)
    print(sess.get_uri())
    sess.set_uri('bingbong')
    print(sess.get_uri())

# subcollection deleting test
def test_18():
    acc = account.get_account("bob")
    # sess = session.create_session('test_18', acc)
    sess = session.get_session("test_18")
    temp = sess.db.collection('sessions').document('test_18').collections()
    for col in sess.name.collections():
        for doc in col.list_documents():
            doc.delete()
    sess.name.delete()

def test_19():
    sess = session.get_session("imtheaprilfool")
    print(sess.name.collection("saved songs").id)

    for i in sess.name.collection("saved songs").list_documents():
        print(i.get().get("URI"))

    print(sess.name.collection("saved songs").get("track1"))

# Testing likes and dislikes
def test_20():
    acc = account.get_account("george")
    # sess = session.create_session("poptart", acc)
    sess = session.get_session("poptart")

    # likes field in firebase increases by 2
    sess.increment_likes()
    sess.increment_likes()

    # dislikes field in firebase increases by 4
    sess.increment_dislikes()
    sess.increment_dislikes()
    sess.increment_dislikes()
    sess.increment_dislikes()

    # prints out likes and dislikes
    print("Likes: ", sess.get_likes())
    print("Dislikes: ", sess.get_dislikes())
    print("\n")

    # likes field in firebase decreases by 3
    sess.decrement_likes()
    sess.decrement_likes()
    sess.decrement_likes()  # does not go through since current values of likes is 0

    # dislikes field in firebase decreases by 2
    sess.decrement_dislikes()
    sess.decrement_dislikes()

    # another print statement of likes and dislikes
    print("Likes: ", sess.get_likes())
    print("Dislikes: ", sess.get_dislikes())
    print("\n")

    # rests all likes and dislikes when a new song is played
    sess.reset_likes_and_dislikes()

    # final print statement of likes and dislikes
    print("Likes: ", sess.get_likes())
    print("Dislikes: ", sess.get_dislikes())



if __name__ == "__main__":
    cred = credentials.Certificate(r"database-access-key.json")
    firebase_admin.initialize_app(cred)

    # account.create_account("riley", "pancakes")
    # account.create_account("db_test", "d")

    # Just for test_16
    # sess = session.get_session('test_16')
    # session.delete_session(sess.name)
    # Just for test_16

    test_20()

# helpful links
# https://cloud.google.com/firestore/docs/manage-data/delete-data#collections
