from firebase_admin import firestore
from src.database import account


# Session gets added into the Google Firebase 'sessions' collection
# session_name: title of session (String type)
# host_name: the user that is hosting the session (String type)
def create_session(session_name, host_name):
    db = firestore.client()
    session = db.collection('sessions').document(session_name)
    host = db.collection('users').document(host_name)
    if session.get().exists:
        print('create_session error: session already exists.')
        return
    if not host.get().exists:
        print('create_session error: user not found.')
        return

    session.set({host_name: 'host'})
    return Session(session_name)


def delete_session(session_name):
    db = firestore.client()
    session = db.collection('sessions').document(session_name)
    if not session.get().exists:
        print('delete_session error: session not found.')
        return False

    # key-value format to retrieve names of users and what role they are in the session
    sess = session.get().to_dict()
    while sess.__len__() > 0:
        temp = sess.popitem()
        db.collection('users').document(temp[0]).update({'in_session': False})
        acc = account.Account(temp[0])
        acc.in_session = False

    session.delete()
    return True


# Returns the Session searched by session_name
# ! ! session_name must be a String type ! !
def get_session(session_name):
    db = firestore.client()
    session = db.collection('sessions').document(session_name)
    if not session.get().exists:
        print('get_session error: session does not exist.')
        return None

    return Session(session_name)


# Returns the 'Account' host from the session_name
# ! ! session_name must be a String object ! !
def get_host(session_name):
    db = firestore.client()
    name = db.collection('sessions').document(session_name)
    if not name.get().exists:
        print('get_host error: session does not exist')
        return

    sess = name.get().to_dict()
    while sess.__len__() > 0:
        temp = sess.popitem()
        if temp[1] == "host":
            return account.Account(temp[0])

    return None


class Session:
    def __init__(self, session_name):
        self.db = firestore.client()
        self.name = self.db.collection('sessions').document(session_name)
        self.host = get_host(self.name.id)
        self.db.collection('users').document(self.host.username).update({'in_session': True})

    def get_name(self):
        return self.name.id

    def get_host(self):
        return self.host

    # Adds new user to the session
    # ! ! user must be an Account type ! !
    def add_user(self, acc):
        db = firestore.client()
        user = db.collection('users').document(acc.username)
        if not user.get().exists:
            print('add_user error: user not found')
            return
        self.name.update({user.id: 'user'})
        db.collection('users').document(user.id).update({'in_session': True})

    def remove_host(self):
        self.db.collection('sessions').document(self.name.id).update({self.host.username: None})
        self.host = None

        return

    def find_new_host(self):
        if self.host is not None:
            print("find_new_host error: host still exists in" + self.name.id)
            return

        temp = self.db.collection('sessions').document(self.name.id).get().to_dict()
        new_host = temp.popitem()
        while new_host[1] is None:
            new_host = temp.popitem()

        self.host = account.Account(new_host[0])
        self.db.collection('sessions').document(self.name.id).update({self.host.username: 'host'})
