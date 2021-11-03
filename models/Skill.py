class Skill:
    def __init__(self, title, indications, verify):
        self.title = title
        self.indications = indications
        self.verify = verify

    def __str__(self):
        return "Skill: {} {} {}".format(self.title, self.indications, self.verify)