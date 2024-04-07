from firebase_admin import firestore
from src.database import account


# Session gets added into the Google Firebase 'sessions' collection
# session_name: title of session (String type)
# host_name: the user that is hosting the session (Account type)
def create_session(session_name, user_host):
    if not isinstance(user_host, account.Account):
        print("host must be an Account object")
        return

    db = firestore.client()
    session = db.collection('sessions').document(session_name)
    host = db.collection('users').document(user_host.username)
    if session.get().exists:
        print('create_session error: session already exists.')
        return
    if not host.get().exists:
        print('create_session error: user not found.')
        return

    session.set({host.id: 'host'})
    user_host.in_session = True
    return Session(session_name)


def delete_session(sess):
    db = firestore.client()

    if sess is None:
        print("delete_session error: session does not exist")

    # key-value format to retrieve names of users and what role they are in the session
    user_list = sess.get().to_dict()
    while user_list.__len__() > 0:
        temp = user_list.popitem()
        db.collection('users').document(temp[0]).update({'in_session': False})
        acc = account.Account(temp[0])
        acc.in_session = False

    sess.delete()
    return True


# Returns the Session searched by session_name
# ! ! session_name must be a String type ! !
def get_session(session_name):
    db = firestore.client()
    session = db.collection('sessions').document(session_name)
    if not session.get().exists:
        return None

    return Session(session_name)


# Returns the 'Account' host from the session_name
# ! ! session_name must be a String object ! !
def get_host(sess):
    if sess is None:
        print("get_host error: session does not exist")
        return

    user_list = sess.get().to_dict()
    while user_list.__len__() > 0:
        temp = user_list.popitem()
        if temp[1] == "host":
            return account.Account(temp[0])

    return None


def get_user(sess, user_name):
    if sess is None:
        print("get_user error: session does not exist")
        return

    user_list = sess.get().to_dict()
    while user_list.__len__() > 0:
        temp = user_list.popitem()
        if temp[0] == user_name:
            return account.Account(user_name)

    return None


# Collection updates to get rid of the user that left the session
def update_collection_from_remove(sess, removed_user):
    # db = firestore.client()
    # name = db.collection('sessions').document(session_name)
    if sess is None:
        print('get_host error: session does not exist')
        return

    user_list = sess.get().to_dict()
    sess.set({})
    if user_list.__len__() == 1:
        for col in sess.collections():
            for doc in col.list_documents():
                doc.delete()
        sess.delete()  # actual deletion of session name in firebase
        return

    while user_list.__len__() > 0:
        temp = user_list.popitem()
        if temp[0] != removed_user.username:
            sess.update({temp[0]: temp[1]})

    return


class Session:
    def __init__(self, session_name):
        self.db = firestore.client()
        self.batch = self.db.batch()
        self.name = self.db.collection('sessions').document(session_name)
        self.host = get_host(self.name)
        self.host.account.update({'in_session': True})
        self.songs_played = 0
        self.saved_song = self.name.collection('saved songs').document(' ')
        self.saved_song.set({'URI': '', 'song_name': '', 'album': ''})
        self.current_song = self.name.collection('session info').document('current song')
        if self.current_song.get().to_dict() is None:
            self.current_song.set({'URI': '', 'song_name': '', 'album': '', 'likes': 0, 'dislikes': 0})
        self.likes = self.get_likes()
        self.dislikes = self.get_dislikes()


    def get_name(self):
        return self.name.id

    def get_host(self):
        return self.host

    def get_uri(self):
        return self.current_song.get().to_dict().get('URI')

        pass

    def get_likes(self):
        return self.current_song.get().get('likes')

    # Increases likes when user presses like button
    def increment_likes(self):
        self.likes += 1
        self.current_song.update({'likes': self.likes})

    # Decrease likes when user unpresses like button
    def decrement_likes(self):
        if self.likes == 0:
            print("Likes is at 0 and cannot be a negative number")
            return

        self.likes -= 1
        self.current_song.update({'likes': self.likes})

    def get_dislikes(self):
        return self.current_song.get().get('dislikes')

    # Increase dislikes when user presses dislike button
    def increment_dislikes(self):
        self.dislikes += 1
        self.current_song.update({'dislikes': self.dislikes})

    # Decrease dislikes when user unpresses dislike button
    def decrement_dislikes(self):
        if self.dislikes == 0:
            print("Dislikes is at 0 and cannot be a negative number")
            return

        self.dislikes -= 1
        self.current_song.update({'dislikes': self.dislikes})


    # Used for moving to next song and need to reset fields for likes and dislikes
    def reset_likes_and_dislikes(self):
        self.likes = 0
        self.dislikes = 0
        self.current_song.update({'likes': self.likes})
        self.current_song.update({'dislikes': self.dislikes})

    def set_uri(self, new_uri):
        self.current_song.update({'URI': new_uri})

    # Adds new user to the session
    # ! ! user must be an Account type ! !
    def add_user(self, acc):
        if acc is None:
            print('add_user error: user does not exist')
            return
        if acc.in_session is True:
            print('add_user error: user is already in a session')
            return
        self.name.update({acc.username: 'user'})
        acc.account.update({'in_session': True})
        acc.in_session = True

    def remove_user(self, user):
        if user is None:
            print("user not found in session")
            return

        user.account.update({'in_session': False})
        user.in_session = False
        update_collection_from_remove(self.name, user)

    def remove_host(self):
        self.host.account.update({'in_session': False})
        self.host.in_session = False
        update_collection_from_remove(self.name, self.host)
        self.host = None

        if self.name.get().exists is True:
            print("grass")
            self.find_new_host()

        return

    # Get someone to test this method out
    def find_new_host(self):
        if self.host is not None:
            print("find_new_host error: host still exists in" + self.name.id)
            return

        temp = self.name.get().to_dict()
        new_host = temp.popitem()

        self.host = account.Account(new_host[0])
        self.name.update({self.host.username: 'host'})

    def add_song(self, song_name, artist):
        song = str(self.songs_played + 1) + '. ' + song_name

        self.name.collection('saved_songs').document(song)
        self.name.collection('saved_songs').document(song).set({'song': song_name, 'artist': artist})
        self.songs_played += 1
