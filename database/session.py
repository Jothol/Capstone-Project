from firebase_admin import firestore
from database import account


def create_session(session_name, host_name):
    db = firestore.client()
    session = db.collection('sessions').document(session_name)
    host = db.collection('users').document(host_name)
    if session.get().exists:
        print('create_session error: session already exists.')
        return None
    elif not host.get().exists:
        print('create_session error: user not found.')
        return None
    else:
        session.set({'Session Name': session_name})
        session.set({'host': host_name})
        return Session(session_name)


def delete_session(session_name, host_name):
    db = firestore.client()
    session = db.collection('sessions').document(session_name)
    # host = db.collection('users').document(host_name)
    if session.get().exists:
        session.delete()
        return True
    else:
        print('delete_session error: session does not exist.')
        return False


def get_session(session_name):
    db = firestore.client()
    session = db.collection('sessions').document(session_name)
    if session.get().exists:
        return Session(session_name)
    else:
        print('get_session error: session does not exist.')
        return None


def get_host(session_name):
    if get_session(session_name) is None:
        print('get_host error: session does not exist')
    else:
        session = get_session(session_name)
        return session.name.collection('host')


# def add_user(user_name):
#     if get_session() = None


class Session:
    def __init__(self, session_name):
        self.db = firestore.client()
        self.name = self.db.collection('sessions').document(session_name)
        #self.host = self.name.collection('host').document(host_name)


    def get_name(self):
        return self.name

    # Get the host name retrieval working
    def get_host(self):
        return self.host
