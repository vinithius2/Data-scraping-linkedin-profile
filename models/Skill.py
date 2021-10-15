class Skill:
    def __init__(self, titulo, indications, verify):
        self.titulo = titulo
        self.indications = indications
        self.verify = verify

    def __str__(self):
        return "Skill: {} {} {}".format(self.titulo, self.indications, self.verify)