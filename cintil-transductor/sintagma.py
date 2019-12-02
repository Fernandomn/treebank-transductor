class Sintagma:

    def __init__(self, classe, filhos, classe_pai, valor):
        self.classe = classe
        self.filhos = filhos  # para nao terminais
        self.classe_pai = classe_pai  # para nao-raiz
        self.valor = valor  # apenas para nos folha

    def removeFilho(self, filho):
        posicao = self.filhos.index(filho)
        for neto in reversed(filho.filhos):
            neto.classe_pai = self.classe
            self.filhos.insert(posicao, neto)
        # self.filhos += filho.filhos
        self.filhos.remove(filho)
