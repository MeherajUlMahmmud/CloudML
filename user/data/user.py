class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


class UserDao:
    def getUser(self, id):
        return User(id, "John", "Doe")

    def getUserByUsername(self, username):
        return User(1, username, "Doe")

    def loginUser(self, username, password):
        return User(1, username, password)

    def registerUser(self, username, password):
        return User(1, username, password)

    def updateUser(self, id, username, password):
        return User(id, username, password)

    def deleteUser(self, id):
        return User(id, "John", "Doe")

    def getAllUsers(self):
        return [User(1, "John", "Doe"), User(2, "Jane", "Doe")]
