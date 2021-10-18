class Experience:
    def __init__(self, empresa, cargo, anos, meses, descricao):
        self.empresa = empresa
        self.cargo = cargo
        self.anos = anos
        self.meses = meses
        self.descricao = descricao

    def __str__(self):
        return "Experience: {} {} {} {} {}".format(self.empresa, self.cargo, self.anos, self.meses, self.descricao)
