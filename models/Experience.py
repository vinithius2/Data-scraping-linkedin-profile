class Experience:
    def __init__(self, cargo, tempo, descricao):
        self.cargo = cargo
        self.anos = tempo.get('anos')
        self.meses = tempo.get('meses')
        self.descricao = descricao

    def __str__(self):
        return "Experience: {} {} {} {}".format(self.cargo, self.anos, self.meses, self.descricao)
