class Language:
    def __init__(self, idioma, nivel):
        self.idioma = idioma
        self.nivel = nivel

    def __str__(self):
        return "Language: {} {}".format(self.idioma, self.nivel)

