from firebase_admin import firestore


def create_account(username, password):
    db = firestore.client()
    account = db.collection('users').document(username)
    if account.get().exists:
        print('create_account error: user already exists.')
        return None
    else:
        account.set({'password': password, 'first_name': '', 'last_name': '', 'email': '', 'in_session': False,
                     'friends': '', 'invites': ''})
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
    if username is None:
        return None
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
        self.first_name = self.account.get().to_dict().get('first_name')
        self.last_name = self.account.get().to_dict().get('last_name')
        self.email = self.account.get().to_dict().get('email')
        self.in_session = self.account.get().to_dict().get('in_session')
        self.friends = self.account.get().to_dict().get('friends')
        self.invites = self.account.get().to_dict().get('invites')

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

    def get_in_session(self):
        return self.in_session

    def leave_session(self):
        if not self.in_session:
            print("leave_session error: user is not in a session")
            return

        self.in_session = False

    def add_friend(self, friend_name):
        friends = self.account.get().to_dict()['friends']
        friend = get_account(friend_name)
        if friend is None:
            return False
        if friend_name in friends or friend_name == self.username:
            return False
        if len(friends) > 0:
            friends = friends + ", "
        friends = friends + friend_name
        self.account.update({'friends': friends})
        self.friends = friends
        return True

    def remove_friend(self, friend_username):
        friends = self.account.get().to_dict()['friends']
        if friend_username not in friends:
            return False
        friends_list = friends.split(", ")
        friends_list.remove(friend_username)
        friends = ", ".join(friends_list)
        self.account.update({'friends': friends})
        self.friends = friends

        friend = get_account(friend_username)
        friend_friends = friend.get_friends()
        if self.username in friend_friends:
            friend_friends_list = friend_friends.split(", ")
            friend_friends_list.remove(self.username)
            friend_friends = ", ".join(friend_friends_list)
            friend.account.update({'friends': friend_friends})
        return True

    def get_friends(self):
        return self.account.get().to_dict()['friends']

    def send_invite(self, friend_username):
        friends = self.account.get().to_dict()['friends']
        friend = get_account(friend_username)
        if friend_username in friends:
            return False
        if friend is None:
            return False
        friends_invites = friend.account.get().to_dict()['invites']
        if self.username in friends_invites:
            return False
        if len(friends_invites) > 0:
            friends_invites = friends_invites + ", "
        friends_invites = friends_invites + self.username
        friend.account.update({'invites': friends_invites})
        friend.invites = friends_invites
        return True

    def get_invites(self):
        return self.account.get().to_dict()['invites']

    def accept_invite(self, friend_username):
        invites = self.account.get().to_dict()['invites']
        invites_list = invites.split(", ")
        invites_list.remove(friend_username)
        invites = ", ".join(invites_list)
        self.account.update({'invites': invites})
        self.invites = invites
        self.add_friend(friend_username)
        get_account(friend_username).add_friend(self.username)

        self.delete_invite(friend_username)
        return True

    def decline_invite(self, friend_username):
        invites = self.account.get().to_dict()['invites']
        if friend_username not in invites:
            return False
        invites_list = invites.split(", ")
        invites_list.remove(friend_username)
        invites = ", ".join(invites_list)
        self.account.update({'invites': invites})
        self.invites = invites

        self.delete_invite(friend_username)
        return True

    def delete_invite(self, friend_username):
        friend = get_account(friend_username)
        friend_invites = friend.get_invites()
        if self.username in friend_invites:
            friend_invites_list = friend_invites.split(", ")
            friend_invites_list.remove(self.username)
            friend_invites = ", ".join(friend_invites_list)
            friend.account.update({'invites': friend_invites})
