class Sintagma:

    def __init__(self, classe, filhos, classe_pai, valor):
        self.classe = classe
        self.filhos = filhos  # para nao terminais
        self.classe_pai = classe_pai  # para nao-raiz
        self.valor = valor  # apenas para nos folha

    def removeFilhoConservaNetos(self, filho):
        posicao = self.filhos.index(filho)
        for neto in reversed(filho.filhos):
            neto.classe_pai = self.classe
            self.filhos.insert(posicao, neto)

        self.filhos.remove(filho)

    def removeFilho(self, filho):
        self.filhos.remove(filho)

    def atualizaClasseFilhos(self):
        for filho in self.filhos:
            filho.classe_pai = self.classe

    def absorveFilhos(self):
        valor_prov = ''
        for filho in (self.filhos):
            valor_prov += ' ' + filho.valor
        for filho in reversed(self.filhos):
            self.removeFilho(filho)
        self.valor = valor_prov.strip()

    def absorveFilhosSingleLine(self):
        tagConjCoord = 'CC'
        tagFlat = '_FLAT_'
        conjIndex = -1
        valor_prov = ''
        for i in range(len(self.filhos)):
            filho = self.filhos[i]
            valor_prov += ' ' + filho.valor
            if filho.classe == tagConjCoord or filho.classe == tagFlat:
                conjIndex = i
                break
        if conjIndex >= 0:
            for j in reversed(range(conjIndex + 1)):
                filho = self.filhos[j]
                self.removeFilho(filho)
        self.valor = valor_prov.strip()
