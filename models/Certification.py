class Certification:
    def __init__(self, titulo):
        self.titulo = titulo

    def __str__(self):
        return "Certification: {}".format(self.titulo)
