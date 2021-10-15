class Experience:
    def __init__(self, cargo, anos, meses, descricao):
        self.cargo = cargo
        self.anos = anos
        self.meses = meses
        self.descricao = descricao

    def __str__(self):
        return "Experience: {} {} {} {}".format(self.cargo, self.anos, self.meses, self.descricao)
