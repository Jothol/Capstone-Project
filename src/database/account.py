from firebase_admin import firestore


def create_account(username, password):
    db = firestore.client()
    account = db.collection('users').document(username)
    if account.get().exists:
        print('create_account error: user already exists.')
        return None
    else:
        account.set({'password': password, 'first_name': '', 'last_name': '', 'email': '', 'in_session': False})
        return Account(username)


def delete_account(username):
    db = firestore.client()
    account = db.collection('users').document(username)
    if account.get().exists:
        account.delete()
        return True
    else:
        print('delete_account error: user does not exist.')
        return False


def get_account(username):
    db = firestore.client()
    account = db.collection('users').document(username)
    if account.get().exists:
        return Account(username)
    else:
        print('get_account error: user does not exist.')
        return None


def try_login(username, password):
    db = firestore.client()
    account = db.collection('users').document(username).get()
    if account.exists and account.to_dict().get('password') == password:
        return True
    else:
        print('login error: invalid login.')
        return False


class Account:
    def __init__(self, username):
        self.db = firestore.client()
        self.account = self.db.collection('users').document(username)
        self.username = username
        self.password = self.account.get().to_dict().get('password')
        self.first_name = ''
        self.last_name = ''
        self.email = ''

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def reset_password(self, password):
        self.password = password
        self.account.update({'password': password})

    def set_first_name(self, first_name):
        self.account.update({'first_name': first_name})
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.account.update({'last_name': last_name})
        self.last_name = last_name

    def set_email(self, email):
        self.account.update({'email': email})
        self.email = email

    def get_first_name(self):
        return self.account.get().to_dict()['first_name']

    def get_last_name(self):
        return self.account.get().to_dict()['last_name']

    def get_email(self):
        return self.account.get().to_dict()['email']