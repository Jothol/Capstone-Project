from firebase_admin import firestore


class User:
    def __init__(self):
        self.db = firestore.client()

    def add_user(self):
        users = self.db.collection('users').document('fkgHhAByiXIbskPfiqll')
        users.set({'name': 'jon'})
