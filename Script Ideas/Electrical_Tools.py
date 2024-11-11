# def desbalanceo(FaseA, FaseB, FaseC):
#     return ((max(FaseA, FaseB, FaseC) - min(FaseB, FaseB, FaseC))
#             / max(FaseB, FaseB, FaseC)) * 100

#clases
class Tablero:
    def __init__(self,name, FaseA, FaseB, FaseC):
        self.name = name
        self.FaseA = FaseA
        self.FaseB = FaseB
        self.FaseC = FaseC

    def desbalanceo(self):
        return ((max(self.FaseA, self.FaseB, self.FaseC) - min(self.FaseA, self.FaseB, self.FaseC))
                / max(self.FaseA, self.FaseB, self.FaseC) * 100)



tabA = Tablero("TAB-ABC", 458, 648, 485)
tabB = Tablero("TAB-DEF", 175, 782, 175)
tabC = Tablero("TAB-GHI", 147, 147, 863)

listtab = {tabA , tabB, tabC}

for i in listtab:
    print(f"El desbalanceo del tablero es:", round(i.desbalanceo(),2),"%")