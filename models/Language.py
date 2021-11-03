class Language:
    def __init__(self, language, level):
        self.language = language
        self.level = level

    def __str__(self):
        return "Language: {} {}".format(self.language, self.level)

