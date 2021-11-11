class Migration:
    def __init__(self, name_file, user_version, datetime=None):
        self.name_file = name_file
        self.user_version = user_version
        self.datetime = datetime

    def __str__(self):
        return "Migration: {} {}".format(self.name_file, self.user_version)

