class User:
    def __init__(self, username, desc, roles):
        self.username = username
        self.roles = roles
        self.desc = desc
        self.lns = {}

    def looking_for_team(self, desc):
        self.desc = desc
        return self